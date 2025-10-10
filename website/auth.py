from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, UserCountry, UserTravelScore, Sport, Cost, CulturalValue, MonthlyTemperatures
from .models import UserCountryScore, CountryDailyCost, Safety, Nature, PopulationDensity, YearlyTemperatures
from werkzeug.security import generate_password_hash, check_password_hash
from . import db_session
from flask_login import login_user, login_required, logout_user, current_user
from .forms import LoginForm, SignupForm, GuestLoginForm
import string
import random
from sqlalchemy import delete

auth = Blueprint('auth', __name__)
# Update this if werkzeug changes its hash

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate():
        email = form.email.data
        password = form.password.data
        # queries the database to get the first name where the email is the same as the email of the request
        user = User.query.filter_by(email=email).first()
        if user:
            # check password hash is a method in the module werkzeug.security
            try:
                check_password_hash(user.password, password)
            except ValueError as ve:
                flash('Using old hash method, please reset password', category='error')
                return render_template("login.html", user=current_user, form=form)
            if check_password_hash(user.password, password):
                flash('Login Successful', category='success')
                login_user(user, remember=True)
                # Redirects the user to the home page
                return redirect(url_for('views.home'))
            else:
                # Displays an incorrect password message
                flash('Incorrect password', category='error')
        else:
            # Displays an email does not exist message
            flash('Email does not exist', category='error')

    return render_template("login.html", user=current_user, form=form)


@auth.route('/logout')
@login_required
def logout():
    db = db_session()
    try:
        if current_user.user_type == 0:
            db.query(UserCountryScore).filter_by(user_id=current_user.user_id).delete()
            db.query(UserTravelScore).filter_by(user_id=current_user.user_id).delete()
            user = db.query(User).get(current_user.user_id)
            db.delete(user)
            db.commit()
    except Exception as e:
        db.rollback()
        print("Error deleting guest user:", e)
    finally:
        db.close()

    logout_user()
    return redirect(url_for('views.home'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignupForm()
    if request.method == 'POST':
        email = form.email.data
        first_name = form.firstName.data
        password = form.password.data

        if form.validate():
            user = User.query.filter_by(email=email).first()
            if user:
                # You can 'flash' a message to the user if there are any messages to send
                # via the built-in flask flash method
                flash('Email already exists', category='error')
            else:
                new_user = User(email=email, first_name=first_name, password=generate_password_hash(password), user_type=1)
                db = db_session()
                db.add(new_user)
                db.commit()
                login_user(new_user, remember=True)
                flash('Account created successfully!', category='success')
                # Sends the user to the homepage as they have passed all the error checks
                db.close()
                return redirect(url_for('views.home'))

    # Runs when it's a get request and displays the page for signing up
    return render_template("sign_up.html", user=current_user, form=form)


@auth.route('/guest-login', methods=['GET', 'POST'])
def guest_login():
    form = GuestLoginForm()
    if request.method == 'POST':
        firstName = form.firstName.data
        # Although currently guests can be created without much personal info (even none depending on their preference)
        # Validation is good practise for extensibility
        if form.validate():
            if len(firstName) == 0:
                firstName = "guest"
            test_password = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=12))
            guest_user = User(email="default@XYZ.com", first_name=firstName, password=generate_password_hash(test_password), user_type=0)
            db = db_session()
            db.add(guest_user)

            # Here we update the email to include the ID
            guest_user.email = "default" + str(guest_user.id) + "@XYZ.com"
            db.commit()

            login_user(guest_user, force=True, remember=True)
            flash('Guest logged in successfully!', category='success')
            print("Passed here!")
            db.close()
            return redirect(url_for('views.home'))

    return render_template("guest_login.html", user=current_user, form=form)

