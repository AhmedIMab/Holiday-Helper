import json
import os
import sqlite3
import sqlalchemy.exc
from .models import Note, User, Country, UserCountry, UserTravelScore
from flask_login import login_required, current_user
from . import db
from .collectionStream import CollectionStream


def getQuestions():
    print("Function is running")

    # print(os.getcwd())
    # print(os.path.join("\\website\\static\\test2.json"))
    filename = (os.getcwd() + os.path.join('\\website\\static\\test2.json'))
    # print(filename)

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

    if questionAnswered == True:
        print("This question has been answered", {questionID})
    else:
        print("Not answered")

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







def nextQuestionID(travelID):
    questions = getQuestions()
    # first filter will ask the questions which have not been answered
    # by applying a not to the return of isQuestionAnswered
    # second filter will make sure only mandatory questions are asked
    # x is the current element the method is looking at (filter)
    # questionsStream = CollectionStream(questions).stream()\
    #     .filter(lambda x:not(isQuestionAnswered(1, x.get("questionID"))))\
    #     .filter(lambda x:x.get("mandatory") == True)\
    #     .sort(lambda x:x.get("questionID")).first()

    questionsStream = questions
    questionsStream = filter(lambda x:not(isQuestionAnswered(1, x.get("questionID"))), questionsStream)
    questionsStream = filter(lambda x:x.get("mandatory") == True, questionsStream)
    questionsStream = sorted(questionsStream, key=lambda x:x.get("questionID"))

    if len(questionsStream) == 0:
        questionsStream = questions
        questionsStream = filter(lambda x:x.get("mandatory") == False, questionsStream)
        questionsStream = filter(lambda x: not(isQuestionAnswered(1, x.get("questionID"))), questionsStream)
        questionsStream = filter(lambda x:haveRequirementsBeenMet(travelID, x.get("questionID")), questionsStream)
        questionsStream = sorted(questionsStream, key=lambda x:x.get("questionID"))
        # questionsStream = questionsStream[0]

        if len(questionsStream) == 0:
            return 1
        else:
            questionsStream = questionsStream[0]
            return questionsStream.get("questionID")

    else:
        questionsStream = questionsStream[0]
        return questionsStream.get("questionID")


    print(questionsStream)


    # if questionsStream == None:
    #     # This will only run when their are no questions left or test2.json is empty/no questions to begin with
    #     # filter and get the non mandatory questions
    #     # also filtering questions they have answered as they may answer a question and this will loop
    #     # questionsStream = CollectionStream(questions).stream()\
    #     #     .filter(lambda x:x.get("mandatory") == False) \
    #     #     .filter(lambda x: not(isQuestionAnswered(1, x.get("questionID"))))\
    #     #     .filter(lambda x:haveRequirementsBeenMet(travelID, x.get("questionID"))) \
    #     #     .sort(lambda x:x.get("questionID"))\
    #     #     .first()
    #
    #     print(questionsStream)
    #
    #     if questionsStream == None:
    #         return 1
    #     else:
    #         return questionsStream.get("questionID")
    #
    # else:
    #     return questionsStream.get("questionID")


def getMandatoryQuestions():
    questions = getQuestions()
    mandatoryQuestions = CollectionStream(questions).filter(lambda x:x.get("mandatory") == True).collect()
    #print(len(mandatoryQuestions))
    #print(mandatoryQuestions)
    return mandatoryQuestions



#getMandatoryQuestions()

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


def questionAnswered(current_travel, questionID):
    # every time their is current travel...
    # Checks if the answer is in the users current answered questions
    print("Question Answered Function Is Running")

    print("Question Answered Function Is Running")
    print(questionAnswered)
    return questionAnswered




def userQuestionAnswer(questionID, answerValue, travelID):
    question = getQuestion(questionID)
    answerIntegerValue = int(answerValue)
    print("The answer as an integer is: ", answerIntegerValue)
    answer = getAnswer(questionID, answerValue)
    answerI = getAnswer(questionID, answerIntegerValue)
    questionType = question.get("questionType")




    questionAnswered = False
    #print(current_user.id)
    #print(travelID)

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
                                          budget_user_score=0,
                                          final_travel_cost=0)
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
            setattr(current_travel, toModify, x + answerIntegerValue)

            # if questionID == 1:
            #     # Hard coded as the first question will ALWAYS be num travellers
            #     # Avoid this if in the next questions?
            #     print("This is the first question")
            #     print(int(answerValue))
            #
            #     x = getattr(current_travel, "num_travellers")
            #     print(x)
            #     setattr(current_travel, "num_travellers", x + answerIntegerValue)

        elif questionType == "Multiple Choice":
            print("This is a Multiple Choice Question")
            # Modifies the values of the user's score
            for modifier in answer.get("modifiers"):
                if questionAnswered == False:
                    toModify = modifier.get("modifier")
                    modificationBy = modifier.get("value")
                    print(modificationBy)
                    print(type(modificationBy))
                    # Gets the attribute name in the database of the modifier
                    x = getattr(current_travel, toModify)
                    print(x)
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








    # try:
    #     new_user_travel = UserTravelScore(user_id=current_user.id,
    #                                       prev_countries=None,
    #                                       travelling_time=0,
    #                                       num_travellers=0,
    #                                       water_sports_user_score=0,
    #                                       winter_sports_user_score=0,
    #                                       culture_user_score=0,
    #                                       safety_user_score=0,
    #                                       budget_user_score=0,
    #                                       final_travel_cost=0)
    #     db.session.add(new_user_travel)
    #     db.session.commit()
    # except (sqlite3.IntegrityError, sqlalchemy.exc.IntegrityError) as e:
    #     print("User has already travelled")
    #     user_travel = UserTravelScore.query().filter(UserTravelScore.travel_id == travelID)
    #     print(user_travel)
    #
    # for modifier in answers.get("modifiers"):
    #     toModify = modifier.get("modifier")
    #     modificationBy = modifier.get("value")
    #     print(type(toModify))
    #     print(toModify)
    #     print(type(modificationBy))
    #     print(modificationBy)
    #     x = getattr(new_user_travel, toModify)
    #     setattr(new_user_travel, toModify, x + modificationBy)
    #     db.session.commit()













