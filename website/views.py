import sqlite3
import sqlalchemy.exc
from flask import Blueprint, render_template, request, flash, jsonify, url_for, redirect, send_from_directory
from flask_login import login_required, current_user
from .models import User, Country, UserCountry
from . import db_session, NUM_COUNTRIES
import json
from datetime import datetime
import os
from website.questionHandler import *
import traceback
import time
from . import csrf
import functools

views = Blueprint('views', __name__)


def requires_user_types(user_types):
    def decorator(func):
        # This wraps decorator is to ensure that the functions name and other attributes aren't changed by the decorator
        @functools.wraps(func)
        def wrapper_requires_access_level(*args, **kwargs):
            if current_user.user_type not in user_types:
                flash("Guests cannot access this page", category='error')
                return redirect(url_for('views.landing'))
            else:
                # This is to ensure that the functions return values are lost
                return func(*args, **kwargs)
        return wrapper_requires_access_level
    return decorator


@views.route('/robots.txt', methods=['GET'])
def robots():
    print("Here we are!")
    print(os.getcwd() + 'website/')
    return send_from_directory(os.getcwd() + '/website/', 'robots.txt')


@views.route('/sitemap.xml', methods=['GET'])
def sitemap():
    print(os.getcwd() + 'website/')
    return send_from_directory(os.getcwd() + '/website/', 'sitemap.xml')


@views.route('/', methods=['GET', 'POST'])
def home():
    print("Welcome! Entered site on:", datetime.now())
    if current_user.is_authenticated and (current_user.user_type == 1 or current_user.user_type == 2):
        return render_template("home.html", user=current_user)
    else:
        return render_template("home.html", user=None)


@views.route('/about', methods=['GET'])
@csrf.exempt
def about():
    return render_template("about.html", user=current_user)


@views.route("/travelID", methods=["GET"])
@login_required
def newTravel():
    result = UserTravelScore.query.filter_by(user_id=current_user.id)

    travelIDs = []
    try:
        for travel in result:
            travelID = travel.travel_id
            travelIDs.append(travelID)

        newTravelID = max(travelIDs) + 1
    except ValueError:
        # When the user hasn't travelled yet
        newTravelID = 1

    return jsonify(newTravelID)


@views.route("/journeys", methods=["GET"])
@time_taken
@login_required
def journey():
    def find_journeys():
        prev_countries = UserCountry.query.filter_by(user_id=current_user.id).all()
        prev_countries_country_codes = [Country.query.filter_by(country_code=cc.country_code).first().country_code for cc in prev_countries]
        all_travel_sessions = UserTravelScore.query.filter_by(user_id=current_user.id).all()

        travel_sessions = []
        for travel in all_travel_sessions:
            travelID = travel.travel_id
            dateAdded = travel.date_added
            dateString = dateAdded.strftime("%d/%m/%Y")
            # To find if the current journey is complete, check...
            # if all 197 countries have been added as that is the only guaranteed common factor for all completed travels
            # Cannot use questions answered as number of questions each user gets may be different
            result_travel_countries = UserCountryScore.query.filter_by(user_id=current_user.id,
                                                                       travel_id=travelID).all()
            if len(result_travel_countries) == 0:
                # This will run when the user has not completed the questionnaire
                travel_sessions.append((travelID, dateString, travel.prev_countries,  {'Status': 'Incomplete'}))
            else:
                if len(result_travel_countries) == NUM_COUNTRIES:
                    # 0 means does not want to include previous countries
                    # 1 means want to include previous countries
                    if travel.prev_countries == 0:
                        # print("They wanted to filter the countries in this travel session", travelID)

                        # Selects countries with the user id and travel id matching
                        # and orders by descending so the first one is the optimal country
                        # Will only get as many rows as the number of previous countries plus one so that it will be more efficient
                        # Whilst also displaying the top country which isn't previously visited if they want the filtering
                        result_all_countries = UserCountryScore.query \
                            .filter_by(user_id=current_user.id, travel_id=travelID) \
                            .order_by(UserCountryScore.total_score.desc()) \
                            .limit(len(prev_countries) + 1) \
                            .all()


                        # As a default option
                        top_country = result_all_countries[0]

                        for country_y in result_all_countries:
                            if country_y.country_code not in prev_countries_country_codes:
                                top_country = country_y
                                break

                    else:
                        top_country = UserCountryScore.query \
                            .filter_by(user_id=current_user.id, travel_id=travelID) \
                            .order_by(UserCountryScore.total_score.desc()) \
                            .first()

                    top_country_name = Country.query.filter_by(country_code=top_country.country_code).first().country_name

                    travel_sessions.append((travelID, dateString, travel.prev_countries, {'Top Country': top_country_name}))
                else:
                    # This else will only run if there is at least one country score, otherwise the first if will catch it
                    # As the code that adds countries only ever adds all countries, there has likely been a database error
                    print("Incomplete - possible server error")
                    travel_sessions.append((travelID, dateString, travel.prev_countries, {'Status': 'Incomplete'}))
        return travel_sessions

    travel_sessions_list = find_journeys()

    return render_template("journeys.html", user=current_user, journeys=travel_sessions_list)


@views.route("/noTravel", methods=["GET"])
@login_required
def noTravel():
    return render_template("no_travel.html", user=current_user)


@views.route("/questions/<travelID>", methods=["GET"])
@login_required
def questionsPage(travelID):
    return render_template("questions.html", user=current_user, travelID=travelID)


@views.route("/validateTravelID/<travelID>", methods=["GET"])
@csrf.exempt
@login_required
def validateTravelID(travelID):
    try:
        current_travel = UserTravelScore.query.get((current_user.id, travelID))
    except (sqlite3.IntegrityError, sqlalchemy.exc.IntegrityError) as e:
        print("Travel Invalid")
        current_travel = None

    if current_travel is None:
        return jsonify({'valid': False, 'message': "Invalid travel ID"}), 404
    else:
        return jsonify({'valid': True}), 200


@views.route("/suggestions/<travelID>", methods=["GET"])
@csrf.exempt
@login_required
def suggestions(travelID):
    countries = Country.query.all()
    AllCountries = {}
    for country in countries:
        AllCountries[country.country_code] = country.country_name

    user_travel_details = []
    try:
        print("\nIn the suggestions and just about to call userCountryScore function\n")
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
        user_travel_details.append(current_travel.prev_countries)
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
@csrf.exempt
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
@csrf.exempt
@login_required
@requires_user_types([1,2])
def countries():
    countries = Country.query.all()
    countries_list = []
    for country in countries:
        countries_list.append({country.country_code: country.country_name})

    return render_template("countries.html", user=current_user, countries=countries_list)


@views.route('/usercountries', methods=['GET', 'POST'])
@csrf.exempt
@login_required
def addCountry():
    if request.method == "POST":
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
        except (sqlite3.IntegrityError, sqlalchemy.exc.IntegrityError) as e:
            # print("This is the exception when adding a country that was already there:", e)
            db.rollback()
            # return f"This user has already added this country {country_code}", 500
            return jsonify({"error": "Country already added"}), 400

    return render_template("countries.html", user=current_user)


@views.route("/usercountries", methods=["DELETE"])
@login_required
@csrf.exempt
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



