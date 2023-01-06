from email import encoders, message
from email.mime.base import MIMEBase
from pipes import Template
from re import T
from application.workers import celery
from datetime import datetime
from celery.schedules import crontab
from application.models import *
from jinja2 import Template
from weasyprint import HTML
from application.models import *
from flask_login import current_user
import csv

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date

SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = 1025
SENDER_ADDRESS = "Email@meer.com"
SENDER_PASSWORD = ""

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=17, minute=0),
        #10,
        daily_reminder_jobs.s(),
        name = "Daily remonder jobs send at 5pm"
    )
    sender.add_periodic_task(
        crontab(hour=12, minute=0, day_of_month='1'),
        #10,
        monthly_progress_report.s(),
        name = "Monthly Progress report sent at 12pm"
    )

def format_message(template_fie, data=None):
    #template = 'Dear, ' + data.username + "\n\n" + "You didn't logged to any of the tracker today.\nPlease login to the website and log in your daily tracker.\n\nRegards\nMeer."
    with open("./template/"+template_fie) as file_:
        template = Template(file_.read())
    return template.render(data=data)
    #return template


def send_email(to_address, subject, message, content="text", attachment_file=None):
    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject

    if content == "html":
        msg.attach(MIMEText(message, "html"))
    else:
        msg.attach(MIMEText(message, "plain"))


    if attachment_file:
        with open("./"+attachment_file, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)


        part.add_header(
            "Content-Disposition", f"attachment; filename = {attachment_file}",
        )
        msg.attach(part)

    s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()
    print("Email sent successfully")
    return True

@celery.task()
def daily_reminder_jobs():
    users = User.query.all()
    today = date.today()
    current_day = today.strftime("%d")
    for user in users:
        print("Inside user")
        trackers = Trackers.query.filter_by(user_id = user.id).all()
        logged_today = False
        for tracker in trackers:
            print("Inside tracker")
            logs = tracker.logged
            for log in logs:
                print("Inside logger")
                if log.timestamp.strftime("%d") == current_day:
                    logged_today = True
                    break
            if logged_today:
                break
        if logged_today == False:
            print("generating message")
            message = format_message('daily-reminder.html', data=user)
            print("sending mail")
            send_email(user.email, subject="Daily Reminder", message=message, content="html")
    return True

def format_report(template_fie, logs, user, tracker):
    with open("./template/"+template_fie) as file_:
        template = Template(file_.read())
    return template.render(logs=logs, user=user, tracker=tracker)

def create_pdf_report(logs, user, tracker):
    message  = format_report("report-template.html", logs=logs, user=user, tracker=tracker)
    html = HTML(string=message)
    file_name = str(user.username) + ".pdf"
    print(file_name)
    html.write_pdf(target=file_name)

@celery.task()
def monthly_progress_report():
    users = User.query.all()
    for user in users:
        trackers = Trackers.query.filter_by(user_id = user.id).all()
        logs_len = 0
        to_be_used_tracker = None
        for tracker in trackers:
            logs = tracker.logged
            if len(logs) > logs_len:
                to_be_used_tracker = tracker
        if to_be_used_tracker != None:
            logs = to_be_used_tracker.logged
            create_pdf_report(logs=logs, user=user, tracker=to_be_used_tracker)
            message = format_message('monthly-mail-template.html', data=user)
            send_email(user.email, subject="Monthly Report", message=message, content="html", attachment_file=user.username+".pdf")

@celery.task()
def export_as_csv(data):
    if data['value'] == "logs":
        tracker_id = data['tracker_id']
        tracker = Trackers.query.get(tracker_id)
        logs = tracker.logged
        fields = ['SNo.', 'timeStamp', 'value']
        filename =  "report.csv"
        print(type(logs))
        dict = []
        for i in range(len(logs)):
            new_ins = []
            new_ins.append(i+1)
            new_ins.append(logs[i].timestamp)
            new_ins.append(logs[i].log_value)
            dict.append(new_ins)
        with open(filename, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(fields)
            writer.writerows(dict)
    if data['value'] == "Trackers":
        trackers = Trackers.query.filter_by(user_id = current_user.id).all()
        fields = ["SNo.", "Tracker_name", "Tracker_type", "Tracker_question"]
        filename = "report.csv"
        dict = []
        for i in range(len(trackers)):
            new_ins = []
            new_ins.append(i+1)
            new_ins.append(trackers[i].tracker_name)
            new_ins.append(trackers[i].tracker_type)
            new_ins.append(trackers[i].tracker_question)
            dict.append(new_ins)
        with open(filename, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(fields)
            writer.writerows(dict)

@celery.task()
def export_options(data):
    if data['value'] == "logs":
        trackers = Trackers.query.filter_by(user_id = current_user.id).all()
        fields = ['SNo.', 'Tracker_name', 'Tracker_type','timeStamp', 'value']
        filename =  "exportlogs.csv"
        dict = []
        for tracker in trackers:
            logs = tracker.logged
            for i in range(len(logs)):
                new_ins = []
                new_ins.append(i+1)
                new_ins.append(tracker.tracker_name)
                new_ins.append(tracker.tracker_type)
                new_ins.append(logs[i].timestamp)
                new_ins.append(logs[i].log_value)
                dict.append(new_ins)
        with open(filename, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(fields)
            writer.writerows(dict)