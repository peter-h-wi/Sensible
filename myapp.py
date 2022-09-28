import json
from sqlite3 import Timestamp
from time import timezone
from urllib import request
from flask import Flask, request, jsonify
from datetime import date, timedelta, datetime, timezone
import requests
from pymongo import MongoClient
import certifi

# myheader = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzhSTUIiLCJzdWIiOiJCNEYzNVEiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcm94eSBycHJvIHJudXQgcnNsZSByYWN0IHJyZXMgcmxvYyByd2VpIHJociBydGVtIiwiZXhwIjoxNjkyMjk2MDE4LCJpYXQiOjE2NjA3NjAwMTh9.Ud4qSIXGglbXaYeK-JDzL9GolEskKk9aCGrl79NMDY4'}
# myheader = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzhSRFQiLCJzdWIiOiJCNEYzNVEiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcm94eSBycHJvIHJudXQgcnNsZSByYWN0IHJsb2MgcnJlcyByd2VpIHJociBydGVtIiwiZXhwIjoxNjkzNDg4MDQxLCJpYXQiOjE2NjE5NTIwNDF9.uk4UyLwyQeLjnoE6jxKPNCxfkzs0mFTq_09cfuyV74U'}
# myheader = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzhSNkIiLCJzdWIiOiJCNEYzNVEiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcm94eSBybnV0IHJwcm8gcnNsZSByYWN0IHJsb2MgcnJlcyByd2VpIHJociBydGVtIiwiZXhwIjoxNjkyMjk1NDQ0LCJpYXQiOjE2NjA3NTk0NDR9.bILcGIrPRXPWRrWBZDKRLsZdtTKKqPUpZ4NZZ-U3k5g'}
# myheader = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzhRNVIiLCJzdWIiOiJCNEYzNVEiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcm94eSBycHJvIHJudXQgcnNsZSByYWN0IHJyZXMgcmxvYyByd2VpIHJociBydGVtIiwiZXhwIjoxNjkyMzIxOTk2LCJpYXQiOjE2NjA3ODU5OTZ9.Rw2SpXEMA3YVx1-O1W0ZamKq2BwRnUpOw_fQCMRn0z8'}
myheader = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzhRUEYiLCJzdWIiOiJCNEYzNVEiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcm94eSBycHJvIHJudXQgcnNsZSByYWN0IHJyZXMgcmxvYyByd2VpIHJociBydGVtIiwiZXhwIjoxNjkyMzIyMTc4LCJpYXQiOjE2NjA3ODYxNzh9.t4-tjP-pBKe-wdbYLTL9t-h7wAOWsAlu-cGurSkfJiU'}
# myheader = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzhRTkQiLCJzdWIiOiJCNEYzNVEiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcm94eSBybnV0IHJwcm8gcnNsZSByYWN0IHJsb2MgcnJlcyByd2VpIHJociBydGVtIiwiZXhwIjoxNjkyMzIyMzQ0LCJpYXQiOjE2NjA3ODYzNDR9.-kAqRq3x5D5J0nCgzOm-2ATMbz9e7EZYXUiitEt6h4k'}


