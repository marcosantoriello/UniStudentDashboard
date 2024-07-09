import sqlite3
import os
from flask import flask, g, render_template, request, redirect, Flask

# TO CHANGE!!
DATABASE = '/data/exams.db'

app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    """app.config["DATABASE"] access the flask app configuration value DATABASE"""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    """If it doesn't exists, it opens an new db connection"""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Close the database at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def index():
    db = get_db()
    