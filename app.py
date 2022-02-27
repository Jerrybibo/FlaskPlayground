# Python scripts for learning Flask.
# Base material referenced from:
# * Flask Documentation - https://flask.palletsprojects.com/en/2.0.x/
# * pythonbasics.org - https://pythonbasics.org/what-is-flask-python/
# Written by Jerrybibo, 2022.

from flask import Flask, render_template, request, escape

app = Flask(__name__)


@app.route('/')
def hello_world():
    """
    Basic function to return raw HTML content. Served on the root URL.
    WARN It seems like it's not a good idea to reference raw variables directly in returned HTML.
    WARN This is due to the possibility of XSS exploits created from such implementation.
    WARN Escape them with escape() as imported from the flask package.
    :return: Raw HTML data to be rendered to the user
    """
    return '<h1>Hello World!</h1>'


@app.route('/index')
def variable_replacement():
    """
    Displays a website with "Hello <name>!", where <name> is passed in as a "name" HTTP GET parameter.
    With PyCharm, a link to the HTML file referenced will appear next to the method header.
    :return: HTML data generated from render_template()
    """
    name = request.args.get('name')
    return render_template('index.html', title='Welcome', username=name)


@app.route('/if')
def if_clause():
    """
    Checks whether the "name" HTTP GET parameter is equal to "Jerry".
    :return: HTML data generated from render_template()
    """
    name = request.args.get('name')
    return render_template('if.html', title='Are you Jerry?', username=name)


if __name__ == '__main__':
    app.run()
