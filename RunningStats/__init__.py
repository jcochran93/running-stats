from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

try:
    SESSION_SECRET = open('session.secret').read().strip()
except:
    SESSION_SECRET = os.getenv("SESSION_SECRET")


app = Flask(__name__)
app.config["SECRET_KEY"] = SESSION_SECRET
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)

from RunningStats.models import UserInfo

with app.app_context():
    db.create_all()

from RunningStats import routes