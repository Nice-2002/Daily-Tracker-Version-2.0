from flask_restful import Resource, Api, marshal_with, reqparse, fields
from flask import request, jsonify
from flask_security import LoginForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Numeric
from .database import db
from .models import Trackers, Logger, User, LoginForm, RegisterForm
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import numpy as np
import matplotlib.pyplot as plt
from flask_cors import cross_origin

class HomeAPI(Resource):
    def get(self):
        tracker = Trackers.query.filter_by(user_id = 1).all()
        data = []
        for track in tracker:
            new_track = dict()
            new_track["tracker_name"] = track.tracker_name
            new_track["tracker_type"] = track.tracker_type
            new_track["tracker_question"] = track.tracker_question
            data.append(new_track)
        return jsonify(data)