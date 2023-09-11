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

summaryStringList = []
dataset = pd.DataFrame()

try:
    testAthleteId = int(open('testUser.secret').read().strip())
except:
    testAthleteId = None

stravaStats = None
athleteIdGlobal = 0

app_dash.config.suppress_callback_exceptions = True

app_dash.layout = html.Div(children="Loading...")

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
    
    return html.Div([
        html.Div(children=summaryStringList[0]),
        html.Div(children=summaryStringList[1]),
        html.Div(children=summaryStringList[2]),
        html.Div(children=summaryStringList[3]),
        html.Div(children=summaryStringList[4]),
        html.Div(children=summaryStringList[5]),
        html.Div(children=summaryStringList[6]),
        html.Div(children=summaryStringList[7]),
        html.Div(children=summaryStringList[8]),
        html.Div(children=summaryStringList[9]),
        html.Div(children=summaryStringList[10])
    ])

def checkDbForActivityData(athleteId):
    
    results = RunningData.query.filter_by(athlete_id=athleteId).order_by(RunningData.start_date.desc()).first()

    try:
        latestDate = results.start_date
    except:
        latestDate = None

    return latestDate

def addActivitiesToDb(stravaRunsList, athleteId):

    activities = stravaRunsList

    for activity in activities:

        dist = str(activity.distance).strip(" meter")
        dist = float(dist) / 1609.34

        duplicate = RunningData.query.filter_by(name=activity.name, athlete_id=athleteId, 
                                  distance=dist, start_date=activity.start_date_local, moving_time=activity.moving_time.total_seconds()).first()

        if (duplicate == None):

            newActivity = RunningData(name=activity.name, athlete_id=athleteId, 
                                  distance=dist, start_date=activity.start_date_local, moving_time=activity.moving_time.total_seconds())
            try:
                db.session.add(newActivity)
                db.session.commit()
            except:
                continue

def getActivitiesFromDb(athleteId):
    try:
        return RunningData.query.filter_by(athlete_id=athleteId).order_by(RunningData.start_date)
    except:
        return []

# def plotlyDashboard(accessToken, athleteId):
# CLIENT_ACCESS = accessToken
athleteIdGlobal = testAthleteId #or athleteId
nameString = ""

if (testAthleteId == None):
    latestDate = checkDbForActivityData(athleteIdGlobal)
    newClient = Client(access_token=CLIENT_ACCESS)

    stravaRuns = StravaActivities(newClient)
    stravaRunsList = stravaRuns.getActivities(activityType="Run", afterDate=latestDate)

    # stravaStats = StravaStats(stravaRunsList)
    addActivitiesToDb(stravaRunsList, newClient.get_athlete().id)
    athlete = newClient.get_athlete()
    nameString = f'{athlete.firstname} {athlete.lastname}'


activities  = getActivitiesFromDb(athleteIdGlobal)
activities = [activity for activity in activities] 

stravaStats = StravaStats(activities)

nameString = nameString or "Test"

# allStats = strava.allStats

dates = stravaStats.dailyDateList
miles = stravaStats.dailyMilesList
dataset = pd.DataFrame({'dates': dates, 'miles': miles}, columns=['dates', 'miles'])

earliestDate = dates.min().date()
latestDate = dates.max().date()

app_dash.layout = html.Div([
    html.H2(html.Div(children='Hello '+ nameString),),
    html.Div([
    "Date Range: ",
    dcc.Input(id='startDate', value=dates.min().date(), type='date'),
    dcc.Input(id='endDate', value=dates.max().date(), type='date')
]), 
    html.Div(id='statSummary', children=getSummary(athleteIdGlobal, earliestDate, latestDate)),
    dcc.Graph(id="scatterplot", figure=px.scatter(dataset, x='dates', y='miles'))

])




@callback(
    Output(component_id='statSummary', component_property='children'),
    Input(component_id='startDate', component_property='value'),
    Input(component_id='endDate', component_property='value')
)
def update_output_div(start_date, end_date):
    athleteIdGlobal = session["userId"]

    return getSummary(athleteIdGlobal, start_date, end_date)

# @callback(
#     Output(component_id='scatterplot', component_property='figure'),
#     Input('startDate', 'value'),
#     Input('endDate', 'value')
# )
# def update_output_graph(start_date, end_date):
#     athleteId = session["userId"]

#     try:
#         activities  = getActivitiesFromDb(athleteId)
#         activities = [activity for activity in activities] 
#         stravaStats = StravaStats(activities)
#     except:
#         return px.scatter()
    
#     dates = stravaStats.getDailyDateList(stravaStats.runList, start_date, end_date)
#     miles = stravaStats.getDailyMilesList(stravaStats.runList, start_date, end_date)
#     dataset = pd.DataFrame({'dates': dates, 'miles': miles}, columns=['dates', 'miles'])
#     return px.scatter(dataset, x='dates', y='miles')

# @callback(
#     Output('statSummary', 'children'),
#     Input('scatterplot', 'relayoutData'))
# def display_relayout_data(relayoutData):
#     try:
#         graphRange = relayoutData
#         # graphRange = json.dumps(relayoutData, indent=2)
#         start_date = graphRange["xaxis.range[0]"][:10]
#         start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
#         end_date = graphRange["xaxis.range[1]"][:10]
#         end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

#         if (start_date > end_date):
#             start_date, end_date = end_date, start_date

#         return getSummary(athleteIdGlobal, start_date, end_date)
#     except:
#         return "error"


