from RunningStats import app_dash
import pandas as pd
from dash import html, dcc, Input, Output, callback
import plotly.express as px
from stravalib import Client
from functions.StravaStats import StravaStats
from RunningStats.models import UserInfo, Token

summaryStringList = []
dataset = pd.DataFrame()

strava = None

app_dash.layout = html.Div(children="Loading...")

def plotlyDashboard(accessToken):
    CLIENT_ACCESS = accessToken

    newClient = Client(access_token=CLIENT_ACCESS)
    strava = StravaStats(newClient, 200)

    athlete = newClient.get_athlete()
    nameString = f'{athlete.firstname} {athlete.lastname}'

    # allStats = strava.allStats

    dates = strava.dailyDateList
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
        html.Div(id="statSummary", children=getSummary(CLIENT_ACCESS, earliestDate, latestDate))
    ])




@callback(
    Output(component_id='statSummary', component_property='children'),
    Input(component_id='startDate', component_property='value'),
    Input('endDate', 'value')
)
def update_output_div(start_date, end_date):
    
    return getSummary(strava, start_date, end_date)

def getSummary(token, startDate, endDate):

    newClient = Client(access_token=token)
    stravaClient = StravaStats(newClient, 200)

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

