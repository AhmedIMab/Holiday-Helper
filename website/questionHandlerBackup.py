import json
import os
import sqlite3

import sqlalchemy.exc

from .models import Note, User, Country, UserCountry, UserTravelScore
from flask_login import login_required, current_user
from . import db


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


def nextQuestionID():
    return "1"


def getAnswers(questionID):
    question = getQuestion(questionID)
    print(type(question))
    answers = question.get("answers")
    print(answers)
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
    answerIntegerValue = int(answerValue)
    answer = getAnswer(questionID, answerValue)
    answerI = getAnswer(questionID, answerIntegerValue)
    questionType = question.get("questionType")
    print("IT PASSED THE ANSWER")
    print(answer)
    print(answerI)

    if answer == None:
        print("This is an integer question/answer hasn't been written in JSON file yet")




    questionAnswered = False
    #print(current_user.id)
    #print(travelID)

    try:
        #print("TTTTTTTTT")
        #print(current_user.id)
        #print(travelID)
        current_travel = UserTravelScore.query.get((current_user.id, travelID))

        #print(current_travel)

    except (sqlite3.IntegrityError, sqlalchemy.exc.IntegrityError) as e:
        pass

    if current_travel == None:
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
        #print("TESTESTEST")
        #print(current_user.id)
        #print(travelID)
        current_travel = UserTravelScore.query.get((current_user.id, travelID))
        #print(current_travel)


    # every time their is current travel...
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
        # Modifies the values of the user's score
        for modifier in answer.get("modifiers"):
            if questionAnswered == False:
                toModify = modifier.get("modifier")
                modificationBy = modifier.get("modifyBy")
                #print(type(toModify))
                #print(toModify)
                #print(type(modificationBy))
                #print(modificationBy)
                # Gets the attribute name in the database of the modifier
                x = getattr(current_travel, toModify)
                # Changes the fields value by the modification
                setattr(current_travel, toModify, x + modificationBy)

        # Adds the question to the user's questions answered
        current_travel.questions_answered = (questionID + ",")
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
    #     modificationBy = modifier.get("modifyBy")
    #     print(type(toModify))
    #     print(toModify)
    #     print(type(modificationBy))
    #     print(modificationBy)
    #     x = getattr(new_user_travel, toModify)
    #     setattr(new_user_travel, toModify, x + modificationBy)
    #     db.session.commit()













