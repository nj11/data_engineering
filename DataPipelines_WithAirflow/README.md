# Project : Building a data pipeiline with S3 and Redshit and Apache Airflow

## Introduction
Sparkify application's source data resides in S3 and needs to be processed in Sparkify's data warehouse in Amazon Redshift. 
The source datasets consist of JSON logs that tell about user activity in the application and JSON metadata about the songs the users listen to.

### Source Data on S3
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
        session_id int - user session id
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
1.airflow/dags/redshift_load.py  Main ETL file

2.airflow/create_tables.sql Script file to create the necessary tables in Redshift

3.airflow/plugins/__init__.py

4.airflow/plugins/helpers/__init__.py

5.airflow/plugins/operators/__init__.py

6.airflow/plugins/sql_queries.py SQL queries used by the ETL pipeline built using airflow.

7.airflow/plugins/operators/data_quality.py Operator to perform data quality checks after ETL run is complete

8.airflow/plugins/operators/load_dimension.py Operrator to load data into dimension tables from staging tables

9.airflow/plugins/operators/load_fact.py  Operrator to load data into fact tables from staging tables

10.airflow/plugins/operators/stage_redshift.py Operator to load data

11.**README.md** Documentation for the project.

### Steps implemented to run this project.

 1. Create  a redshift cluster in AWS console.

 2. Download AWS credentials ( secret key and password ) in AWS console.

 3.Start the airflow web server.

 4.Create a connection in Apache Airflow UI named aws_credentials

![Alt desc](https://github.com/nj11/data_engineering/blob/master/DataModelling/Postgresql-Modelling_and_ETL/screenshots/aws_connection.png)


 5.Create a connection in Apache Aifflow UI named redshift


![Alt desc](https://github.com/nj11/data_engineering/blob/master/DataModelling/Postgresql-Modelling_and_ETL/screenshots/redshift_connection.png)


 6.Write and run the  SQL airflow/create_tables.sql  to create the necessary tables in redshift


 7.Implement the ETL pipeline using reusable operators to load data from s3 to staging tables in redshift ( stage_redshift.py),
  from staging to the fact tables(load_fact.py), from fact to the dimension tables(load_dimension.py) and finally to perform the quality   checks after ETL ( data_quality.py)
  
 
 8.Implement the main ETL under the airflow/dags/redshift_load.py directory using these operators ( Step 7).Make sure the dependencies     between all the steps works as expected.

  
  ![Alt desc](https://github.com/nj11/data_engineering/blob/master/DataModelling/Postgresql-Modelling_and_ETL/screenshots/redshift_connection.png)


 9.Test the ETL run on Apache Airflow to make sure all tasks completed successfully.If tasks fail check Airflow logs for details.

![Alt desc](https://github.com/nj11/data_engineering/blob/master/DataModelling/Postgresql-Modelling_and_ETL/screenshots/dag_run.png)




