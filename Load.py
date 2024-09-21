import Extract
import Transform
import pandas as pd 
import datetime
from datetime import datetime
import requests
import json
import sqlite3
import sqlalchemy
from sqlalchemy.orm import sessionmaker

DATABASE_LOCATION = "sqlite:///Spotify_albums.sqlite"


if __name__ == "__main__":

    load_df = Extract.return_df()

    if Transform.DataQuaityCheck(load_df) == False:
        raise Exception("Data is Empty")
    
    Transform_df = Transform.TransformData(load_df)


    # Loading The Dataset 

    engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect("Spotify_albums.sqlite")
    cursor  = conn.cursor()

        #SQL Query to Create Played Songs
    sql_query_1 = """
    CREATE TABLE IF NOT EXISTS Albums(
        Album VARCHAR(200),
        Song VARCHAR(200),
        Artists VARCHAR(2000),
        DURATION VARCHAR(200)
    )
    """
    #SQL Query to Create Most Listened Artist
    sql_query_2 = """
    CREATE TABLE IF NOT EXISTS Artists(
        Artist_ID VARCHAR(200),
        Artists VARCHAR(200),
        CONSTRAINT primary_key_constraint PRIMARY KEY (Artist_ID)
    )
    """

    cursor.execute(sql_query_1)
    cursor.execute(sql_query_2)

    print("Opened Database successfully")


    try:
        Transform_df[0].to_sql("Albums", engine,index=False,if_exists="append")
    except:
        print("Data is already present")
    try:
        Transform_df[1].to_sql("Artists", engine,index=False,if_exists="append")
    except:
        print("Data is already present")


    conn.close()
    print("Connection Closed")