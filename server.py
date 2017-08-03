"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, redirect, request, flash, session, url_for
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    
    return render_template("homepage.html")

@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route("/registration")
def registration_form():
    """Show registration form to user."""

    return render_template("registration_form.html")

@app.route("/process_form", methods=["POST"])
def add_new_user():
    """Verifies new users and adds them to database."""

    user = request.form.get("email")
    password = request.form.get("password")
    new_user = User(email=user, password=password)

    if not User.query.filter_by(email=user).first():
        db.session.add(new_user)
        db.session.commit()
        return redirect("/users")
    else:
        flash("This email is already associated with an account. Please log in")
        return redirect("/login_form")


@app.route("/login_form")
def login_form():
    """Show login form to user."""

    return render_template("login_form.html")

@app.route("/login_user", methods=["POST"])
def login_user():
    """Verify user login."""

    user_email = request.form.get("email")
    user_password = request.form.get("password")
    # user = User(email=user_email, password=user_password)

    if User.query.filter_by(email=user_email).first():
        true_user = User.query.filter_by(email=user_email).first()
        if true_user.password == user_password:
            session['email'] = user_email
            flash("Logged in as {}".format(user_email))
            return redirect('/')
        else:
            flash("I'm sorry. That is an incorrect password.")
            return redirect("/login_form")
    else:
        flash("I'm sorry. This email does not have an existing account.")
        return redirect("/registration")

@app.route("/logout")
def logout():
    """Log user out."""
    session['email'] = None
    flash("You are now logged out.")
    return redirect("/")

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    # app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=8000, host='0.0.0.0')
