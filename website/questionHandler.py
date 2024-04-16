import json
import os
import sqlite3
import sqlalchemy.exc
from .models import User, Country, UserCountry, UserTravelScore, Sport, Cost, CulturalValue, MonthlyTemperatures
from .models import UserCountryScore, CountryDailyCost, CovidRestrictions, Safety, Nature, PopulationDensity
from .models import YearlyTemperatures
from flask_login import login_required, current_user
from sqlalchemy.sql import *
from . import db
from enum import Enum
from datetime import datetime


def getQuestions():
    # Access's the questions in the json file

    filename = os.path.join(os.getcwd(), 'website', 'static', 'questions.json')

    f = open(filename, 'r')
    # uses the json module to load it as a JSON object in python
    data = json.load(f)
    allQuestions = data.get("questions")
    return allQuestions


def getQuestion(questionID):
    # For finding the specific question's dictionary of values
    questions = getQuestions()

    for question in questions:
        # iterates through all the questions
        if question.get("questionID") == int(questionID):
            # if it finds the question with the ID passed into the function, returns it
            return question

    return None


def getAnswers(questionID):
    question = getQuestion(questionID)
    answers = question.get("answers")
    # returns a list of all the answers for the particular question
    # this is a dictionary which includes the answerID, text and modifiers
    return answers


def getAnswer(questionID, answerID):
    answers = getAnswers(questionID)

    for answer in answers:
        if answer.get("answerID") == int(answerID):
            # returns the specific answers' values
            return answer

    # if the answerID is not found, return None
    return None


def isQuestionAnswered(travelID, questionID):
    questionAnswered = False
    try:
        # tries to get the user's current travel
        current_travel = UserTravelScore.query.get((current_user.id, travelID))
    except (sqlite3.IntegrityError, sqlalchemy.exc.IntegrityError) as e:
        print(e)

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
        # Runs when no questions have been answered
        pass

    # Returns a boolean value of whether the question has or has not been answered
    return questionAnswered


def haveRequirementsBeenMet(travelID, questionID):
    question = getQuestion(questionID)
    requirementsMet = True
    try:
        current_travel = UserTravelScore.query.get((current_user.id, travelID))

    except (sqlite3.IntegrityError, sqlalchemy.exc.IntegrityError) as e:
        print("THIS IS E2", e)

    try:
        questionRequirements = question.get("questionRequirements")
        for requirement in questionRequirements:
            requiredModifier = requirement.get("modifier")
            requiredValue = requirement.get("value")
            currentValue = getattr(current_travel, requiredModifier)
            if isinstance(requiredValue, int):
                if currentValue >= requiredValue:
                    print("requirement met")
                else:
                    # If the user does not have a greater than or equal score for the required factor
                    requirementsMet = False
                    break
            elif isinstance(requiredValue, str):
                if currentValue == requiredValue:
                    print("requirements met")
                else:
                    requirementsMet = False
                    break
    except:
        # This will run when the question does not have any question requirements
        return False

    return requirementsMet


def nextQuestionID(travelID):
    questions = getQuestions()
    questionsStream = questions

    # filter will ask the questions which have not been answered
    # by applying a not to the return of isQuestionAnswered so isQuestionAnswered will take the questionID and travelID
    # it will return True if the question has been answered
    # so by applying a not, the value will be False
    # and the filter function extracts elements from a list which return True therefore ignoring answered questions
    # x is the current element the method is looking at (filter)
    questionsStream = filter(lambda x:not(isQuestionAnswered(travelID, x.get("questionID"))), questionsStream)
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
        questionsStream = filter(lambda x: not(isQuestionAnswered(travelID, x.get("questionID"))), questionsStream)
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


def doesUserWantThisCountry(countryCode):
    # Retrieves all countries in the user country table
    countries = UserCountry.query.all()
    users_countries = []

    # loops through every record in the list of objects (records in the table)
    for country in countries:
        # if the user id is the same as the current user
        if country.user_id == current_user.id:
            # add the country code to the list of users visited countries
            users_countries.append(country.country_code)

    # loops through each country in the users countries
    for country in users_countries:
        # if the inputted country code is located in the users countries
        if countryCode in users_countries:
            return True
        else:
            return False


