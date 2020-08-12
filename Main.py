# library to make https requests to the Strava API
import requests
# library to interface with MongoDB
import pymongo
# library to check if an access token is expired
import time
# library to generate ISO 8601 formatted date time to create a Strava activity
from datetime import datetime

# my athlete_id (created by Strava for each user)
athlete_id = 45807130
# API keys for my Strava dev account
client_id = "49946"
client_secret = "d34b8cb3feebcb58a8ddab131f6a0fb0542076bd"

# connects to a MongoDB database with a document containing a users athlete_id, access token, when that access token expires, and a refresh token
client = pymongo.MongoClient('mongodb+srv://lucas:Pizza112@stravarecords.fqrf5.mongodb.net/test?authSource=admin&replicaSet=atlas-4czmj0-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true')

# gets the data for a specific user
info = client["auth"]["users"].find_one({"athlete_id": athlete_id})

# gets when the access token expires in epoch
expiry = info["expires_at"]

# checks to see if the access token is expired
if (time.time() >= expiry):
    # if it is expired it gets a new token and updates the database
    # url in the Strava API to refresh a token with the client_id, client_secret, and refresh token entered as variables
    refresh_url = "https://www.strava.com/api/v3/oauth/token?client_id=" + client_id + "&client_secret=" + client_secret + "&grant_type=refresh_token&refresh_token=" + info["refresh"]
    # makes the request and stores the json response as a dictionary
    response = requests.post(refresh_url).json()
    # updates the database with the new access token
    client["auth"]["users"].find_one_and_update(
        {"athlete_id": athlete_id},
        {"$set":
             {"access": response["access_token"]}
         }
    )
    # updates the database with the new expiry date
    client["auth"]["users"].find_one_and_update(
        {"athlete_id": athlete_id},
        {"$set":
             {"expires_at": response["expires_at"]}
         }
    )

# authorization header that pulls the access token from MongoDB
header = {"Authorization": "Bearer " + info["access"]}
# variables to create a Strava activity
name = "Test"
typeOfActivity = "Workout"
startDate = str(datetime.now())
elapsedTime = str(1800)
description = "This is a test."

# url in the Strava API to create an activity
create_url = "https://www.strava.com/api/v3/activities?name=" + name + "&type=" + typeOfActivity + "&start_date_local=" + startDate + "&elapsed_time=" + elapsedTime + "&description=" + description
# https post request to create an activity
requests.post(create_url, headers = header)
