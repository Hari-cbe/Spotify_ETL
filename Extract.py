import requests
from datetime import datetime
import pandas as pd
import datetime
import os 
from dotenv import load_dotenv, dotenv_values



load_dotenv()

USER_ID = os.getenv("CLIENT_ID")
USER_SECRET = os.getenv("CLIENT_SECRET")


# Get the access Token 
data = {
  "grant_type": "client_credentials",
  "redirectUri": "http://localhost:8000/callback",
  "client_id": USER_ID,
  "client_secret": USER_SECRET,
  "scope" : "user-read-currently-playing user-read-recently-played"
};

input_var = {
    "Content-Type" : "application/x-www-form-urlencoded"
}
get_token = requests.post("https://accounts.spotify.com/api/token",headers=input_var,data=data)

# Check for successful response
if get_token.status_code == 200:  
    data_dict = get_token.json() 
    print(data_dict)
else:
    print("Error:", get_token.text)

def return_df():
    input_variables = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization": "Bearer {token}".format(token=data_dict["access_token"])
    }
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=2)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    # Download all songs you've listened to "after yesterday", which means in the last 24 hours      
    try:
        r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix_timestamp), headers = input_variables)
    except:
        print("ERROR",r.text)
    # r = requests.get("https://api.spotify.com/v1/artists/4Z8W4fKeB5YxbusRsdQVPb",headers=input_variables)
    data = r.json()
    print(data)


return_df()
# print(USER_ID, USER_SECRET)