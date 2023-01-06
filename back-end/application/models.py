from enum import unique
from .database import db
import datetime
from flask_security import UserMixin, RoleMixin
#from flask_login import UserMixin
from flask_wtf import FlaskForm 
from wtforms.validators import InputRequired, Email, Length
from wtforms import StringField, PasswordField, BooleanField

roles_users = db.Table('roles_users', 
    db.Column( "user_id", db.Integer(), db.ForeignKey('user.id')),
    db.Column( "role_id", db.Integer(), db.ForeignKey('role.id')),
)

def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=False)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users ,backref=db.backref('users'))
    tracks = db.relationship("Trackers", backref = 'user')


class Role(db.Model, RoleMixin):
    __tablename__ = "role"
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(85), unique = True)
    description = db.Column(db.String(255))

class Trackers(db.Model):
    __tablename__ = "trackers"
    tracker_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tracker_name = db.Column(db.String, unique=False)
    tracker_type = db.Column(db.String, nullable = False)
    tracker_question = db.Column(db.String, nullable = True)
    user_id = db.Column(db.String, db.ForeignKey("user.id"), nullable = False)
    logged = db.relationship("Logger", backref = "trackers")

class Logger(db.Model):
    __tablename__ = "logger"
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    log_value = db.Column(db.String, unique=True, nullable = False)
    track_tracker = db.Column(db.String, db.ForeignKey("trackers.tracker_id"), nullable = False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])