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


