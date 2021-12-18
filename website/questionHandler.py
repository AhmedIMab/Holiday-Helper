import json
import os
import sqlite3
import sqlalchemy.exc
from .models import Note, User, Country, UserCountry, UserTravelScore, Sport, Cost, CulturalValue, CovidRestrictions, Safety
from .models import UserCountryScore, CountryDailyCost
from flask_login import login_required, current_user
from sqlalchemy.sql import *
from sqlalchemy import desc
from sqlalchemy.sql import func
from . import db
from enum import Enum


def getQuestions():
    print("Function is running")

    # print(os.getcwd())
    # print(os.path.join("\\website\\static\\questions.json"))
    filename = (os.getcwd() + os.path.join('\\website\\static\\questions.json'))

    f = open(filename, 'r')
    data = json.load(f)
    allQuestions = data.get("questions")
    return allQuestions


def getQuestion(questionID):
    questions = getQuestions()
    print(questionID)
    print("Function 2 is running")

    for question in questions:
        if question.get("questionID") == int(questionID):
            return question

    return None


def isQuestionAnswered(travelID, questionID):
    questionAnswered = False
    #print(current_user.id)
    #print(travelID)

    try:
        current_travel = UserTravelScore.query.get((current_user.id, travelID))

    except (sqlite3.IntegrityError, sqlalchemy.exc.IntegrityError) as e:
        pass

    if current_travel == None:
        current_travel = UserTravelScore.query.get((current_user.id, travelID))


    try:
        y = getattr(current_travel, 'questions_answered')
        questionsAnsweredArray = y.split(',')
        for questionA in questionsAnsweredArray:
            if questionA == "":
                pass
            else:
                if int(questionID) == int(questionA):
                    questionAnswered = True
                    break

    except (UnboundLocalError, AttributeError) as e:
        print("NOTHING ANSWERED")

    return questionAnswered


def haveRequirementsBeenMet(travelID, questionID):
    question = getQuestion(questionID)
    requirementsMet = True

    try:
        current_travel = UserTravelScore.query.get((current_user.id, travelID))

    except (sqlite3.IntegrityError, sqlalchemy.exc.IntegrityError) as e:
        pass

    if current_travel == None:
        current_travel = UserTravelScore.query.get((current_user.id, travelID))


    try:
        questionRequirements = question.get("questionRequirements")
        for requirement in questionRequirements:
            requiredModifier = requirement.get("modifier")
            requiredValue = requirement.get("value")
            x = getattr(current_travel, requiredModifier)
            if x >= requiredValue:
                print("requirement met")
                #requirementsMet = True
            else:
                requirementsMet = False
                break

    except:
        return False


    return requirementsMet


def doesUserWantThisCountry(travelID, countryCode):
    # stores a sql command which will SELECT the country where the user.id is equal to the current user
    # and where the country code is the countryCode passed into the function (countryCode)
    x = select(UserCountry) \
        .where(UserCountry.user_id == current_user.id, UserCountry.country_code == countryCode)

    result = db.session.connection().execute
    result = result.fetchall()
    print("This is the countries the user has travelled to: ", result)

    return True

def filterPrevCountries(travelID, ranked_countries):
    pass


def sortCountries(travelID):
    print("sort countries is running")
    print("this is the travelID", travelID)
    # stores a sql command which will SELECT the countries where the user.id is equal to the current user
    # and where the travel id is the same as travelID
    # Orders the countries by highest to lowest
    x = select(UserCountryScore)\
        .where(UserCountryScore.user_id == current_user.id, UserCountryScore.travel_id == travelID)\
        .order_by(UserCountryScore.total_score.desc())

    # Executes the command
    result = db.session.connection().execute(x)
    result = result.fetchall()
    userSuggestions = []

    country_number = 1
    for score in result:
        travel_cost = score.final_travel_cost
        # Creates a dictionary to later be manipulated by the Jinja templating to display journey cost
        valuesToDisplay = {}
        # Sets the key with text "your journey will cost approximately" to the travel cost in the table
        valuesToDisplay["Your journey will cost approximately"] = travel_cost
        # Adds country as a tuple to the list of userSuggestions
        userSuggestions.append((score.country_code, int(country_number), valuesToDisplay))
        country_number += 1

    return userSuggestions





