# /flaskr/db.py
# Woo databases!!
# SQLite databases are used for this project to store users and posts.
# Do note that SQLite does not scale well due to its inherent qualities; but for small applications it should be fine.
# Reference: https://flask.palletsprojects.com/en/2.0.x/tutorial/database/
import sqlite3

# click ("Command Line Interface Creation Kit") creates helper commands for initializing our database.
import click
from flask import current_app, g
from flask.cli import with_appcontext


def init_app(app):
    """
    Registers the relevant functions with the specific Flask application instance.
    :param app: Flask app object
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def get_db():
    """
    Establishes connection to SQLite database.
    :return: SQLite connection object
    """
    # g is a special object unique for each request, which stores cross-function data. ("the application context")
    # If a DB connection has already been made, it won't reconnect to the SQLite DB.
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],  # current_app is a special object that points to the Flask application.
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # sqlite3.Row tells SQLite to return rows that behave like dicts. (column names = dict keys)
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """
    Closes the database connection if any exists.
    :param e:
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """
    Initializes a SQLite database using schema.sql.
    """
    db = get_db()
    # Opens schema.sql as relative to the flaskr package, then executes the commands in the SQL file on SQLite
    with current_app.open_resource('schema.sql') as schema_file:
        db.executescript(schema_file.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """
    Initializes a SQLite database using schema.sql.
    """
    init_db()
    click.echo('Initialized the database.')
