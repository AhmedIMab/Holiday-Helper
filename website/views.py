import sqlite3
import sqlalchemy.exc
from flask import Blueprint, render_template, request, flash, jsonify, url_for, redirect
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

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)


# @views.route("/test", methods=["GET"])
# @login_required
# def test():
#     countries = Country.query.all()
#     countriess = []
#     for country in countries:
#         countriess.append({country.country_code: country.country_name})
#
#     return render_template("travelID.html", user=current_user, countries=countriess)

# @views.route("/api/answerquestion/", methods=["POST"])
# @login_required
# def questions():
#     if request.method == "POST":
#         #print(app.static_folder)
#         filename = os.path.join(app.static_folder, "questions.json")
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



@views.route("/travelSession", methods=["GET"])
@login_required
def travelsession():
    print("This is with a GET response!")
    return render_template("travelID.html", user=current_user)


@views.route("/noTravel", methods=["GET"])
@login_required
def noTravel():
    return render_template("NoTravel.html", user=current_user)


@views.route("/suggestions/<travelID>", methods=["GET"])
@login_required
def suggestions(travelID):
    countries = Country.query.all()
    AllCountries = {}
    for country in countries:
        AllCountries[country.country_code] = country.country_name


    user_travel_details = []
    try:
        ranked_countries = userCountryScore(travelID, AllCountries)
        # x[0] is the country code
        # the first part of the tuple (x[0]) will be replaced with the the country name
        # x[1] is the original second part of the tuple and x[2] is the 3rd part
        ranked_countries_UF = list(map(lambda x: (AllCountries[x[0]], x[1], x[2]), ranked_countries))
        current_travel = UserTravelScore.query.get((current_user.id, travelID))
        num_travellers = current_travel.num_travellers
        travelling_time = current_travel.travelling_time
        user_travel_details.append(travelID)
        user_travel_details.append(num_travellers)
        user_travel_details.append(travelling_time)
        return render_template("suggestions.html",
                               user=current_user,
                               best_countries=ranked_countries_UF,
                               user_travel=user_travel_details)

    except (AttributeError, sqlalchemy.exc.IntegrityError) as e:
        print("ERROR", e)
        user_travel_details.append(0)
        user_travel_details.append(1)
        return redirect(url_for('views.noTravel'))


# @views.route("/countrySuggestions", methods=["GET", "POST"])
# @login_required
# def suggestCountries():
#     if request.method == "POST":
#         travel_response = json.loads(request.data)
#         print(travel_response)
#         travelID = travel_response["travelID"]
#         print(travelID)
#         ranked_countries = sortCountries(travelID)
#         print("Hiii")
#         print(ranked_countries)
#         return render_template("suggestions.html", user=current_user, best_countries=ranked_countries)
#         # return render_template("suggestions.html", user=current_user)
#
#     print("we're here")
#     return render_template("travelID.html", user=current_user)




# @views.route("/testCountryUser", methods=['GET', 'POST'])
# @login_required
# def testCountry():
#     testResponse = json.loads(request.data)
#     #print(testResponse)
#     travelID = testResponse.get("travelID")
#     #countryCode = testResponse.get("countryCode")
#
#
#     #print("XXX")
#     #print(AllCountries)
#
#     countries = Country.query.all()
#
#     AllCountries = []
#     for country in countries:
#         #print(type(country))
#         AllCountries.append(country.country_code)
#
#     userSuggestions = userCountryScore(travelID, AllCountries)
#
#     return render_template("suggestions.html", user=current_user, best_countries=userSuggestions)
#


@views.route("userQuestionAnswer", methods=["POST"])
@login_required
def userAnswer():
    userAnswerResponse = json.loads(request.data)
    questionID = userAnswerResponse.get("questionID")
    answerID = userAnswerResponse.get("answerID")
    travelID = userAnswerResponse.get("travelID")
    print(questionID)
    print(answerID)

    userQuestionAnswer(questionID, answerID, travelID)

    return jsonify({}), status.HTTP_200_OK



@views.route("/api/questions/", methods=["GET"])
@login_required
def AllQuestions():
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





