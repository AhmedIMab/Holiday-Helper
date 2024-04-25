import sqlite3
import sqlalchemy.exc
from flask import Blueprint, render_template, request, flash, jsonify, url_for, redirect
from flask_login import login_required, current_user
from .models import User, Country, UserCountry
from . import db_session, NUM_COUNTRIES
import json
from datetime import datetime
import os
from website.questionHandler import *
import traceback
import time

views = Blueprint('views', __name__)


@views.route("/usercountries", methods=["DELETE"])
@login_required
def delete_country():
    country = json.loads(request.data)
    countryCode = country.get('countryCode')
    country = UserCountry.query.get((current_user.id, countryCode))
    if country:
        if country.user_id == current_user.id:
            db = db_session()
            db.delete(country)
            db.commit()

    return jsonify({})

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route("/travelID", methods=["GET"])
@login_required
def newTravel():
    x = select(UserTravelScore) \
        .where(UserTravelScore.user_id == current_user.id)
    db = db_session()
    result = db.connection().execute(x)
    result = result.fetchall()
    # print("THIS IS RESULT", result)

    travelIDs = []
    try:
        for travel in result:
            travelID = travel[1]
            travelIDs.append(travelID)

        newTravelID = max(travelIDs) + 1
    except ValueError:
        # When the user hasn't travelled yet
        newTravelID = 1

    return jsonify(newTravelID)


@views.route("/journeys", methods=["GET"])
@login_required
def journey():
    start = time.time()
    countries = Country.query.all()
    AllCountries = {}
    for country in countries:
        AllCountries[country.country_code] = country.country_name

    x = select(UserTravelScore)\
            .where(UserTravelScore.user_id == current_user.id)
    db = db_session()
    result = db.connection().execute(x)
    result = result.fetchall()
    travel_sessions = []
    for travel in result:
        num_country_scores = 0
        travelID = travel[1]
        dateAdded = travel[2]
        dateString = dateAdded.strftime("%d/%m/%Y")
        # To find if the current journey is complete, check...
        # if all 197 countries have been added as that is the only guaranteed common factor for all completed travels
        # Cannot use questions answered as number of questions each user gets may be different
        countries_X = select(UserCountryScore)\
            .where(UserCountryScore.user_id == current_user.id, UserCountryScore.travel_id == travelID)
        result_countries = db.connection().execute(countries_X)
        result_travels = result_countries.fetchall()
        if result_travels == []:
            # This will run when the user has not completed the questionnaire
            travel_sessions.append((travelID, dateString, {'Status': 'Incomplete'}))
        else:
            for country_score in result_travels:
                num_country_scores += 1
            # If there are 197 records / 197 country scores as there are 197 countries in the database
            # consider this a complete travel
            if num_country_scores == NUM_COUNTRIES:
                # Selects all countries with the user id and travel id matching
                # and orders by descending so the first one is the optimal country
                country_scores_query = select(UserCountryScore)\
                    .where(UserCountryScore.user_id == current_user.id, UserCountryScore.travel_id == travelID)\
                    .order_by(UserCountryScore.total_score.desc())
                result_all_countries = db.connection().execute(country_scores_query).fetchall()
                # As result_all_countries returns a list of tuples
                # And each tuple is in the same structure as the database table UserCountryScore
                # The third column (index 2) is the country code
                # So result_top_country will be the first tuple's country code
                top_country = result_all_countries[0][2]


                country_codes_to_filter = []
                for result in result_all_countries:
                    country_codes_to_filter.append(result[2])

                # Uses the function 'filterPrevCountries' to avoid showing the top country which is one they visited
                filtered_country_codes = filterPrevCountries(country_codes_to_filter, travelID)
                top_filtered_country_code = filtered_country_codes[0]
                top_country_name = AllCountries[top_filtered_country_code]

                # print(travelID, top_country_name)

                travel_sessions.append((travelID, dateString, {'Top Country': top_country_name}))
            else:
                # This else will only run if there is at least one country score, otherwise the first if will catch it
                # As the code that adds countries only ever adds all countries, there has likely been a database error
                print("Incomplete - possible server error")
                travel_sessions.append((travelID, dateString, {'Status': 'Incomplete'}))

    print("This is how long it currently takes to load journeys:", time.time()-start)
    return render_template("journeys.html", user=current_user, journeys=travel_sessions)


@views.route("/noTravel", methods=["GET"])
@login_required
def noTravel():
    return render_template("no_travel.html", user=current_user)


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
        # map function is used to replace country codes with country names for user convenience
        # x[0] is the country code
        # the first part of the tuple (x[0]) will be replaced with the country name
        # By the country with country code index of x[0]
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

    except AttributeError:
        print("ERROR", traceback.format_exc())
        user_travel_details.append(0)
        user_travel_details.append(1)
        return redirect(url_for('views.noTravel'))


@views.route("/userQuestionAnswer", methods=["POST"])
@login_required
def userAnswer():
    userAnswerResponse = json.loads(request.data)
    questionID = userAnswerResponse.get("questionID")
    answerID = userAnswerResponse.get("answerID")
    travelID = userAnswerResponse.get("travelID")

    userQuestionAnswer(questionID, answerID, travelID)

    return jsonify({}), 200


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

    if question is None:
        return f"A question with questionID: {questionID} was not found", 406
    else:
        return question, 200


@views.route("/api/questions/<questionID>", methods=["GET"])
@login_required
def questions(questionID):
    question = getQuestion(questionID)
    if question is None:
        return f"A question with questionID: {questionID} was not found", 404

    else:
        return question, 200


@views.route('/countries', methods=['GET', 'POST'])
@login_required
def countries():
    countries = Country.query.all()
    countries_list = []
    for country in countries:
        countries_list.append({country.country_code: country.country_name})

    return render_template("countries.html", user=current_user, countries=countries_list)


@views.route('/usercountries', methods=['GET', 'POST'])
@login_required
def addCountry():
    print("Running this hehehe")
    if request.method == "POST":
        print("POST request made hehhehe")
        db = db_session()
        try:
            now = datetime.now()
            country = json.loads(request.data)
            country_code = country.get("countryCode")
            new_user_country = UserCountry(user_id=current_user.id,
                                           country_code=country_code,
                                           date_added=datetime.date(now),
                                           rating=0)
            db.add(new_user_country)
            # the commit will confirm that the changes are added together
            # ensuring consistency
            db.commit()
        except Exception as e:
            print("This is the exception when adding a country that was already there:", e)
            db.rollback()
            # return f"This user has already added this country {country_code}", 500
            return jsonify({"error": "Country already added"}), 400

    return render_template("countries.html", user=current_user)





