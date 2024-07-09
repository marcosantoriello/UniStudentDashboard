import sqlite3
import os
import logging
from flask import Flask, g, render_template, request, redirect, Flask, flash

# TO CHANGE!!
DATABASE = './data/exams.sqlite'

app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    print('Connecting to database...', flush=True)
    """app.config["DATABASE"] access the flask app configuration value DATABASE"""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    with open('./data/schema.sql') as f:
        conn.executescript(f.read())
    print('Table created!', flush=True)
    return conn


def get_db():
    """If it doesn't exists, it opens a new db connection"""
    print('Opening database...', flush=True)
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def create_app():
    db = get_db()
    cursor = db.cursor()


@app.teardown_appcontext
def close_db(error):
    """Close the database at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def index():
    db = get_db()
    # just for testing purposes
    db.execute('INSERT into exam (title, cfu) values (?, ?)',
               ["Analisi Matematica", 6])
    res = db.execute('SELECT * FROM exam')
    res.row_factory = lambda _, x: {'id': x[0], 'title': x[1], 'cfu': x[2]}
    exams = res.fetchall()
    return render_template("index.html", exams=exams)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
