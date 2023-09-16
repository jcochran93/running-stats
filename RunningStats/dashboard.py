from RunningStats import app_dash
import pandas as pd
from dash import html, dcc, Input, Output, callback
import plotly.express as px
from stravalib import Client
from functions.StravaStats import StravaStats, StravaActivities
from RunningStats.models import UserInfo, Token, RunningData
from sqlalchemy import desc
from datetime import datetime, timedelta, date
from RunningStats import db
from flask import session
import json
import dash_bootstrap_components as dbc

summaryStringList = []
dataset = pd.DataFrame()

try:
    testAthleteId = int(open('testUser.secret').read().strip())
except:
    testAthleteId = None

stravaStats = None
athleteIdGlobal = 0
nameString = ""

app_dash.config.suppress_callback_exceptions = True

app_dash.layout = html.Div(children="Loading...")


def checkDbForActivityData(athleteId):
    
    results = RunningData.query.filter_by(athlete_id=athleteId).order_by(RunningData.start_date_local.desc()).first()

    try:
        latestDate = results.start_date_local
    except:
        latestDate = None

    return latestDate

def addActivitiesToDb(stravaRunsList, athleteId):

    activities = stravaRunsList

    for activity in activities:

        dist = str(activity.distance).strip(" meter")
        dist = float(dist) / 1609.34

        duplicate = RunningData.query.filter_by(name=activity.name, athlete_id=athleteId, 
                                  distance=dist, start_date_local=activity.start_date_local, moving_time=activity.moving_time.total_seconds()).first()

        if (duplicate == None):

            newActivity = RunningData(name=activity.name, athlete_id=athleteId, 
                                  distance=dist, start_date_local=activity.start_date_local, moving_time=activity.moving_time.total_seconds())
            try:
                db.session.add(newActivity)
                db.session.commit()
            except:
                continue

def getActivitiesFromDb(athleteId):
    try:
        return RunningData.query.filter_by(athlete_id=athleteId).order_by(RunningData.start_date_local)
    except:
        return []

def plotlyDashboard(accessToken, athlete):
    CLIENT_ACCESS = accessToken
    athleteId = athlete or testAthleteId
    nameString = ""


    if (athlete != ""):
        latestDate = checkDbForActivityData(athleteId)
        newClient = Client(access_token=CLIENT_ACCESS)

        stravaRuns = StravaActivities(newClient)
        stravaRunsList = stravaRuns.getActivities(activityType="Run", afterDate=latestDate)
        stravaRunsList = stravaRuns.getActivities(activityType="Run")

        stravaStats = StravaStats(stravaRunsList)
        addActivitiesToDb(stravaRunsList, newClient.get_athlete().id)
        athlete = newClient.get_athlete()
        nameString = f'{athlete.firstname}'


    activities  = getActivitiesFromDb(athleteId)
    activities = [activity for activity in activities] 

    stravaStats = StravaStats(activities)

    nameString = nameString or "Test"

    dates = stravaStats.dailyDateList
 
    earliestDate = dates.min().date()
    latestDate = dates.max().date()

    card = []

    app_dash.layout = dbc.Container(
    [
        html.H1("Hello "+ nameString),
        html.Hr(), 
        dbc.Row([
            dbc.Col(html.H4(
        "Date Range: "), md=3)]),
        dbc.Row([
        dbc.Col(
        dbc.Input(id='startDate', value=dates.min().date(), type='date', class_name="col-xs-2"), md=2),
        dbc.Col(
        dbc.Input(id='endDate', value=dates.max().date(), type='date'), md=2)
        ]), 
        html.Br(),dbc.Container(
    getSummaryForDateRange(athleteId, earliestDate, latestDate)
        , id="summary")

    ])




@callback(
    Output(component_id='summary', component_property='children'),
    Input(component_id='startDate', component_property='value'),
    Input(component_id='endDate', component_property='value')
)
def update_output_div(start_date, end_date):
    athleteIdGlobal = session["userId"]

    return getSummaryForDateRange(athleteIdGlobal, start_date, end_date)

def getSummaryForDateRange(athleteId, startDate, endDate, stravaActivities=None):
    try:

        if (isinstance(startDate, str)):
            startDate = datetime.strptime(startDate, '%Y-%m-%d').date()
            endDate = datetime.strptime(endDate, '%Y-%m-%d').date()

        activities  = getActivitiesFromDb(athleteId)
        activities = [activity for activity in activities] 

        if(stravaActivities != None):
            activities = [activity for activity in stravaActivities] 

        stravaStats = StravaStats(activities)
        summaryStringList = stravaStats.summaryStringForRange(startDate, endDate)
        dates = stravaStats.getDailyDateList(stravaStats.runActivityList, startDate, endDate)
        miles = stravaStats.getDailyMilesList(stravaStats.runActivityList, startDate, endDate)
        dataset = pd.DataFrame({'dates': dates, 'miles': miles}, columns=['dates', 'miles'])
    except:
        return html.Div(children="Loading...")

    card = []

    for title, body in summaryStringList.items():
        card.append(dbc.Card(
        dbc.CardBody(
        [
            html.H4(title, className="card-title"),
            html.P(
                body,
                className="card-text",
            )
        ]
    )
    ))

    try:

        return dbc.Container([
        dbc.Row([
            dbc.Col(card[0], md=3),
            dbc.Col(card[1], md=3),
            dbc.Col(card[2], md=3),
            dbc.Col(card[3], md=3)
        ]),
        dbc.Row([
            dbc.Col(card[4], md=3),
            dbc.Col(card[5], md=3),
            dbc.Col(card[6], md=3),
            dbc.Col(card[7], md=3),
        ]),
        dbc.Row([
            dbc.Col(card[8], md=4),
            dbc.Col(card[9], md=4)
        ],class_name='justify-content-center'),
        dcc.Graph(id="scatterplot", figure=px.scatter(dataset, x='dates', y='miles'))
    ])
    except:
        return "Loading"


def getSummary(athleteId, startDate, endDate):
    try:

        if (isinstance(startDate, str)):
            startDate = datetime.strptime(startDate, '%Y-%m-%d').date()
            endDate = datetime.strptime(endDate, '%Y-%m-%d').date()

        activities  = getActivitiesFromDb(athleteId)
        activities = [activity for activity in activities] 
        stravaStats = StravaStats(activities)
        summaryStringList = stravaStats.summaryStringForRange(startDate, endDate)
    except:
        return html.Div(children="Loading...")
    
    return summaryStringList