def filterPrevCountries(codes, travelID):
    try:
        # Sets the current travel to the UserTravelScore of the user with primary key values
        # user_id as the current user id and travel id key as the travel id passed into the function
        current_travel = UserTravelScore.query.get((current_user.id, travelID))
    except (sqlite3.IntegrityError, sqlalchemy.exc.IntegrityError) as e:
        print(e)

    prev_countries = getattr(current_travel, "prev_countries")
    if prev_countries == True:
        return codes
    else:
        # For every country code
        # it will check if the country code is one of the users visited countries
        # by applying a not, if the country is one of the users countries
        # the doesUserWantThisCountry will return True
        # as it's a not, the value will become false
        # as a filter function which will extract elements from a list which return True
        # it means only the countries which return false in the doesUserWantThisCountry function will be extracted
        suggestionsStream = filter(lambda x:not(doesUserWantThisCountry(x)), codes)
        suggestionsStream = list(suggestionsStream)
        return suggestionsStream

def sortCountries(travelID):
    #print("sort countries is running")
    # Executes the command
    # stores a sql command which will SELECT the countries where the user.id is equal to the current user
    # and where the travel id is the same as travelID
    # Orders the countries by highest to lowest

    x = select(UserCountryScore)\
        .where(UserCountryScore.user_id == current_user.id, UserCountryScore.travel_id == travelID)\
        .order_by(UserCountryScore.total_score.desc())

    # Executes the command
    result = db.session.connection().execute(x)
    result = result.fetchall()

    uCountryCodes = []
    for country in result:
        countryCode = country[2]
        uCountryCodes.append(countryCode)


    userSuggestions = []

    filteredCountries = filterPrevCountries(uCountryCodes, travelID)
    #print("filteredCountries in sort countries", filteredCountries)

    country_number = 1
    for country in filteredCountries:
        result = UserCountryScore.query.get((current_user.id, travelID, country))
        travelCost = result.final_travel_cost
        # Creates a dictionary to later be manipulated by the Jinja templating to display journey cost
        valuesToDisplay = {}
        # Sets the key with text "your journey will cost approximately" to the travel cost in the table
        valuesToDisplay["Your journey will cost approximately"] = f"{travelCost:0.2f}"
        # Adds country as a tuple to the list of userSuggestions
        userSuggestions.append((country, int(country_number), valuesToDisplay))
        country_number += 1

    return userSuggestions


def calculateTempScores(travelID, countryCodes, temps, temp_differences_squared):
    valuesX = temp_differences_squared.values()
    temps_d_squared_list = list(valuesX)
    minimum_temp_d_squared = min(temps_d_squared_list)
    maximum_temp_d_sqaured = max(temps_d_squared_list)
    normalised_temps = {}
    for country, temp in temp_differences_squared.items():
        temp = float(temp)
        # To normalise the value between 0 to 50
        # Only normalised 0 to 50 as opposed to 0 to 100 as I would prefer to for the temperature to not have a large
        # weighting on the score for the country
        # Also did not normalise into negative values as I would like the temperature to refine to a more suited country
        # as opposed to dispersing the countries which do not meet the temperature
        temp_normalised = ((temp-min(temps_d_squared_list))/((max(temps_d_squared_list)-min(temps_d_squared_list))))*100
        # Inverse as it is currently a giving a larger number the further away it is from the users score...
        temp_inverse = (-1 * temp_normalised) + 100
        normalised_temps[country] = temp_inverse

    # print(f"These are inverse normalised temps:", normalised_temps)

    for country_code in countryCodes:
        country_temp = normalised_temps[country_code]
        current_country = UserCountryScore.query.get((current_user.id, travelID, country_code))
        x = getattr(current_country, "temp_score")
        setattr(current_country, "temp_score", x+country_temp)


