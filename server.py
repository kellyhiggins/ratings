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

# We are explicitly specifying GET, despite its default status, to differentiate from POST
# on same URL
@app.route('/signup', methods=["GET"])
def display_signup_form():
    """displays form for users to sign up for a login"""

    return render_template('signup.html')

@app.route('/signup', methods=["POST"])
def process_signup_form():
    """Processes signup once user provides username and password."""

    email = request.form.get("email")
    password = request.form.get("password")
# We create a possible user object to query if the user's email is in the User Class or user table.
# We query by email, since this will be unique to each user, and return the first.
# If this user doesn't exist yet, it will return none. (.one() throws an error if row doesn't exist or is >1)
    possible_user = User.query.filter_by(email=email).first()
# If this exists in the user table (or is not None)
    if possible_user:
        flash("You already have an account...lucky you!")
# Add user to user database
    else:
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash("You have successfully enlisted in The Judgemental Eye!")
# with both of these possibilities, we send user to log in.
    return redirect('/login')

# We are explicitly specifying GET, despite its default status, to differentiate from POST
# on same URL
@app.route('/login', methods=["GET"])
def display_login_form():
    """Displays form for users to login"""

    return render_template('login.html')

@app.route('/login', methods=["POST"])
def process_login():
    """Process login from User, redirect to homepage"""

    email = request.form.get("email")
    password = request.form.get("password")
# We create a possible user object to query if the user's email is in the User Class or user table.
# We query by email, since this will be unique to each user, and return the first.
    possible_user = User.query.filter_by(email=email).first()

# If possible_user exists in user table and the password matches the record:
# If possible_user doesn't exist, python's "quick fail" tendency will not check the second condition
    if possible_user and possible_user.password == password:
    # add user_id to session variable 

        session['user_id'] = possible_user.user_id
        flash("You are logged in!")
        # takes user to the users app route, not an html page
        return redirect('/users')
    else:
        flash("Incorrect login, dummy. Try harder.")
        return redirect('/login')

@app.route('/logout')
def logout():
    """Removes user_id from the session"""

    # del session['user_id']
    session.pop('user_id', None)
    flash("You have successfully logged out.")
    return redirect('/')
    # this queries for username in db, if username matches pwd, log them in
    # session variables! to keep user logged in, add user id (fetched from db to session)

# update base.html to show flashed messages

# after user logs in, redirect them to home page

# logging out - remove user_id from sessin 
# flash message like "Logged Out"
# redirect user to homepage
@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Return page showing details of a user. Show age, zipcode, movies rated, scores."""
    # Querying user table to get user object
    user = User.query.get(user_id)
    # getting ratings from user object since the tables are joined in the data model by db.relationship
    ratings = user.ratings
    return render_template('user_details.html', user=user, ratings=ratings)



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
