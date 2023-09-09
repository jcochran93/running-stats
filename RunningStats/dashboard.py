from RunningStats import app_dash
import pandas as pd
from dash import html, dcc, Input, Output, callback
import plotly.express as px
from stravalib import Client
from functions.StravaStats import StravaStats
from RunningStats.models import UserInfo, Token, RunningData
from sqlalchemy import desc
from datetime import datetime, timedelta, date
from RunningStats import db

summaryStringList = []
dataset = pd.DataFrame()

stravaClient = None

app_dash.config.suppress_callback_exceptions = True

app_dash.layout = html.Div(children="Loading...")

def plotlyDashboard(accessToken, athleteId):
    CLIENT_ACCESS = accessToken

    newClient = Client(access_token=CLIENT_ACCESS)
    earliestDate = checkDbForActivityData(athleteId)

    # if( earliestDate == date.min):
    stravaClient = StravaStats(newClient, earliestDate)
    addActivitiesToDb(newClient, earliestDate)
    activities  = getActivitiesFromDb(athleteId)
    activities = [activity for activity in activities] 

    stravaStats = StravaStats(activities)

    athlete = newClient.get_athlete()
    nameString = f'{athlete.firstname} {athlete.lastname}'

    # allStats = strava.allStats

    dates = stravaClient.dailyDateList
    # miles = strava.dailyMilesList
    # dataset = pd.DataFrame({'dates': dates, 'miles': miles}, columns=['dates', 'miles'])

    earliestDate = dates.min().date()
    latestDate = dates.max().date()

    app_dash.layout = html.Div([
        html.H2(html.Div(children='Hello '+ nameString),),
        html.Div([
        "Date Range: ",
        dcc.Input(id='startDate', value=dates.min().date(), type='date'),
        dcc.Input(id='endDate', value=dates.max().date(), type='date')
    ]), 
        html.Div(id="statSummary", children=getSummary(earliestDate, latestDate))
    ])




@callback(
    Output(component_id='statSummary', component_property='children'),
    Input(component_id='startDate', component_property='value'),
    Input('endDate', 'value')
)
def update_output_div(start_date, end_date):
    
    return getSummary(start_date, end_date)

def getSummary(startDate, endDate):

    summaryStringList = stravaClient.summaryStringForRange(startDate, endDate)
    
    dates = stravaClient.getDailyDateList(stravaClient.runList, startDate, endDate)
    miles = stravaClient.getDailyMilesList(stravaClient.runList, startDate, endDate)
    dataset = pd.DataFrame({'dates': dates, 'miles': miles}, columns=['dates', 'miles'])

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
        html.Div(children=summaryStringList[10]),
        dcc.Graph(figure=px.scatter(dataset, x='dates', y='miles'))
    ])

def checkDbForActivityData(athleteId):
    
    results = RunningData.query.filter_by(athleteId=athleteId).order_by(RunningData.startDate).first_or_404()

    try:
        earliestDate = results[0]
    except:
        earliestDate = date.min

    return earliestDate

def addActivitiesToDb(stravaClient, afterDate):

    activities = stravaClient.get_activities(afterDate)

    for activity in activities:

        dist = str(activity.distance).strip(" meter")
        dist = float(dist) / 1609.34

        newActivity = RunningData(name=activity.name, athleteId=stravaClient.get_athlete().id, 
                                  distance=dist, startDate=activity.start_date_local, movingTime=activity.moving_time)
        try:
            db.session.add(newActivity)
            db.session.commit()
        except:
            continue

def getActivitiesFromDb(athleteId):

    return RunningData.query.filter_by(athleteId=athleteId).order_by(RunningData.startDate)



# id = db.Column(db.Integer, nullable=True, primary_key=True)
#     name = db.Column(db.String(100))
#     athleteId = db.Column(db.Integer, db.ForeignKey("user_info.id"), nullable=False)
#     distance = db.Column(db.Integer, nullable=False, default = 0)
#     startDate = db.Column(db.DateTime, nullable=False)
#     movingTime = db.Column(db.Float, nullable=False)