def calculateCountryScores(travelID, countryCodes):
    # multiple enum's as inconsistent naming in databases
    # Every enum class has the have the same order for the names
    # e.g. WATER_SPORTS has to be first one defined in every class
    class UserCountryScoreEnum(Enum):
        WATER_SPORTS = "water_sports_score"
        WINTER_SPORTS = "winter_sports_score"
        CULTURE_SCORE = "culture_score"
        NATURE_SCORE = "nature_score"
        SAFETY_SCORE = "safety_score"
        BUDGET_SCORE = "budget_score"
        DENSITY_SCORE = "pop_density_score"

    class CountryScoreEnum(Enum):
        WATER_SPORTS = "water_sports_score"
        WINTER_SPORTS = "winter_sports_score"
        CULTURE_SCORE = "heritage_score"
        NATURE_SCORE = "nature_score"
        SAFETY_SCORE = "safety_score"
        BUDGET_SCORE = "cost_score"
        DENSITY_SCORE = "pop_density_score"


    class UserScoreEnum(Enum):
        WATER_SPORTS = "water_sports_user_score"
        WINTER_SPORTS = "winter_sports_user_score"
        CULTURE_SCORE = "culture_user_score"
        NATURE_SCORE = "nature_user_score"
        SAFETY_SCORE = "safety_user_score"
        BUDGET_SCORE = "budget_user_score"
        DENSITY_SCORE = "pop_density_user_score"

    try:
        # Sets the current travel to the UserTravelScore of the user with primary key values
        # user_id as the current user id and travel id key as the travel id passed into the function
        current_travel = UserTravelScore.query.get((current_user.id, travelID))
    except (sqlite3.IntegrityError, sqlalchemy.exc.IntegrityError) as e:
        print(e)

    missing_monthly_temps = 0
    temps = {}
    temp_differences_squared = {}
    for countryCode in countryCodes:
        # Loops through every country's code in the list of all countryCodes
        # Does the same for the current country
        current_country = UserCountryScore.query.get((current_user.id, travelID, countryCode))
        if current_travel == None or current_country == None:
            # When the country does not have a score
            # Adds a new default record
            new_user_country = UserCountryScore(user_id=current_user.id,
                                                travel_id=travelID,
                                                country_code=countryCode,
                                                water_sports_score=0,
                                                winter_sports_score=0,
                                                culture_score=0,
                                                nature_score=0,
                                                temp_score=0,
                                                safety_score=0,
                                                budget_score=0,
                                                pop_density_score=0,
                                                total_score=0,
                                                final_travel_cost=1)
            db.session.add(new_user_country)
            db.session.commit()
            # sets the current_country to a query of country's newly created record
            current_country = UserCountryScore.query.get((current_user.id, travelID, countryCode))
            user_score = {}
            user_score_values = []

            for n in UserScoreEnum:
                factor_user_score = getattr(current_travel, n.value)
                user_score[n.name] = (factor_user_score)
                user_score_values.append(factor_user_score)

            most_important_user_score = max(user_score_values)

            country_scores = {}
            countryScore = Sport.query.get(countryCode)
            # Adds a dictionary key of the Water Sports to the attribute of enum value for water sports
            country_scores[CountryScoreEnum.WATER_SPORTS.name] = getattr(countryScore,
                                                                         CountryScoreEnum.WATER_SPORTS.value)
            country_scores[CountryScoreEnum.WINTER_SPORTS.name] = getattr(countryScore,
                                                                          CountryScoreEnum.WINTER_SPORTS.value)

            countryScore = CulturalValue.query.get((countryCode))
            country_scores[CountryScoreEnum.CULTURE_SCORE.name] = getattr(countryScore,
                                                                          CountryScoreEnum.CULTURE_SCORE.value)

            countryScore = Safety.query.get((countryCode))
            country_scores[CountryScoreEnum.SAFETY_SCORE.name] = getattr(countryScore,
                                                                         CountryScoreEnum.SAFETY_SCORE.value)

            countryScore = Cost.query.get((countryCode))
            country_scores[CountryScoreEnum.BUDGET_SCORE.name] = getattr(countryScore,
                                                                         CountryScoreEnum.BUDGET_SCORE.value)

            countryScore = Nature.query.get((countryCode))
            country_scores[CountryScoreEnum.NATURE_SCORE.name] = getattr(countryScore,
                                                                         CountryScoreEnum.NATURE_SCORE.value)

            countryScore = PopulationDensity.query.get((countryCode))
            country_scores[CountryScoreEnum.DENSITY_SCORE.name] = getattr(countryScore,
                                                                          CountryScoreEnum.DENSITY_SCORE.value)


            user_relative_scores = {}
            for x in UserScoreEnum:
                factor_relative_score = user_score[x.name] / most_important_user_score
                user_relative_scores[x.name] = factor_relative_score

            # print("This is country_scores", country_scores)
            # print("This is relative scores", user_relative_scores)

            userCountryScores = []
            userCountryScoresD = {}
            for y in UserScoreEnum:
                # To deal with no data for that countries factor score
                if country_scores[y.name] is not None:
                    userCountryScoreT = user_relative_scores[y.name] * country_scores[y.name]
                    #print("country", countryCode)
                    #print("This is userCountryScoreT", userCountryScoreT)
                else:
                    # When the value is NULL, sets the value to 0
                    userCountryScoreT = 0

                userCountryScores.append(userCountryScoreT)
                userCountryScoresD[y.name] = userCountryScoreT


            ## For Temperature
            user_temp = getattr(current_travel, "pref_user_temp")
            journey_start = getattr(current_travel, "journey_start")
            countryScore = MonthlyTemperatures.query.get(countryCode)
            # This is needed as the fields in the monthly temps has temperatures as: 'february_temp', 'december_temp'
            # However in the User Country it is stored just as a month
            journey_start_country = f"{journey_start}_temp"
            try:
                # country_temp is referring to the temperature of the country for the given user month
                country_temp = getattr(countryScore, journey_start_country)
            except AttributeError:
                countryScore = YearlyTemperatures.query.get(countryCode)
                country_temp = getattr(countryScore, "yearly_temp")
            if country_temp is None:
                # If theres no data for that month for the country
                # Use the yearly temperature data
                missing_monthly_temps += 1
                countryScore = YearlyTemperatures.query.get(countryCode)
                country_temp = getattr(countryScore, "yearly_temp")
                temps[countryCode] = country_temp
            else:
                temps[countryCode] = country_temp
                pass

            temp_difference = user_temp - country_temp
            # Squares the difference
            temp_difference = temp_difference * temp_difference
            temp_differences_squared[countryCode] = temp_difference

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

            for t in UserCountryScoreEnum:
                # adds the value for the factor score, using the value in the Enumerator of the UserCountryScore table
                # e.g. the first run of the loop, t.value = water_sports_score
                # and userCountryScoresD[t.name] = value of the dictionary for water_sports score
                setattr(current_country, t.value, userCountryScoresD[t.name])

    calculateTempScores(travelID, countryCodes, temps, temp_differences_squared)

    # sets the total score
    for countryCode in countryCodes:
        current_country = UserCountryScore.query.get((current_user.id, travelID, countryCode))
        allScores = []
        for factor in UserCountryScoreEnum:
            x = getattr(current_country, factor.value)
            allScores.append(x)

        temp_score = getattr(current_country, "temp_score")
        allScores.append(temp_score)

        total_score_for_country = sum(allScores)
        setattr(current_country, "total_score", total_score_for_country)

    db.session.commit()