client = MongoClient("mongodb+srv://sensible123:qwerty12345@cluster0.9kcbopx.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = client["mydb"]
app = Flask(__name__)

@app.route("/heartrate/last", methods=["GET"])
def get_heart_rate():
    # Return the most recent heartrate.
    dayinput = date.today()
    myurl = "https://api.fitbit.com/1/user/-/activities/heart/date/{}/1d.json".format(
        dayinput)
    resp = requests.get(myurl, headers=myheader).json()
    activity_dataset = resp["activities-heart-intraday"]["dataset"]
    while (len(activity_dataset) == 0):
        # if there is no data on that day, check the previous days.
        dayinput -= timedelta(days=1)
        myurl = "https://api.fitbit.com/1/user/-/activities/heart/date/{}/1d.json".format(
            dayinput)
        resp = requests.get(myurl, headers=myheader).json()
        activity_dataset = resp["activities-heart-intraday"]["dataset"]
    recent = activity_dataset[-1]
    # retrieve heartrate, timeoffset (min)
    heartrate = recent["value"]
    timeoffset = datetime.now(tz=timezone.utc) - datetime.combine(dayinput, datetime.strptime(
        recent["time"], "%H:%M:%S").time(), tzinfo=timezone.utc)
    ret = {"heart-rate": heartrate,
           "time offset": timeoffset.seconds//60-240}  # minutes
    return jsonify(ret)


@app.route("/steps/last", methods=["GET"])
def get_steps():
    # Return the most recent step.
    dayinput = date.today()
    myurl = "https://api.fitbit.com/1/user/-/activities/steps/date/today/1d.json"
    resp = requests.get(myurl, headers=myheader).json()
    activity_step = resp["activities-steps"]
    timeoffset = resp["activities-steps-intraday"]["datasetInterval"]
    myurl = "https://api.fitbit.com/1/user/-/activities/distance/date/today/1d.json"
    resp = requests.get(myurl, headers=myheader).json()
    activity_distance = resp["activities-distance"]
    while (len(activity_step) == 0 or len(activity_distance) == 0):
        # if there is no data on that day, check the previous days.
        dayinput -= timedelta(days=1)
        myurl = "https://api.fitbit.com/1/user/-/activities/steps/date/{}/1d.json".format(
            dayinput)
        resp = requests.get(myurl, headers=myheader).json()
        activity_step = resp["activities-steps"]
        myurl = "https://api.fitbit.com/1/user/-/activities/distance/date/{}/1d.json".format(
            dayinput)
        resp = requests.get(myurl, headers=myheader).json()
        activity_distance = resp["activities-distance"]
    timeoffset = datetime.now(
        tz=timezone.utc) - datetime.combine(dayinput, datetime.min.time(), tzinfo=timezone.utc)
    ret = {"step-count": activity_step[-1]["value"],
           "distance": activity_distance[-1]["value"], "time offset": timeoffset.seconds//60-240}
    return jsonify(ret)


@app.route("/sleep/<date_input>", methods=["GET"])
def get_sleep(date_input):
    myurl = "https://api.fitbit.com/1.2/user/-/sleep/date/{}.json".format(
        date_input)
    resp = requests.get(myurl, headers=myheader).json()
    ret = {}
    if len(resp["sleep"]) > 0:
        sleep = resp["sleep"][0]["levels"]["summary"]
        for key in sleep:
            ret[key] = sleep[key]["minutes"]
    return ret


@app.route("/activity/<date_input>", methods=["GET"])
def get_activeness(date_input):
    # Return the activeness.
    myurl = "https://api.fitbit.com/1/user/-/activities/date/{}.json".format(
        date_input)

    resp = requests.get(myurl, headers=myheader).json()
    summary = resp["summary"]

    sedentary = summary["sedentaryMinutes"]
    lightly_active = summary["lightlyActiveMinutes"]
    fairly_active = summary["fairlyActiveMinutes"]
    very_active = summary["veryActiveMinutes"]

    ret = {"very-active": very_active, "fairly-active": fairly_active,
           "lightly-active": lightly_active, "sedentary": sedentary}
    return jsonify(ret)

# Returns the last logged temperature and humidity values*
# e.g., {‘temp’: 75, ‘humidity’: 88, ‘timestamp’: 1594823426.159446}
@app.route("/sensors/env", methods=["GET"])
def get_environment():
    # get the latest value
    row = db.myenvironment.find().sort("timestamp", -1).limit(1)[0]
    ret = {"temp": row["temp"], "humidity": row["humidity"], "timestamp": row["timestamp"]}
    return jsonify(ret)

# Returns the last logged gesture/pose/presence information*
# e.g., {‘presence’: ‘yes’, ‘pose’: ‘sitting’, ‘timestamp’: 1594823426.159446}
@app.route("/sensors/pose", methods=["GET"])
def get_pose():
    # get the latest value
    row = db.mypose.find().sort("timestamp", -1).limit(1)[0]
    ret = {"presence": row["presence"], "pose": row["pose"], "timestamp": row["timestamp"]}
    return jsonify(ret)

@app.route("/post/env", methods=["POST"])
def postenv():
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    env = request.get_json()
    db.myenvironment.insert_one({'temp': env['temp'], 'humidity': env['humidity'], 'timestamp': timestamp})
    return {'temp': env['temp'], 'humidity': env['humidity'], 'timestamp': timestamp}

@app.route("/post/pose", methods=["POST"])
def postpose():
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    pose = request.get_json()
    db.mypose.insert_one({'presence': pose['presence'], 'pose': pose['pose'], 'timestamp': timestamp})
    return {'presence': pose['presence'], 'pose': pose['pose'], 'timestamp': timestamp}

if __name__ == '__main__':
    app.run(debug=True)