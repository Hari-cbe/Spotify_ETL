import requests
from datetime import datetime
import pandas as pd
import datetime
import os 
import json
from dotenv import load_dotenv, dotenv_values



load_dotenv()

USER_ID = os.getenv("CLIENT_ID")
USER_SECRET = os.getenv("CLIENT_SECRET")

def get_access_token():
    data = {
    "grant_type": "client_credentials",
    "client_id": USER_ID,
    "client_secret": USER_SECRET
    };

    input_var = {
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    get_token = requests.post("https://accounts.spotify.com/api/token",headers=input_var,data=data)

    # Check for successful response
    if get_token.status_code == 200:  
        data_dict = get_token.json()
    else:
        print("Error:", get_token.text)
    return data_dict

def return_df():
    token = get_access_token()

    input_variables = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization": "Bearer {token}".format(token=token["access_token"])
    }

    r = requests.get("https://api.spotify.com/v1/albums?ids=382ObEPsp2rxGrnsizN5TX,1A2GTWGtFfWp7KSQTwWOyo,2noRn2Aes5aoNVsU6iWThc&market=IN",headers=input_variables)
    
    req_data = r.json()

    
    artist_names = []
    album_names = []
    songs = []
    durations = []

    # Convert Unix Seconds to normal time 
    def convert_ms_time(ms):
        seconds = (ms / 1000) % 60 
        mins = ( ms / (1000 * 60)) % 60

        return f"{int(mins):02}:{int(seconds):02}"
    

    for item in req_data["albums"]:
        for track in item["tracks"]["items"]:
            album_names.append(item["name"])
            songs.append(track["name"])
            durations.append(convert_ms_time(track["duration_ms"]))

    
    for item in req_data["albums"]:
        for track in item["tracks"]["items"]:
            artist_list = []
            for artist in track["artists"]:
                artist_list.append(artist["name"])
            artist_names.append(artist_list)

       
    songs = {
      "album_name" : album_names,
      "song" : songs,
      "artists" : artist_names,
      "duration" : durations
    }


    # df = pd.DataFrame(songs.items(), columns=["Albums","Song","Artist","Duration"])
    df = pd.DataFrame.from_dict(songs)
    return df 

if __name__ == "__main__":
    return_df()
# print(USER_ID, USER_SECRET)