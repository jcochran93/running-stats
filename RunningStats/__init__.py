from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dash import Dash 
import dash_bootstrap_components as dbc
import os

is_prod = os.environ.get('PROD', None)

if is_prod:
    SESSION_SECRET = os.getenv("SESSION_SECRET")
    DATABASE_URL = os.getenv("DATABASE_URL")
    AUTH_URL = 'https://running-stats-d49636ca3c9f.herokuapp.com/authorization'
else:
    SESSION_SECRET = open('session.secret').read().strip()
    DATABASE_URL = open('database.secret').read().strip()
    AUTH_URL = 'http://127.0.0.1:5000/authorization'
 

app = Flask(__name__)
app.config["SECRET_KEY"] = SESSION_SECRET
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL

db = SQLAlchemy(app)

app_dash = Dash(__name__, server=app, url_base_pathname='/dash/',external_stylesheets=[dbc.themes.DARKLY])



from RunningStats.models import UserInfo

with app.app_context():
    db.create_all()

from RunningStats import routes
