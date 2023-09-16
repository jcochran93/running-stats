from datetime import datetime
from flask_login import UserMixin
from RunningStats import db


class UserInfo(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

class Token(db.Model):
    id = db.Column(db.Integer, db.ForeignKey("user_info.id"), nullable=False, primary_key=True)
    access_token = db.Column(db.String(100), nullable=False)
    refresh_token = db.Column(db.String(100), nullable=False)
    expires_at = db.Column(db.Integer, nullable=False)

class RunningData(db.Model):
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    name = db.Column(db.String(100))
    athlete_id = db.Column(db.Integer, db.ForeignKey("user_info.id"), nullable=False)
    distance = db.Column(db.Float, nullable=False, default = 0)
    start_date_local = db.Column(db.DateTime, nullable=False)
    moving_time = db.Column(db.Float, nullable=False)
    gear_id = db.Column(db.Integer, nullable=False, default=0)


