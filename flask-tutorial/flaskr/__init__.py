# flaskr/__init__.py
# The application factory script, __init__.py will also indicate that this directory is a package.
# Reference: https://flask.palletsprojects.com/en/2.0.x/tutorial/factory/
import os
from flask import Flask
from . import db


def create_app(test_config=None):
    """
    Application factory function.
    Returns a Flask object, and when run, displays a page at 127.0.0.1:5000/hello.
    """
    # Creates the Flask object; __name__ specifies the current module (flaskr) as the "base" of the project.
    app = Flask(__name__, instance_relative_config=True)

    # Sets default app configuration.
    app.config.from_mapping(
        SECRET_KEY='dev',  # todo Should be overridden with a random value on deployment.
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),  # Database directory
    )

    # Load instance config if it is not passed in
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # Check that the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Create a route to a simple page that says hello
    @app.route('/hello')
    def hello():
        return '<p>Hello world!</p>'

    # Register the init-db command and close_db function with the application instance
    db.init_app(app)

    # Be sure to return the object
    return app
