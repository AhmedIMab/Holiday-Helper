import sqlite3
import sqlalchemy.exc
from flask import Blueprint, render_template, request, flash, jsonify, url_for
from flask_api import status
import flask_sqlalchemy
from flask_login import login_required, current_user
from .models import Note, User, Country, UserCountry
from . import db
import json
import datetime
import os
from website.questionHandler import *



views = Blueprint('views', __name__)



@views.route('/notes', methods=['POST'])
@login_required
def add_note():
    if request.method == 'POST':
        # Converts the JSON coming from api.js into a python dictionary
        note = json.loads(request.data)
        # Accessing the note value field from the dictionary
        noteValue = note.get('noteValue')
        # print(noteValue)
        if len(noteValue) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=noteValue, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("notes.html", user=current_user)



@views.route('/notes', methods=['GET'])
@login_required
def get_notes():
    return render_template("notes.html", user=current_user)



@views.route("/usercountries", methods=["DELETE"])
@login_required
def delete_country():
    country = json.loads(request.data)
    countryCode = country.get('countryCode')
    print(countryCode)
    country = UserCountry.query.get((current_user.id, countryCode))
    print(country)
    if country:
        if country.user_id == current_user.id:
            db.session.delete(country)
            db.session.commit()
            print("Hello")

    return jsonify({})



# DELETE used as more standard way - RESTful
@views.route('/notes', methods=['DELETE'])
@login_required
def delete_note():
    # we are taking the data from the POST request (from api.js)
    # loads it as a JSON object / Python dictionary
    note = json.loads(request.data)
    # then we access the noteId attribute (sent with the POST request)
    noteId = note.get('noteId')
    # then look for the note which has that id
    note = Note.query.get(noteId)
    # make sure it exists
    if note:
        # if the user that's signed in actually owns the note - stops other users deleting each others notes
        if note.user_id == current_user.id:
            # delete the note
            db.session.delete(note)
            db.session.commit()

    # return an empty response
    return jsonify({})


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    #email = current_user
    #user = User.query.filter_by(email=email).first()
    return render_template("home.html", user=current_user)



@views.route("/test", methods=["GET"])
@login_required
def test():
    countries = Country.query.all()
    countriess = []
    for country in countries:
        countriess.append({country.country_code: country.country_name})

    return render_template("TEST.html", user=current_user, countries=countriess)



# @views.route("/api/answerquestion/", methods=["POST"])
# @login_required
# def questions():
#     if request.method == "POST":
#         #print(app.static_folder)
#         filename = os.path.join(app.static_folder, "test2.json")
#         f = open(filename, 'r')
#         data = json.load(f)
#
#         userAnswer = json.loads(request.data)
#         answerID = userAnswer.get("answerID")
#         questionID = userAnswer.get("questionID")
#
#
#     return


# @views.route("/api/questions/<questionID>", methods=["GET"])
# @login_required
# def questions(questionID):
#     question = getQuestion(questionID)
#     if question == None:
#         return f"A question with questionID: {questionID} was not found", status.HTTP_404_NOT_FOUND
#
#     else:
#         return question, status.HTTP_200_OK

# @views.route("/api/questions/nextQuestionAnswers", methods=["GET"])
# @login_required
# def answers():
#     questionID = nextQuestionID()
#     answers = getAnswers(questionID)
#     print(answers)
#
#     if answers == None:
#         return f"A question with questionID: {questionID} was not found", status.HTTP_404_NOT_FOUND
#
#     else:
#         return jsonify(answers), status.HTTP_200_OK






@views.route("/countrySuggestions", methods=["GET"])
@login_required
def suggestCountries():
    return render_template("TEST.html", user=current_user)



@views.route("/testCountryUser", methods=['GET', 'POST'])
@login_required
def testCountry():
    testResponse = json.loads(request.data)
    print(testResponse)
    travelID = testResponse.get("travelID")
    countryCode = testResponse.get("countryCode")
    userCountryScore(travelID, countryCode)
    return testResponse


@views.route("userQuestionAnswer", methods=["POST"])
@login_required
def userAnswer():
    userAnswerResponse = json.loads(request.data)
    questionID = userAnswerResponse.get("questionID")
    answerID = userAnswerResponse.get("answerID")
    print(questionID)
    print(answerID)

    userQuestionAnswer(questionID, answerID, 1)

    return jsonify({}), status.HTTP_200_OK


@views.route("/api/questions/", methods=["GET"])
@login_required
def AllQuestions():
    #print(app.static_folder)
    data = getQuestions()

    return jsonify(data)





@views.route("/api/questions/nextQuestion", methods=["GET"])
@login_required
def nextQuestion():
    travelID = 1
    questionID = nextQuestionID(travelID)
    question = getQuestion(questionID)
    print("THIS IS QUESTION ID in next question views", questionID)

    if question == None:
        return f"A question with questionID: {questionID} was not found", status.HTTP_406_NOT_ACCEPTABLE


    else:
        return question, status.HTTP_200_OK



@views.route("/api/questions/<questionID>", methods=["GET"])
@login_required
def questions(questionID):
    question = getQuestion(questionID)
    if question == None:
        # return render_template("TEST.html", user=current_user)
        return f"A question with questionID: {questionID} was not found", status.HTTP_404_NOT_FOUND

    else:
        return question, status.HTTP_200_OK




@views.route("/questions", methods=["GET"])
@login_required
def questionsPage():
    return render_template("questions.html", user=current_user)




@views.route('/countries', methods=['GET', 'POST'])
@login_required
def countries():
    countries = Country.query.all()
    countriess = []
    for country in countries:
        countriess.append({country.country_code: country.country_name})

    return render_template("countries.html", user=current_user, countries=countriess)


@views.route('/usercountries', methods=['GET', 'POST'])
@login_required
def addCountry():
    if request.method == "POST":
        try:
            country = json.loads(request.data)
            country_code = country.get("countryCode")
            new_user_country = UserCountry(user_id=current_user.id, country_code=country_code, data_added=datetime.datetime.now(), rating=0)
            db.session.add(new_user_country)
            # the commit will confirm that the changes are added together
            # ensuring consistency
            db.session.commit()
            print(country_code)
        except (sqlite3.IntegrityError, sqlalchemy.exc.IntegrityError) as e:
            print("Country already Added")
            # return f"This user has already added this country {country_code}", 500
            return f"This user has already added this country {country_code}", status.HTTP_400_BAD_REQUEST

    return render_template("countries.html", user=current_user)





