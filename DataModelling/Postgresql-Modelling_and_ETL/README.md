# Project : Data Modeling with Postgres and building an ETL pipeline with Python.

## Introduction

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. 
The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

This project creates a Postgres database with tables designed to optimize queries on song play analysis.It creates a database schema and ETL pipeline in python for this analysis.

### Data
- **Song datasets**: JSON files under this location */data/song_data*. Sample song JSON file is shown below:

```
{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}
```

- **Log datasets**: JSOM files under this location */data/log_data*.  Sample log JSON file is shown below:

```
{"artist":"Slipknot","auth":"Logged In","firstName":"Aiden","gender":"M","itemInSession":0,"lastName":"Ramirez","length":192.57424,"level":"paid","location":"New York-Newark-Jersey City, NY-NJ-PA","method":"PUT","page":"NextSong","registration":1540283578796.0,"sessionId":19,"song":"Opium Of The People (Album Version)","status":200,"ts":1541639510796,"userAgent":"\"Mozilla\/5.0 (Windows NT 6.1) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"","userId":"20"}
```

## Database Schema
The schema used for this exercise is the Star Schema:
https://en.wikipedia.org/wiki/Star_schema

There is one main fact table containing all the data associated to each user play song event , 
and 4 dimentional tables, each with a primary key that is being referenced from the fact table.

#### Fact Table
**SONGPLAYS TABLE** - records the log data associated with song plays 
        songplay_id int PRIMARY KEY  - ID of each user song play
        start_time date - start time of song play.
        user_id int - user id
        level text - user level ( Free or paid)
        song_id text  - ID of the song being played
        artist_id text - Artist ID of the song played
        session_id text - user session id
        location text -- user location
        user_agent text - user agent used for the sparkify platform
        
#### Dimension Tables
   
**USERS TABLE** - users of the app
 user_id int PRIMARY KEY - user id
    first_name text - user first name
    last_name text - user last name
    gender text - gender
    level text -- user level i.e free or paid

**SONGS TABLE** - songs available to play in the app.
    song_id text PRIMARY KEY - song id
    title text NOT NULL - song title
    artist_id text  - artist id of the song.
    year int - year the song was released
    duration float - duration of the song in milliseconds.
                        

**ARTISTS TABLE** - artists of all the songs available for play in the app.
 artist_id text PRIMARY KEY - artist ID
 name text  - artist name
 location text - artist location
 latitude float - Latitude of artist location
 longitude float - Longitude of artist location

**TIME TABLE** - time information of songs played broken down into different units.
    start_time date PRIMARY KEY - start time of the song played
    hour int - Hour component of time
    day int -Day component of time
    week int - Week component of time
    month int -Month component of the time
    year int - Year component of the time
    weekday text - Weekday eg.Mon,Tue etc


## Project structure


1. **data**  JSON data lives here.
2. **sql_queries.py** Pythpn script that contains SQL queries .
3. **create_tables.py** Python script to drop and recreate tables .This is run first before you run the ETL script
4. **test.ipynb** Test script to run after tables are created and when data is inserted to check the database.Display first n rows in each table.
5. **etl.ipynb** Test script to load sample data from JSON files to postgres table. 
6. **etl.py** Python script to ETL app json data into postgres tables.
7. **README.md** Documentation for the project.

### Steps implemented to finish this project.

1. Write all the create,drop and select queries sql_queries.py

2. Run create_table script in console
 ```
python create_tables.py
```

![Alt desc](https://github.com/nj11/data_engineering/blob/master/DataModelling/Postgresql-Modelling_and_ETL/screenshots/screenshot1.png)

3. Run test.ipynb Jupyter Notebook to verify that all the tables from step 2 were created properly.

![Alt desc](https://github.com/nj11/data_engineering/blob/master/DataModelling/Postgresql-Modelling_and_ETL/screenshots/screenshot2.png)

4. Write the etl.ipynb Jupyter Notebook to create the blueprint for ETL pipeline to insert data from JSON logs to postgres database.

5. Write the ET scriptand run the etl in console, and verify results by running the test.ipynb Jupyter Notebook.
 ```
python etl.py
```
![Alt desc](https://github.com/nj11/data_engineering/blob/master/DataModelling/Postgresql-Modelling_and_ETL/screenshots/screenshot3.png)

![Alt desc](https://github.com/nj11/data_engineering/blob/master/DataModelling/Postgresql-Modelling_and_ETL/screenshots/screenshot4.png)




