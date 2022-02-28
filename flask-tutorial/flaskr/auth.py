# /flaskr/auth.py
# Blueprint for authentication functions.

import functools
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

# Creates a Blueprint object named auth, associated with the flaskr project location
# All the defined routes below will have /auth prefixed (i.e., /register -> /auth/register)
bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.before_app_request
def load_logged_in_user():
    """
    Stores the currently logged-in user ID (obtained from SESSION) into the application context (g).
    """
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', user_id
        ).fetchone()


@bp.route('/register', methods=('GET', 'POST'))
def register():
    """
    Checks for POST calls to the register endpoint, then attempts to create a new user entry in database.
    :return: A redirect to the login page on success
    """
    # Look for POST request
    if request.method == 'POST':
        # Obtain username and password from POST request
        username, password = request.form['username'], request.form['password']
        # Establish connection to database
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        # If preliminary variable checks passes,
        if error is None:
            # Try to insert entry into user table
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password))
                )
            # If IntegrityError is thrown (username is a key), there must be a duplicate username
            except db.IntegrityError:
                error = f"User {username} is already registered."
            # If no explicitly caught error was thrown, direct to login page
            else:
                return redirect(url_for('auth.login'))

        # If there was an error, display to user
        flash(error)

    # Render the register HTML on GET request
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """
    Logs specified user in, if user exists in database, on POST request. Also stores user ID in SESSION on success.
    Similar implementation to register().
    :return: A redirect to the index page on success
    """
    if request.method == 'POST':
        username, password = request.form['username'], request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", username
        ).fetchone()  # Returns first result (None if not found); fetchall() returns list of all results

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            # Clear SESSION variable
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout', methods=('GET', 'POST'))
def logout():
    """
    Logs current user out by clearing SESSION.
    :return: A redirect to the index page
    """
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    """
    A decorator that allows for easy checks on whether a user is logged in. Wraps around original view function.
    More on decorators: https://realpython.com/primer-on-python-decorators/
    :param view: View function to be decorated
    :return: Wrapped view function
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        # If the user is logged in, returns the view as intended; if not, redirects to the login page.
        if g.users is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
