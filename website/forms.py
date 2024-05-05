from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, PasswordField, EmailField
from wtforms.validators import InputRequired, Length, EqualTo

class LoginForm(FlaskForm):
    email = EmailField('Email Address', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])


class SignupForm(FlaskForm):
    email = EmailField('Email Address', validators=[InputRequired()])
    firstName = StringField('First Name', validators=[InputRequired(), Length(min=2)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=7), EqualTo('confirm_pass', message="Passwords don\'t match. Please try again")])
    confirm_pass = PasswordField('Confirm Password', validators=[InputRequired(), Length(min=7)])


