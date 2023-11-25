from datetime import datetime
from project.server import db
from flask_login import UserMixin
from project.server import login

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(120), index=True, unique=True)
    projects = db.relationship('Project', backref='owner', cascade='all, delete')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    code = db.Column(db.String(1024))