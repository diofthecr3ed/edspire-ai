from flask import (
    Flask, 
    flash, 
    jsonify, 
    redirect, 
    render_template, 
    request, 
    session
)

import datetime
import os
import requests
from collections import OrderedDict, defaultdict


from flask import redirect, render_template, request, session, flash
from functools import wraps

from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import (
    default_exceptions, 
    HTTPException, 
    InternalServerError
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename


# Configure application
app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
Session(app)


app.jinja_env.filters['zip'] = zip


@app.route("/leaderboard", methods=["GET", "POST"])
def leaderboard():
    usernames = ['Parth', 'Krrish', 'Kenan', 'Aadi']
    levels = [10, 23, 44, 33]
    return render_template("leaderboard.html",
        usernames= usernames,
        levels= levels
        )


@app.route("/history", methods=["GET", "POST"])
def history():
    data = get_historydata()
    return render_template("history.html", names = data)


@app.route("/index", methods=["GET", "POST"])
def index():
    data = get_dict()
    return render_template("dashboard.html", names=data)


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    courseID, course, questionID, question = get_quizdata()
    return render_template("test.html", courseID = courseID, 
        course = course, questionID = questionID, 
        question = question)



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        if not request.form.get('username'):
            print('USERNAME NOT PROVIDED')
            return render_template("login.html")
        if not request.form.get('password'):
            print('PASSWORD NOT PROVIDED')
            return render_template("login.html")
        print(request.form.get('password'))
        return redirect('/index')



@app.route("/register", methods=["GET", "POST"])
def signup():
    return render_template("register.html")
@app.route("/diagnosis", methods=["GET", "POST"])
def diagnosis():
    return render_template("diagnosis.html")
@app.route("/pretest", methods=["GET", "POST"])
def pretest():
    return render_template("range.html")



def get_dict():
    data = {}
    data['MATH 51'] = 'Linear Algebra, Multivariable Calculus and Modern Applications.'
    data['EE 374'] = 'Blockchain Foundations.'
    data['MATH 53'] = 'Differential Equations.'
    return data


def get_historydata():
    data = {}
    data['Test 1'] = [(datetime.datetime(2022, 5, 17)), ('1-5')]
    data['Test 2'] = [(datetime.datetime(2023, 5, 17)), ('5-7')]
    data['Test 3'] = [(datetime.datetime(2024, 5, 17)), ('7-10')]
    return data


def get_quizdata():
    courseID = 'EE374'
    course = 'Blockchain Foundations'
    question = 'Compute the correlation coefficient of the following 2-D data points: (2,1), (2,2), (0,1).'
    questionID = 'Question 1'
    return courseID, course, questionID, question


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
