from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        # queries the database to get the first name where the email is the same as the email of the request
        user = User.query.filter_by(email=email).first()
        if user:
            # check password hash is a method in the module werkzeug.security
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

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    # Redirects to the endpoint login in the file
    # So the user can login again/into another user
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sigh_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            # You can 'flash' a message to the user if their are any messages to send
            # via the built-in flask flash method
            flash('Email must be greater than 3 characters', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character', category='error')
        elif password1 != password2:
            # The backslash escapes the issue of clashing speech marks and apostrophes
            flash('Passwords don\'t match. Please try again', category='error')
        elif len(password1) < 7:
            flash('Password is too short. Please try to make it longer', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created successfully!', category='success')
            # Sends the user to the homepage as they have passed all the error checks
            return redirect(url_for('views.home'))

    # Runs when its a get request and displays the page for signing up
    return render_template("sign_up.html", user=current_user)