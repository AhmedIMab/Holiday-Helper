from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date, Boolean
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from . import Base


class User(Base, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True)
    password = Column(String(255))
    first_name = Column(String(255))
    user_type = Column(Integer)
    countries = relationship('UserCountry', backref='user')
    travel_score = relationship('UserTravelScore', backref='user')


class Country(Base):
    __tablename__ = 'country'

    country_code = Column(String(3), primary_key=True)
    country_name = Column(String(150), unique=True)

    # Relationships for SQLAlchemy
    # uselist is needed so that the objects are not returned as a list but the actual related table object
    sport = relationship('Sport', backref='Country', uselist=False)
    cost = relationship('Cost', backref='Country', uselist=False)
    cultural_value = relationship('CulturalValue', backref='Country', uselist=False)
    nature = relationship('Nature', backref='Country', uselist=False)
    safety = relationship('Safety', backref='Country', uselist=False)
    population_density = relationship('PopulationDensity', backref='Country', uselist=False)


class UserCountry(Base):
    __tablename__ = 'user_country'

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    country_code = Column(String(3), ForeignKey('country.country_code'), primary_key=True)
    date_added = Column(Date)
    rating = Column(Integer)


class Sport(Base):
    __tablename__ = 'sport'

    country_code = Column(String(3), ForeignKey('country.country_code'), primary_key=True)
    water_sports_score = Column(Float)
    winter_sports_score = Column(Float)


class Safety(Base):
    __tablename__ = 'safety'

    country_code = Column(String(3), ForeignKey('country.country_code'), primary_key=True)
    safety_score = Column(Float)


class Cost(Base):
    __tablename__ = 'cost'

    country_code = Column(String(3), ForeignKey('country.country_code'), primary_key=True)
    cost_score = Column(Float)


class CulturalValue(Base):
    __tablename__ = 'cultural_value'

    country_code = Column(String(3), ForeignKey('country.country_code'), primary_key=True)
    heritage_score = Column(Float)


class CountryDailyCost(Base):
    __tablename__ = 'country_daily_cost'

    country_code = Column(String(3), ForeignKey('country.country_code'), primary_key=True)
    daily_cost = Column(Float)


class YearlyTemperatures(Base):
    __tablename__ = 'yearly_temperatures'

    country_code = Column(String(3), ForeignKey('country.country_code'), primary_key=True)
    yearly_temp = Column(Float)


class MonthlyTemperatures(Base):
    __tablename__ = 'monthly_temperatures'

    country_code = Column(String(3), ForeignKey('country.country_code'), primary_key=True)
    january_temp = Column(Float)
    february_temp = Column(Float)
    march_temp = Column(Float)
    april_temp = Column(Float)
    may_temp = Column(Float)
    june_temp = Column(Float)
    july_temp = Column(Float)
    august_temp = Column(Float)
    september_temp = Column(Float)
    october_temp = Column(Float)
    november_temp = Column(Float)
    december_temp = Column(Float)


class Nature(Base):
    __tablename__ = 'nature'

    country_code = Column(String(3), ForeignKey('country.country_code'), primary_key=True)
    nature_score = Column(Float)


class PopulationDensity(Base):
    __tablename__ = 'population_density'

    country_code = Column(String(3), ForeignKey('country.country_code'), primary_key=True)
    pop_density_score = Column(Float)


class CovidRestrictions(Base):
    __tablename__ = 'covid_restrictions'

    country_code = Column(String(3), ForeignKey('country.country_code'), primary_key=True)
    covid_colour = Column(String(5))


class UserTravelScore(Base):
    __tablename__ = 'user_travel_score'

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    travel_id = Column(Integer, primary_key=True)
    date_added = Column(Date)
    questions_answered = Column(String(255))
    prev_countries = Column(Boolean)
    travelling_time = Column(Integer)
    journey_start = Column(String(15))
    covid_feature = Column(Boolean)
    num_travellers = Column(Integer)
    pref_user_activity = Column(String(25))
    pref_user_temp = Column(Integer)
    water_sports_user_score = Column(Integer)
    winter_sports_user_score = Column(Integer)
    culture_user_score = Column(Integer)
    nature_user_score = Column(Integer)
    safety_user_score = Column(Integer)
    budget_user_score = Column(Integer)
    pop_density_user_score = Column(Integer)


class UserCountryScore(Base):
    __tablename__ = 'user_country_score'

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    travel_id = Column(Integer, primary_key=True)
    country_code = Column(String(3), ForeignKey('country.country_code'), primary_key=True)
    water_sports_score = Column(Float)
    winter_sports_score = Column(Float)
    culture_score = Column(Float)
    nature_score = Column(Float)
    temp_score = Column(Float)
    safety_score = Column(Float)
    budget_score = Column(Float)
    pop_density_score = Column(Float)
    total_score = Column(Float)
    final_travel_cost = Column(Float)