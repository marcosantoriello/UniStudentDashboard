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
    # if the db hasn't been populated yet
    if conn.execute('SELECT * from exam').fetchone() is None:
        with open('./data/populate.sql') as f:
            conn.executescript(f.read())
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


def calculate_arithmetic_average(exams) -> float:
    total_grades = sum(exam['grade'] for exam in exams)
    total_exams = len(exams)
    return total_grades / total_exams


def calculate_weighted_average(exams: list) -> float:
    total_cfu = sum(exam['cfu'] for exam in exams)
    total_grades_cfu = sum(exam['grade'] * exam['cfu'] for exam in exams)
    return total_grades_cfu / total_cfu


def calculate_graduation_grade(exams) -> float:
    weighted_average = calculate_weighted_average(exams)
    weight_one_hundred_and_ten = weighted_average * 110 / 30
    return weight_one_hundred_and_ten


@app.route('/')
def index():
    db = get_db()
    # just for testing purposes
    res = db.execute('SELECT * FROM exam')
    res.row_factory = lambda _, x: {'id': x[0], 'title': x[1], 'cfu': x[2], 'grade': x[3], 'passed': x[4]}
    exams = res.fetchall()
    arithmetic_average = calculate_arithmetic_average(exams)
    weighted_average = calculate_weighted_average(exams)
    graduation_grade = calculate_graduation_grade(exams)
    return render_template("index.html", exams=exams, arithmetic_average=arithmetic_average,
                           weighted_average=weighted_average, graduation_grade=graduation_grade)

@app.route('/new', methods=["GET, POST"])
def new():
    if request.method == "POST":
        print('In progress...', flush=True)
        # todo: note creation
        return render_template('new_exam.html')
    return render_template('new_exam.html')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