def userCountryScore(travelID, countryCodes):
    try:
        # Sets the current travel to the UserTravelScore of the user with primary key values
        # user_id as the current user id and travel id key as the travel id passed into the function
        current_travel = UserTravelScore.query.get((current_user.id, travelID))
    except (sqlite3.IntegrityError, sqlalchemy.exc.IntegrityError) as e:
        print(e)

    prev_countries = getattr(current_travel, "prev_countries")

    try:
        # Tries to calculate country scores
        calculateCountryScores(travelID, countryCodes)
    except ValueError:
        # If the countries have already been added...
        # Just go straight to sorting the countries as they are already in the database
        pass

    # Runs the sortCountries function to get a list of the countries in an ordered format
    sortedCountries = sortCountries(travelID)

    return sortedCountries


def userQuestionAnswer(questionID, answerValue, travelID):
    question = getQuestion(questionID)
    answer = getAnswer(questionID, answerValue)
    questionType = question.get("questionType")
    answersType = question.get("answersType")
    questionAnswered = False
    now = datetime.now()

    try:
        # Tries to get a users possible travel record
        current_travel = UserTravelScore.query.get((current_user.id, travelID))
    except (sqlite3.IntegrityError, sqlalchemy.exc.IntegrityError) as e:
        print("This is E", e)

    if current_travel == None:
        # if the user has not travelled yet
        # Creates a new record for them
        new_user_travel = UserTravelScore(user_id=current_user.id,
                                          travel_id=travelID,
                                          date_added=datetime.date(now),
                                          questions_answered="",
                                          prev_countries=None,
                                          travelling_time=0,
                                          journey_start="",
                                          pref_user_activity="",
                                          pref_user_temp=0,
                                          num_travellers=0,
                                          water_sports_user_score=10,
                                          winter_sports_user_score=10,
                                          culture_user_score=10,
                                          nature_user_score=10,
                                          safety_user_score=0,
                                          budget_user_score=0,
                                          pop_density_user_score=0)
        db.session.add(new_user_travel)
        db.session.commit()

        # sets the current_travel to a query of user's newly created record
        current_travel = UserTravelScore.query.get((current_user.id, travelID))

    y = getattr(current_travel, 'questions_answered')
    # splits the string at each comma to get a list containing the question ID of the questions answered
    questionsAnsweredArray = y.split(',')
    for questionA in questionsAnsweredArray:
        if questionA == "":
            pass
        else:
            if int(questionID) == int(questionA):
                questionAnswered = True
                break

    # If the question hasn't been answered
    if questionAnswered == False:
        if questionType == "Integer" or answersType == "Integer":
            print("This is an integer question")
            answers = getAnswers(questionID)
            modifiersX = answers[0]
            modifiers = modifiersX.get("modifiers")
            toModify = modifiers[0].get("modifier")
            x = getattr(current_travel, toModify)
            setattr(current_travel, toModify, x + int(answerValue))

        elif questionType == "Multiple Choice":
            print("This is a Multiple Choice Question")
            # Modifies the values of the user's score
            for modifier in answer.get("modifiers"):
                # For every modifier in the modifiers of this answer
                if questionAnswered == False:
                    # checks again if the question is answered
                    toModify = modifier.get("modifier")
                    modificationBy = modifier.get("value")
                    # Gets the attribute name in the database of the modifier
                    x = getattr(current_travel, toModify)
                    if type(x) == int:
                        print("This is an integer answer")
                        # Changes the fields value by the modification
                        setattr(current_travel, toModify, x + modificationBy)
                    else:
                        # If the type of the value we are changing is not an int
                        # Sets the attribute to the modification value as opposed to adding
                        setattr(current_travel, toModify, modificationBy)

        elif answersType == "Integer+":
            # print("The is a special integer question")
            pref_user_activity = getattr(current_travel, "pref_user_activity")
            top_activity_score = pref_user_activity + "_user_score"
            x = getattr(current_travel, top_activity_score)
            factor1 = getattr(current_travel, "water_sports_user_score")
            factor2 = getattr(current_travel, "winter_sports_user_score")
            factor3 = getattr(current_travel, "culture_user_score")
            factor4 = getattr(current_travel, "nature_user_score")
            allFactorNames = ["water_sports_user_score",
                              "winter_sports_user_score",
                              "culture_user_score",
                              "nature_user_score"]

            for factor in allFactorNames:
                if factor == top_activity_score:
                    print("This is the top factor")
                    initialValue = getattr(current_travel, top_activity_score)
                    x = int(answerValue)
                    value = x/10 * initialValue
                    setattr(current_travel, top_activity_score, value+10)
                else:
                    # When it's not the highest factor...
                    initialValue = getattr(current_travel, factor)
                    x = int(answerValue)
                    value = ((10-(x/10))/3) * 10
                    setattr(current_travel, factor, value+10)

        # Adds the question to the user's questions answered
        current_travel.questions_answered = current_travel.questions_answered + (str(questionID) + ",")

        db.session.commit()

        # Sets the question to answered
        questionAnswered = True

    else:
        print("This question has been answered")
