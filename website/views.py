import sqlite3
import sqlalchemy.exc
from flask import Blueprint, render_template, request, flash, jsonify, url_for, redirect
from flask_api import status
import flask_sqlalchemy
from flask_login import login_required, current_user
from .models import Note, User, Country, UserCountry
from . import db
import json
from datetime import datetime
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



@views.route("/travelID", methods=["GET"])
@login_required
def newTravel():
    newTravelID = getNewTravelID()
    return jsonify(newTravelID)



@views.route("/journeys", methods=["GET"])
@login_required
def journey():
    countries = Country.query.all()
    AllCountries = {}
    for country in countries:
        AllCountries[country.country_code] = country.country_name

    x = select(UserTravelScore)\
            .where(UserTravelScore.user_id == current_user.id)
    result = db.session.connection().execute(x)
    result = result.fetchall()
    travels = []
    for travel in result:
        num_country_scores = 0
        travelID = travel[1]
        dateAdded = travel[2]
        dateString = dateAdded.strftime("%d/%m/%Y")
        # To find if the current journey is complete, check...
        # if all 197 countries have been added as that is the only guaranteed common factor for all completed travels
        # Cannot use questions answered as number of questions each user gets may be different
        countryX = select(UserCountryScore)\
            .where(UserCountryScore.user_id == current_user.id, UserCountryScore.travel_id == travelID)
        result_country = db.session.connection().execute(countryX)
        result_countries = result_country.fetchall()
        if countryX is None:
            print("Incomplete")
            travels.append((travelID, dateString, {'Status': 'Incomplete'}))
        else:
            for country_score in result_countries:
                num_country_scores += 1
            # If there are 197 records / 197 country scores as there are 197 countries in the database
            # consider this a complete travel
            if num_country_scores == 197:
                highestCountryScoreX = select(UserCountryScore)\
                    .where(UserCountryScore.user_id == current_user.id, UserCountryScore.travel_id == travelID)\
                    .order_by(UserCountryScore.total_score.desc())
                result_best_countries = db.session.connection().execute(highestCountryScoreX)
                result_all_countries = result_best_countries.fetchall()
                result_top_country = result_all_countries[0][2]
                result_top_country_name = AllCountries[result_top_country]
                print(result_top_country_name)
                travels.append((travelID, dateString, {'Top Country': result_top_country_name}))
            else:
                # This else will only run if there is at least one country score, otherwise the first else will catch it
                # As the code that adds countries only ever adds all countries, there might have been a database error
                print("Incomplete - possible server error")
                travels.append((travelID, dateString, {'Status': 'Incomplete'}))





    print(travels)


    return render_template("journeys.html", user=current_user, journeys=travels)



@views.route("/noTravel", methods=["GET"])
@login_required
def noTravel():
    return render_template("NoTravel.html", user=current_user)


@views.route("/questions/<travelID>", methods=["GET"])
@login_required
def questionsPage(travelID):
    return render_template("questions.html", user=current_user, travelID=travelID)


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
        # By the country with country code index of x[0]
        # x[1] is the original second part of the tuple and x[2] is the 3rd part
        ranked_countries_UF = list(map(lambda x: (AllCountries[x[0]], x[1], x[2]), ranked_countries))
        current_travel = UserTravelScore.query.get((current_user.id, travelID))
        num_travellers = current_travel.num_travellers
        travelling_time = current_travel.travelling_time
        user_travel_details.append(travelID)
        user_travel_details.append(num_travellers)
        user_travel_details.append(travelling_time)
        print("THIS IS ALL COUNTRIES", AllCountries)
        print("This is rankedCountriesUF", ranked_countries_UF)
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


@views.route("/userQuestionAnswer", methods=["POST"])
@login_required
def userAnswer():
    userAnswerResponse = json.loads(request.data)
    questionID = userAnswerResponse.get("questionID")
    answerID = userAnswerResponse.get("answerID")
    travelID = userAnswerResponse.get("travelID")

    userQuestionAnswer(questionID, answerID, travelID)

    return jsonify({}), status.HTTP_200_OK



@views.route("/api/questions/", methods=["GET"])
@login_required
def AllQuestions():
    data = getQuestions()

    return jsonify(data)



@views.route("/api/questions/nextQuestion/<travelID>", methods=["GET"])
@login_required
def nextQuestion(travelID):
    questionID = nextQuestionID(travelID)
    question = getQuestion(questionID)

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


@views.route('/countries', methods=['GET', 'POST'])
@login_required
def countries():
    countries = Country.query.all()
    countriess = []
    for country in countries:
        countriess.append({country.country_code: country.country_name})


    print(countriess)

    return render_template("countries.html", user=current_user, countries=countriess)


@views.route('/usercountries', methods=['GET', 'POST'])
@login_required
def addCountry():
    if request.method == "POST":
        try:
            now = datetime.now()
            country = json.loads(request.data)
            country_code = country.get("countryCode")
            new_user_country = UserCountry(user_id=current_user.id,
                                           country_code=country_code,
                                           date_added=datetime.date(now),
                                           rating=0)
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





