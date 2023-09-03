from flask import Flask, redirect
from stravalib.client import Client
import pickle
import time
import requests
MY_STRAVA_CLIENT_ID, MY_STRAVA_CLIENT_SECRET = open('client.secret').read().strip().split(',')

app = Flask(__name__)


@app.route('/')
def hello():
    #return redirect("/strava")
   return 'Hello, World! 1234'

@app.route('/strava')
def strava():
    
    # if requests.method == "GET":

    #     CODE = requests.get("code")
    #     access_token = client.exchange_code_for_token(client_id=MY_STRAVA_CLIENT_ID, client_secret=MY_STRAVA_CLIENT_SECRET, code=CODE)

    #     return redirect("/dashboard")


    client = Client()
    
    url = client.authorization_url(client_id=MY_STRAVA_CLIENT_ID, redirect_uri='https://running-stats-d49636ca3c9f.herokuapp.com/authorization', scope=['read_all','profile:read_all','activity:read_all','activity:write'])

    return (url)



@app.route('/authorization', methods=["GET"])
def auth():

    if request.method == "GET":

        CODE = requests.get("code")
        # CODE = request.args.get('code')

        access_token = client.exchange_code_for_token(client_id=MY_STRAVA_CLIENT_ID, client_secret=MY_STRAVA_CLIENT_SECRET, code=CODE)

        return redirect("/dashboard")

    # return redirect("/dashboard")
    # return redirect("https://www.strava.com/oauth/authorize")


@app.route('/dashboard')
def dashboard():

    return client.get_athlete()

if __name__ == '__main__':
    app.run()