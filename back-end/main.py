#Importing Libraries
from crypt import methods
from http.client import CONFLICT
from nis import cat
from flask import Flask, jsonify, request, send_file
from application.database import db
from flask_cors import CORS
from application.models import *
from application import workers
from application import tasks
import csv
import matplotlib.pyplot as plt

from flask_restful import Resource
from flask_security import Security, SQLAlchemyUserDatastore
from flask_security import auth_required
from flask_login import current_user

app = None
celery = workers.celery

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'thisissecrekeyformadapplication'
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = "Authentication-Token"
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECURITY_PASSWORD_SALT'] = 'secretsalt__'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quantified.sqlite3'
app.config['WTF_CSRF_ENABLED'] = False
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = "Authentication-Token"
app.config['CELERY_BROKER_URL'] = "redis://localhost:6379/1"
app.config['CELERY_RESULT_BACKEND'] = "redis://localhost:6379/2"
celery.conf.update(
  broker_url = app.config['CELERY_BROKER_URL'],
  result_backend = app.config['CELERY_RESULT_BACKEND']
)
celery.Task = workers.ContextTask
app.app_context().push()
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
db.init_app(app)



#controllers
@app.route("/", methods=["GET"])
@auth_required("token")
def index():
    tracker = Trackers.query.filter_by(user_id = current_user.id).all()
    data = []
    for track in tracker:
      new_track = dict()
      new_track["tracker_id"] = track.tracker_id
      new_track["user_id"] = track.user_id
      new_track["tracker_name"] = track.tracker_name
      new_track["tracker_type"] = track.tracker_type
      new_track["tracker_question"] = track.tracker_question
      data.append(new_track)
    return jsonify(data), 200

@app.route("/tracker/<int:tracker_id>", methods=["GET", "DELETE", "PUT"])
@auth_required("token")
def tracker_related(tracker_id):
  #get details of a tracker
  if request.method == "GET":
    tracker  = Trackers.query.get(tracker_id)
    track = {
      "tracker_id": tracker.tracker_id,
      "user_id": tracker.user_id,
      "tracker_name": tracker.tracker_name,
      "tracker_type": tracker.tracker_type,
      "tracker_question": tracker.tracker_question
    }
    return jsonify(track)

  #update a tracker
  elif request.method == "PUT":
    tracker = Trackers.query.get(tracker_id)
    data = request.json
    track_name = data["tracker_name"]
    track_ques = data["tracker_question"]
    track_type = data["tracker_type"]

    if track_type != tracker.tracker_type:
      logs = tracker.logged
      for log in logs:
        db.session.delete(log)
      db.session.commit()
    tracker.tracker_name = track_name
    tracker.tracker_question = track_ques
    tracker.tracker_type = track_type

    db.session.commit()
    return "Success", 200

  #dlete a tracker
  elif request.method == "DELETE":
    track = Trackers.query.get(tracker_id)
    logs = track.logged
    for log in logs:
        db.session.delete(log)
    db.session.delete(track)
    db.session.commit()    
    return "Success", 200


#create a tracker
@app.route("/create_tracker", methods=["POST"])
@auth_required("token")
def create_tracker():
  if request.method == "POST":
    data = request.json
    track_name = data["tracker_name"]
    track_question = data["tracker_question"]
    track_type = data["tracker_type"]
    #user_id = 1
    user_id = current_user.id

    trackers = Trackers.query.filter_by(user_id = current_user.id).all()
    for tracker in trackers:
      if tracker.tracker_name == track_name:
        return "Tracker already exist", 300

    track = Trackers(
      tracker_name = track_name,
      tracker_question = track_question,
      tracker_type = track_type,
      user_id = user_id
    )
    db.session.add(track)
    db.session.commit()
    return "Success", 200

