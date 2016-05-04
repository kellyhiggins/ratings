"""Movie Ratings."""

import sqlalchemy
from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template('user_list.html', users=users)

@app.route('/signup')
def display_signup_form():
    """displays form for users to sign up for a login"""

    return render_template('signup.html')

@app.route('/signup', methods=["POST"])
def processes_signup_form():
    """Processes signup once user provides username and password."""

    email = request.form.get("email")
    password = request.form.get("password")

    possible_user = User.query.filter_by(email=email).all()

    if email in possible_user:
        flash("You already have an account!")
        redirect('/login')
    else:
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()


@app.route('/login')
def logging_in():
# add a login form and a route that shows the login form

# add a route that handles submission of the login
    # this queries for username in db, if username matches pwd, log them in
    # session variables! to keep user logged in, add user id (fetched from db to session)

# use Flask flash object to add a message like "logged in"
# update base.html to show flashed messages

# after user logs in, redirect them to home page

# logging out - remove user_id from sessin 
# flash message like "Logged Out"
# redirect user to homepage




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