def userCountryScore(travelID, countryCodesL):
    # multiple enum's as inconsistent naming in databases
    # Every enum class has the have the same order for the names
    # e.g. WATER_SPORTS has to be first one defined in every class
    class UserCountryScoreEnum(Enum):
        WATER_SPORTS = "water_sports_score"
        WINTER_SPORTS = "winter_sports_score"
        CULTURE_SCORE = "culture_score"
        SAFETY_SCORE = "safety_score"
        BUDGET_SCORE = "budget_score"

    class CountryScoreEnum(Enum):
        WATER_SPORTS = "water_sports_score"
        WINTER_SPORTS = "winter_sports_score"
        CULTURE_SCORE = "heritage_score"
        SAFETY_SCORE = "safety_score"
        BUDGET_SCORE = "cost_score"


    class UserScoreEnum(Enum):
        WATER_SPORTS = "water_sports_user_score"
        WINTER_SPORTS = "winter_sports_user_score"
        CULTURE_SCORE = "culture_user_score"
        SAFETY_SCORE = "safety_user_score"
        BUDGET_SCORE = "budget_user_score"



    print("IN USER COUNTRY SCORE FUNCTION")
    for countryCode in countryCodesL:
        try:
            # Sets the current travel to the UserTravelScore of the user with primary key values
            # user_id as the current user id and travel id key as the travel id passed into the function
            current_travel = UserTravelScore.query.get((current_user.id, travelID))
            # Does the same
            current_country = UserCountryScore.query.get((current_user.id, travelID, countryCode))
        except (sqlite3.IntegrityError, sqlalchemy.exc.IntegrityError) as e:
            pass

        if current_travel == None or current_country == None:
            new_user_country = UserCountryScore(user_id=current_user.id,
                                                travel_id=travelID,
                                                country_code=countryCode,
                                                water_sports_score=0,
                                                winter_sports_score=0,
                                                culture_score=0,
                                                safety_score=0,
                                                budget_score=0,
                                                total_score=0,
                                                final_travel_cost=1)
            db.session.add(new_user_country)
            db.session.commit()
            current_country = UserCountryScore.query.get((current_user.id, travelID, countryCode))
            user_score = {}
            user_score_values = []

            for n in UserScoreEnum:
                factor_user_score = getattr(current_travel, n.value)
                user_score[n.name] = (factor_user_score)
                user_score_values.append(factor_user_score)
            # winter_sports_user_score = getattr(current_travel, "winter_sports_user_score")
            # culture_user_score = getattr(current_travel, "water_sports_user_score")
            # safety_user_score = getattr(current_travel, "culture_user_score")
            # budget_user_score = getattr(current_travel, "budget_user_score")
            # print("This is the water sports user score", water_sports_user_score)
            # print("This is the winter sports user score", winter_sports_user_score)
            # print("This is the culture user score", culture_user_score)
            # print("This is the safety user score", safety_user_score)
            # print("This is the budgets user score", budget_user_score)
            # user_score = []
            # user_score.append(water_sports_user_score)
            # user_score.append(winter_sports_user_score)
            # user_score.append(culture_user_score)
            # user_score.append(safety_user_score)
            # user_score.append(budget_user_score)
            #print(user_score)

            most_important_user_score = max(user_score_values)
            country_scores = {}
            countryScore = Sport.query.get((countryCode))
            # Adds a dictionary key of the Water Sports to the attribute of enum value for water sports
            country_scores[CountryScoreEnum.WATER_SPORTS.name] = getattr(countryScore, CountryScoreEnum.WATER_SPORTS.value)
            country_scores[CountryScoreEnum.WINTER_SPORTS.name] = getattr(countryScore, CountryScoreEnum.WINTER_SPORTS.value)
            # country_water_sports_score = getattr(countryScore, CountryScoreEnum.WATER_SPORTS.value)
            # country_winter_sports_score = getattr(countryScore, CountryScoreEnum.WINTER_SPORTS.value)

            countryScore = CulturalValue.query.get((countryCode))
            country_scores[CountryScoreEnum.CULTURE_SCORE.name] = getattr(countryScore, CountryScoreEnum.CULTURE_SCORE.value)
            # country_culture_score = getattr(countryScore, CountryScoreEnum.CULTURE_SPORTS.value)

            countryScore = Safety.query.get((countryCode))
            country_scores[CountryScoreEnum.SAFETY_SCORE.name] = getattr(countryScore, CountryScoreEnum.SAFETY_SCORE.value)
            # country_safety_score = getattr(countryScore, CountryScoreEnum.SAFETY_SCORE.value)

            countryScore = Cost.query.get((countryCode))
            country_scores[CountryScoreEnum.BUDGET_SCORE.name] = getattr(countryScore, CountryScoreEnum.BUDGET_SCORE.value)
            # country_budget_score = getattr(countryScore, CountryScoreEnum.BUDGET_SCORE.value)



            user_relative_scores = {}
            for x in UserScoreEnum:
                factor_relative_score = user_score[x.name] / most_important_user_score
                user_relative_scores[x.name] = factor_relative_score

            userCountryScores = []
            userCountryScoresD = {}
            for y in UserScoreEnum:
                # To deal with no data for that countries factor score
                if country_scores[y.name] is not None:
                    userCountryScoreT = user_relative_scores[y.name] * country_scores[y.name]
                else:
                    # When the value is NULL, sets the value to 0
                    userCountryScoreT = 0

                userCountryScores.append(userCountryScoreT)
                userCountryScoresD[y.name] = userCountryScoreT

            country_daily_cost = CountryDailyCost.query.get((countryCode))
            if country_daily_cost.daily_cost is not None:
                # To get the daily cost for the country, it will multiply the number of travellers by the
                # travelling time and the daily cost of the country using the CountryDailyCost table
                total_cost_for_country = current_travel.num_travellers * current_travel.travelling_time \
                                         * country_daily_cost.daily_cost

                setattr(current_country, "final_travel_cost", total_cost_for_country)
            else:
                total_cost_for_country = 0
                setattr(current_country, "final_travel_cost", total_cost_for_country)


            totalScoreForCountry = sum(userCountryScores)

            for t in UserCountryScoreEnum:
                # adds the value for the factor score, using the value in the Enumerator
                # e.g. the first run of the loop, t.value = water_sports_score
                # and userCountryScoresD[t.name] = value of the dictionary for water_sports score
                setattr(current_country, t.value, userCountryScoresD[t.name])

            setattr(current_country, "total_score", totalScoreForCountry)

    db.session.commit()
    # Runs the sortCountries function to get a list of the countries in an ordered format
    sortedCountries = sortCountries(travelID)

    return sortedCountries






