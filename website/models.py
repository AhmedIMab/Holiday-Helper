# '.' imports from the current package (website __init__.py right now)
from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    # notes = db.relationship('Note')
    countries = db.relationship('UserCountry')
    travel_score = db.relationship('UserTravelScore')


class Country(db.Model):
    country_code = db.Column(db.String(3), primary_key=True)
    country_name = db.Column(db.String(150), unique=True)


class UserCountry(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    country_code = db.Column(db.String(3), db.ForeignKey('country.country_code'), primary_key=True)
    date_added = db.Column(db.Date)
    rating = db.Column(db.Integer)


class Sport(db.Model):
    country_code = db.Column(db.String(3), db.ForeignKey('country.country_code'), primary_key=True)
    water_sports_score = db.Column(db.Float)
    winter_sports_score = db.Column(db.Float)


class Safety(db.Model):
    country_code = db.Column(db.String(3), db.ForeignKey('country.country_code'), primary_key=True)
    safety_score = db.Column(db.Float)


class Cost(db.Model):
    country_code = db.Column(db.String(3), db.ForeignKey('country.country_code'), primary_key=True)
    cost_score = db.Column(db.Float)


class CulturalValue(db.Model):
    country_code = db.Column(db.String(3), db.ForeignKey('country.country_code'), primary_key=True)
    heritage_score = db.Column(db.Float)


class CountryDailyCost(db.Model):
    country_code = db.Column(db.String(3), db.ForeignKey('country.country_code'), primary_key=True)
    daily_cost = db.Column(db.Float)


class YearlyTemperatures(db.Model):
    country_code = db.Column(db.String(3), db.ForeignKey('country.country_code'), primary_key=True)
    yearly_temp = db.Column(db.Float)


class MonthlyTemperatures(db.Model):
    country_code = db.Column(db.String(3), db.ForeignKey('country.country_code'), primary_key=True)
    january_temp = db.Column(db.Float)
    february_temp = db.Column(db.Float)
    march_temp = db.Column(db.Float)
    april_temp = db.Column(db.Float)
    may_temp = db.Column(db.Float)
    june_temp = db.Column(db.Float)
    july_temp = db.Column(db.Float)
    august_temp = db.Column(db.Float)
    september_temp = db.Column(db.Float)
    october_temp = db.Column(db.Float)
    november_temp = db.Column(db.Float)
    december_temp = db.Column(db.Float)


class Nature(db.Model):
    country_code = db.Column(db.String(3), db.ForeignKey('country.country_code'), primary_key=True)
    nature_score = db.Column(db.Float)


class PopulationDensity(db.Model):
    country_code = db.Column(db.String(3), db.ForeignKey('country.country_code'), primary_key=True)
    pop_density_score = db.Column(db.Float)


class CovidRestrictions(db.Model):
    country_code = db.Column(db.String(3), db.ForeignKey('country.country_code'), primary_key=True)
    covid_colour = db.Column(db.String(5))


class UserTravelScore(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    travel_id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.Date)
    questions_answered = db.Column(db.String)
    prev_countries = db.Column(db.Boolean)
    travelling_time = db.Column(db.Integer)
    journey_start = db.Column(db.String(15))
    covid_feature = db.Column(db.Boolean)
    num_travellers = db.Column(db.Integer)
    pref_user_activity = db.Column(db.String(25))
    pref_user_temp = db.Column(db.Integer)
    water_sports_user_score = db.Column(db.Integer)
    winter_sports_user_score = db.Column(db.Integer)
    culture_user_score = db.Column(db.Integer)
    nature_user_score = db.Column(db.Integer)
    safety_user_score = db.Column(db.Integer)
    budget_user_score = db.Column(db.Integer)
    pop_density_user_score = db.Column(db.Integer)



class UserCountryScore(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    travel_id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(3), db.ForeignKey('country.country_code'), primary_key=True)
    # The score for the user * the countries water sports score
    water_sports_score = db.Column(db.Float)
    winter_sports_score = db.Column(db.Float)
    culture_score = db.Column(db.Float)
    nature_score = db.Column(db.Float)
    temp_score = db.Column(db.Float)
    safety_score = db.Column(db.Float)
    budget_score = db.Column(db.Float)
    pop_density_score = db.Column(db.Float)
    total_score = db.Column(db.Float)
    final_travel_cost = db.Column(db.Float)



















