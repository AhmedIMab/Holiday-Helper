# '.' imports from the current package (website __init__.py right now)
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    countries = db.relationship('UserCountry')
    travel_score = db.relationship('UserTravelScore')


class Country(db.Model):
    country_code = db.Column(db.String(3), primary_key=True)
    country_name = db.Column(db.String(150), unique=True)
    #sport = db.relationship('Country')


class UserCountry(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    country_code = db.Column(db.String(3), db.ForeignKey('country.country_code'), primary_key=True)
    data_added = db.Column(db.Date)
    rating = db.Column(db.Integer)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    # User.id will reference the id field in the User table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Sport(db.Model):
    country_code = db.Column(db.String(3), db.ForeignKey('country.country_code'), primary_key=True)
    # Add min/max?
    water_sports_score = db.Column(db.Integer)
    winter_sports_score = db.Column(db.Integer)


class Safety(db.Model):
    country_code = db.Column(db.String(3), db.ForeignKey('country.country_code'), primary_key=True)
    safety_score = db.Column(db.Integer)


class Cost(db.Model):
    country_code = db.Column(db.String(3), db.ForeignKey('country.country_code'), primary_key=True)
    cost_score = db.Column(db.Integer)


class CountryDailyCost(db.Model):
    country_code = db.Column(db.String(3), db.ForeignKey('country.country_code'), primary_key=True)
    daily_cost = db.Column(db.Integer)


class CulturalValue(db.Model):
    country_code = db.Column(db.String(3), db.ForeignKey('country.country_code'), primary_key=True)
    heritage_score = db.Column(db.Integer)


class CovidRestrictions(db.Model):
    country_code = db.Column(db.String(3), db.ForeignKey('country.country_code'), primary_key=True)
    covid_colour = db.Column(db.String(5))


class UserTravelScore(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    travel_id = db.Column(db.Integer, primary_key=True)
    questions_answered = db.Column(db.String)
    questions_skipped = db.Column(db.String)
    # country_code = db.Column(db.String(3), db.ForeignKey('country.country_code'), primary_key=True)
    prev_countries = db.Column(db.Boolean)
    travelling_time = db.Column(db.Integer)
    covid_feature = db.Column(db.Boolean)
    num_travellers = db.Column(db.Integer)
    water_sports_user_score = db.Column(db.Integer)
    winter_sports_user_score = db.Column(db.Integer)
    culture_user_score = db.Column(db.Integer)
    safety_user_score = db.Column(db.Integer)
    budget_user_score = db.Column(db.Integer)
    final_travel_cost = db.Column(db.Integer)

