@app.route("/tracker/<int:tracker_id>/logs", methods=["GET", "POST"])
@auth_required("token")
def logging_related(tracker_id):
  #view all logs related a specific tracker
  if request.method == "GET":
    tracker = Trackers.query.get(tracker_id)
    final_logs = []
    logs = tracker.logged
    for log in logs:
      all_logs = dict()
      all_logs["log_id"] = log.log_id
      all_logs["log_value"] = log.log_value
      all_logs["time_stamp"] = log.timestamp
      final_logs.append(all_logs)
    return jsonify(final_logs)
  
  #log into tracker
  elif request.method == "POST":
    tracker = Trackers.query.get(tracker_id)
    data = request.json
    log_value = data
    track = Logger(
      log_value = log_value
    )
    tracker.logged.append(track)
    db.session.commit()
    return "Success", 200

@app.route("/tracker/<int:tracker_id>/log/<int:log_id>", methods=["GET", "DELETE", "PUT"])
@auth_required("token")
def log_related(tracker_id, log_id):
  #get details about a specific log
  if request.method == "GET":
    log = Logger.query.get(log_id)
    new_log = {
      "log_id": log.log_id,
      "log_value": log.log_value,
    }
    return jsonify(new_log)

  #update a log
  elif request.method == "PUT":
    log = Logger.query.get(log_id)
    db.session.delete(log)
    tracker = Trackers.query.get(tracker_id)
    data = request.json
    log_value = data["value"]
    track = Logger(
      log_value = log_value
    )
    tracker.logged.append(track)
    db.session.commit()
    return "Success", 200
  
  #delete a log value
  elif request.method == "DELETE":
    log = Logger.query.get(log_id)
    db.session.delete(log)
    db.session.commit()
    return "Success", 200


#delete current user
@app.route("/delete_account", methods=["GET"])
@auth_required('token')
def delete_account():
    trackers = Trackers.query.filter_by(user_id = current_user.id).all()
    for track in trackers:
        logs = track.logged
        for log in logs:
            db.session.delete(log)
        db.session.delete(track)
    user_datastore.delete_user(current_user)
    db.session.commit()
    return "Success", 200


#get details of current user
@app.route("/get_user", methods=["GET"])
@auth_required('token')
def get_user():
  user = {
      "user_id": current_user.id,
      "user_name": current_user.username,
    }
  return jsonify(user)

#register endpoint
@app.route("/users", methods=["GET", "POST"])
def user():
  if request.method == "POST":
    data = request.json
    if user_datastore.find_user(email=data['email']):
      return "User Already Exist"
    try:
      user = user_datastore.create_user(
        username = data['username'],
        email = data['email'],
        password = data['password']
      )
      db.session.commit()
      print(user)
      return "User created successfully"
    except:
      raise CONFLICT
  if request.method == "GET":
    return current_user.name


#general export options
@app.route("/export", methods=["POST"])
def export():
  data = request.json
  filename = "report.csv"
  job = tasks.export_as_csv(data)
  return send_file(
    filename,
    mimetype='text/csv',
    download_name=filename,
    as_attachment=True
  )

#export all data tracker as well as log vals
@app.route("/export_options", methods=["POST"])
def export_options():
  data = request.json
  filename = "exportlogs.csv"
  job = tasks.export_options(data)
  return send_file(
    filename,
    mimetype='text/csv',
    download_name=filename,
    as_attachment=True
  )

#get the trandline image
@app.route("/trendline/<int:tracker_id>", methods=["GET"])
def trendline(tracker_id):
  tracker = Trackers.query.get(tracker_id)
  logs = tracker.logged
  data = {}
  if tracker.tracker_type == 'number':
    for log in logs:
      data[log.timestamp.strftime("%Y%m%d%H%M%S")] = int(log.log_value)
    times = list(data.keys())
    times = ['-'.join(s[i:i+2] for i in range(0, len(s), 2) if i != 0) for s in times]
    values = list(data.values())
    fig = plt.figure()
    plt.bar(times, values, color ='maroon', width = 0.4)
    plt.xticks(rotation=45, ha='right')
    plt.xlabel("Timeline")
    plt.ylabel("Log value")
    fig.savefig('my_plot.png')
    return send_file(
      "my_plot.png",
      mimetype='image/jpeg',
      download_name="my_plot.png",
      as_attachment=True
    )
  else:
    return "Not a number type tracker"


#Start the app
if __name__ == '__main__':
  # Run the Flask app
  app.run(
    host='0.0.0.0',
    debug=True,
  )
