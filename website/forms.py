from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, PasswordField, EmailField, TextAreaField
from wtforms.validators import InputRequired, Length, EqualTo


class LoginForm(FlaskForm):
    email = EmailField('Email Address', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])


class SignupForm(FlaskForm):
    email = EmailField('Email Address', validators=[InputRequired()])
    firstName = StringField('First Name', validators=[InputRequired(), Length(min=2)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=7), EqualTo('confirm_pass', message="Passwords don\'t match. Please try again")])
    confirm_pass = PasswordField('Confirm Password', validators=[InputRequired(), Length(min=7)])


class GuestLoginForm(FlaskForm):
    firstName = StringField('First Name (Optional)')


class FeedbackForm(FlaskForm):
    email = EmailField('Email Address', validators=[InputRequired()])
    firstName = StringField('First Name (Optional)')
    message = TextAreaField('How did you find using our app?', render_kw={"rows": 5})
    to_implement = TextAreaField('What would you like to see implemented into the app next?',
                                 render_kw={"rows": 5})


