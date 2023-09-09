from datetime import datetime
from flask import Flask, jsonify, request, render_template, url_for, redirect, session, request
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    login_required,
    logout_user,
    current_user,
)
from werkzeug.security import check_password_hash, generate_password_hash

from RunningStats import app, db, app_dash
from RunningStats.forms import RegisterForm, LoginForm
from RunningStats.models import UserInfo, Token
# from RunningStats.models import UserInfo

from stravalib.client import Client

import pickle
import time
from functions.StravaStats import StravaStats
from RunningStats.dashboard import plotlyDashboard
import os


loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = "userLogin"

client = Client()

accessToken = ""

try:
    MY_STRAVA_CLIENT_ID, MY_STRAVA_CLIENT_SECRET = open('client.secret').read().strip().split(',')
except:
    MY_STRAVA_CLIENT_ID = os.getenv("MY_STRAVA_CLIENT_ID")
    MY_STRAVA_CLIENT_SECRET = os.getenv("MY_STRAVA_CLIENT_SECRET")

@loginManager.user_loader
def load_user(user_id):
    return UserInfo.query.get(int(user_id))


# Members Login Route
@app.route("/login", methods=["POST", "GET"])
def userLogin():

    form = LoginForm()

    if form.validate_on_submit():
        user = UserInfo.query.filter_by(username=form.username.data).first_or_404()

        session['user'] = user.id

        if check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("index"))
        else:
            return "Incorrect Password"

    return render_template("login.html", form=form)


@app.route("/register", methods=["POST", "GET"])
def userRegister():
    error = None
    form = RegisterForm()

    if not form.username.data:
        error = "Username is required"
    elif not form.password.data:
        error = "Password is required"

    if error is None:
        new_user = UserInfo(
            username=form.username.data,
            password=generate_password_hash(form.password.data),
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("userLogin"))
        except:
            return "There was an error creating your account"

    return render_template("register.html", form=form)



@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for("userLogin"))




@app.route('/')
def index():
    # return ("Hello world!")
    return render_template("index.html")

@app.route('/strava')
def strava():
      
    url = client.authorization_url(client_id=MY_STRAVA_CLIENT_ID, redirect_uri='http://127.0.0.1:5000/authorization', scope=['read_all','profile:read_all','activity:read_all','activity:write'])
    # url = client.authorization_url(client_id=MY_STRAVA_CLIENT_ID, redirect_uri='https://running-stats-d49636ca3c9f.herokuapp.com/authorization', scope=['read_all','profile:read_all','activity:read_all','activity:write'])

    return render_template(
            "strava.html", stravaUrl=url
        )



@app.route('/authorization', methods=["GET"])
def auth():

    if request.method == "GET":

        CODE = request.args.get("code")
        # CODE = request.args.get('code')

        token_response = client.exchange_code_for_token(client_id=MY_STRAVA_CLIENT_ID, client_secret=MY_STRAVA_CLIENT_SECRET, code=CODE)

        session["userId"] = client.get_athlete().id # Does this exhaust the token?

        session['access_token'] = token_response['access_token']
        session['refresh_token'] = token_response['refresh_token']

        token_info = Token(id=int(session['user']), access_token=session['access_token'], 
                           refresh_token=session['refresh_token'])
        old_token = Token.query.filter_by(id=int(session['user'])).first_or_404()

        return redirect(url_for("render_dashboard"))

        try:
            db.session.delete(old_token)
            db.session.commit()
        except:
            pass 
        try:
            db.session.add(token_info)
            db.session.commit()
            return redirect(url_for("render_dashboard"))
        except:
            return "There was an error opening the dashboard."
    

    # return redirect("/dashboard")
    # return redirect("https://www.strava.com/oauth/authorize")


@app.route('/plotly_dashboard') 
def render_dashboard():
    plotlyDashboard(session["access_token"], session["userId"])
    return redirect('/dash')


@app.route('/dashboard')
def dashboard():

    try:

        return "404"
        CLIENT_ACCESS = session['access_token']
        newClient = Client(access_token=CLIENT_ACCESS)

        #activityList = strava.getActivities(client)

        strava = StravaStats(newClient, 0)

        allStats = strava.allStats

        streak = allStats["streak"]
        avg_pace = allStats["avg_pace"]
        shortest = allStats["shortest"]
        longest = allStats["longest"]
        average = allStats["average"]
        median = allStats["median"]
        mode = allStats["mode"]
        modeOccurance = allStats["modeOccurance"]
        startDate = allStats["startDate"]
        endDate = allStats["endDate"]
        totalDays = allStats["totalDays"]
        totalRunningDays = allStats["totalRunningDays"]
        percentDays = allStats["percentDays"]
        totalSeconds = allStats["totalSeconds"]
        totalMinutes = allStats["totalMinutes"]
        totalHours = allStats["totalHours"]
        totalOfDaysRunning = allStats["totalOfDaysRunning"]
        totalMiles = allStats["totalMiles"]
 
        athlete = newClient.get_athlete()
        nameString = f'{athlete.firstname} {athlete.lastname}'

        
        return render_template(
            "dashboard.html", average_pace=avg_pace, streak=streak, name=nameString,
            shortest=shortest, longest=longest, average=average, median=median, mode=mode, 
            modeOccurance=modeOccurance, startDate=startDate, endDate=endDate, 
            totalDays=totalDays, totalRunningDays=totalRunningDays, percentDays=percentDays, 
            totalSeconds=totalSeconds, totalMinutes=totalMinutes, totalHours=totalHours, 
            totalOfDaysRunning=totalOfDaysRunning, totalMiles=totalMiles
        )
    
    except:
        return ("Sorry we've encountered an error.")