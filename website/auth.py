from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db_session
from flask_login import login_user, login_required, logout_user, current_user
from .forms import LoginForm, SignupForm

auth = Blueprint('auth', __name__)
# Update this if werkzeug changes its hash
old_method = '$sha256'
new_hash_method = 'scrypt'


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
                # return redirect(url_for('auth.reset_password'))
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
    logout_user()
    # Redirects to the endpoint login in the file
    # So the user can login again/into another user
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sigh_up():
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
                new_user = User(email=email, first_name=first_name, password=generate_password_hash(password, method=new_hash_method))
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


# THIS IS TEMPORARY TO MIGRATE PASSWORDS!
# //@auth.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user is None:
            flash('No email registered', category='error')
        elif user.first_name != first_name:
            flash('Names do not match. Please try again', category='error')
        elif len(password) < 7:
            flash('Password is too short. Please make it longer')
        else:
            new_password = generate_password_hash(password, method=new_hash_method)
            user.password = new_password
            db = db_session()
            db.commit()
            login_user(user, remember=True)
            flash('Account password changed successfully!', category='success')
            db.close()
            return redirect(url_for('views.home'))

    return render_template("reset_password.html", user=current_user)

