def nextQuestionID(travelID):
    questions = getQuestions()
    questionsStream = questions

    # filter will ask the questions which have not been answered
    # by applying a not to the return of isQuestionAnswered so isQuestionAnswered will take the questionID and travelID
    # it will return True if the question has been answered
    # so by applying a not, the value will be False
    # and the filter function extracts elements from a list which return True therefore ignoring answered questions
    # x is the current element the method is looking at (filter)
    questionsStream = filter(lambda x:not(isQuestionAnswered(1, x.get("questionID"))), questionsStream)
    # second filter will make sure only mandatory questions are asked
    questionsStream = filter(lambda x:x.get("mandatory") == True, questionsStream)
    # Sort the questions by the smallest to biggest questionID (integer)
    questionsStream = sorted(questionsStream, key=lambda x:x.get("questionID"))

    if len(questionsStream) == 0:
        # This will only run when there are no questions left or questions.json is empty/no questions to begin with
        # this series of functions is for checking questions with requirements
        questionsStream = questions
        # so only looks at questions which have requirements (non mandatory)
        questionsStream = filter(lambda x:x.get("mandatory") == False, questionsStream)
        # same as above filter
        # needed so that if a question with requirements is answered we need to make sure it's filtered out
        # and only ask non answered questions
        questionsStream = filter(lambda x: not(isQuestionAnswered(1, x.get("questionID"))), questionsStream)
        # runs the function haveRequirementsBeenMet to get the questions which the user meets requirements for
        questionsStream = filter(lambda x:haveRequirementsBeenMet(travelID, x.get("questionID")), questionsStream)
        questionsStream = sorted(questionsStream, key=lambda x:x.get("questionID"))

        if len(questionsStream) == 0:
            # Will only run when there are no questions to ask/questions with requirements have been met as well
            return 0
        else:
            # sets questionsStream to only the current question
            questionsStream = questionsStream[0]
            # returns the ID of the current question so that it can display the question with the right question ID
            return questionsStream.get("questionID")

    else:
        questionsStream = questionsStream[0]
        return questionsStream.get("questionID")


    print(questionsStream)




