from RunningStats import app

if __name__ == "__main__":
    app.run(debug=True)



# from flask import Flask, redirect, request, session
# from stravalib.client import Client
# import pickle
# import time
# import requests
# from functions.functions import *

# MY_STRAVA_CLIENT_ID, MY_STRAVA_CLIENT_SECRET = open('client.secret').read().strip().split(',')
# SESSION_SECRET = open('session.secret').read().strip()

# app = Flask(__name__)
# app.secret_key=SESSION_SECRET

# client = Client()

# @app.route('/')
# def hello():
#     #return redirect("/strava")
#    return 'Hello, World! 1234'

# @app.route('/strava')
# def strava():
      
#     url = client.authorization_url(client_id=MY_STRAVA_CLIENT_ID, redirect_uri='http://127.0.0.1:5000/authorization', scope=['read_all','profile:read_all','activity:read_all','activity:write'])
#     # url = client.authorization_url(client_id=MY_STRAVA_CLIENT_ID, redirect_uri='https://running-stats-d49636ca3c9f.herokuapp.com/authorization', scope=['read_all','profile:read_all','activity:read_all','activity:write'])

#     return redirect(url)



# @app.route('/authorization', methods=["GET"])
# def auth():

#     if request.method == "GET":

#         CODE = request.args.get("code")
#         # CODE = request.args.get('code')

#         token_response = client.exchange_code_for_token(client_id=MY_STRAVA_CLIENT_ID, client_secret=MY_STRAVA_CLIENT_SECRET, code=CODE)

#         session['access_token'] = token_response['access_token']
#         session['refresh_token'] = token_response['refresh_token']

#         return redirect("/dashboard")

#     # return redirect("/dashboard")
#     # return redirect("https://www.strava.com/oauth/authorize")


# @app.route('/dashboard')
# def dashboard():

#     try:
#         CLIENT_ACCESS = session['access_token']

#         client = Client(access_token=CLIENT_ACCESS)

#         activityList = getActivities(client)

#         runs = longestRunStreak(activityList)

#         athlete = client.get_athlete()

#         return(runs)
    
#     except:
#         return ("hellolskdnfdklsf")

# if __name__ == '__main__':
#     app.run()