def getAnswers(questionID):
    question = getQuestion(questionID)
    #print(type(question))
    answers = question.get("answers")
    print("Function 3 is running")
    #print(answers)
    return answers



def getAnswer(questionID, answerID):
    question = getQuestion(questionID)
    answers = question.get("answers")

    for answer in answers:
        if answer.get("answerID") == int(answerID):
            return answer

    return None



def userQuestionAnswer(questionID, answerValue, travelID):
    question = getQuestion(questionID)
    answer = getAnswer(questionID, answerValue)
    questionType = question.get("questionType")
    questionAnswered = False

    try:
        #print("TTTTTTTTT")
        #print(current_user.id)
        #print(travelID)
        # Tries to get a users possible travel record
        current_travel = UserTravelScore.query.get((current_user.id, travelID))

        #print(current_travel)

    except (sqlite3.IntegrityError, sqlalchemy.exc.IntegrityError) as e:
        pass

    if current_travel == None:
        # if the user has not travelled yet
        # Creates a new record for them
        new_user_travel = UserTravelScore(user_id=current_user.id,
                                          travel_id=1,
                                          questions_answered="",
                                          prev_countries=None,
                                          travelling_time=0,
                                          num_travellers=0,
                                          water_sports_user_score=0,
                                          winter_sports_user_score=0,
                                          culture_user_score=0,
                                          safety_user_score=0,
                                          budget_user_score=0)
        db.session.add(new_user_travel)
        db.session.commit()

        # sets the current_travel to a query of user's newly created record
        current_travel = UserTravelScore.query.get((current_user.id, travelID))



    y = getattr(current_travel, 'questions_answered')
    questionsAnsweredArray = y.split(',')
    for questionA in questionsAnsweredArray:
        if questionA == "":
            pass
        else:
            #print(f"This is the question in the array: {questionA}")
            #print(type(questionA))
            #print(f"This is the id of the question asked: {questionID}")
            #print(type(questionID))
            if int(questionID) == int(questionA):
                questionAnswered = True
                break

    # print(f"This question has been answered? {questionAnswered}")




    if questionAnswered == False:
        # could use if answer == None (?) -> answer hasn't been written in JSON file yet
        if questionType == "Integer":
            print("This is an integer question")
            # Try to make lines 153 to 162 a recursive function?
            # Ask Dom
            answers = getAnswers(questionID)
            #print(answers)
            modifiersX = answers[0]
            #print(modifiersX)
            #print(type(modifiersX))
            modifiers = modifiersX.get("modifiers")
            #print(modifiers)
            #print(type(modifiers))
            toModify = modifiers[0].get("modifier")
            #print(toModify)
            x = getattr(current_travel, toModify)
            setattr(current_travel, toModify, x + int(answerValue))

        elif questionType == "Multiple Choice":
            print("This is a Multiple Choice Question")
            # Modifies the values of the user's score
            for modifier in answer.get("modifiers"):
                if questionAnswered == False:
                    toModify = modifier.get("modifier")
                    modificationBy = modifier.get("value")
                    #print(modificationBy)
                    #print(type(modificationBy))
                    # Gets the attribute name in the database of the modifier
                    x = getattr(current_travel, toModify)
                    #print(x)
                    if type(x) == int:
                        print("This is an integer answer")
                        # Changes the fields value by the modification
                        setattr(current_travel, toModify, x + modificationBy)
                    else:
                        # If the type of the value we are changing is not an int
                        # Sets the attribute to the modification value as opposed to adding
                        setattr(current_travel, toModify, modificationBy)

        # Adds the question to the user's questions answered
        current_travel.questions_answered = current_travel.questions_answered + (str(questionID) + ",")
        #current_travel.questions_answered = ((y) + "," + questionID)

        db.session.commit()

        # Sets the question to answered
        questionAnswered = True

    else:
        print("This question has been answered")















