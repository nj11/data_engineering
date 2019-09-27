# Project: Data Lake with Spark and S3.

## Introduction

Using the song and log datasets from a music streaming application, you'll need to create a star schema optimized for queries on song play analysis.
Application log data resides on the S3.Write ETL script that loads data from S3 , tranforms it using spark dataframes and then writes the
data back to S3 in parquest file format with the appropriate partitions.

## Instructions to run ETL

**In the template configuration file `dl.cfg` add the following information:**

```
[AWS]
AWS_ACCESS_KEY_ID       =<replace with your AWS access key ID>
AWS_SECRET_ACCESS_KEY   =<replace with your secret AWS access key>
INPUT_DATA              =<replace with your S3 input directory location>
OUTPUT_DATA             =<replace with your S3 output directory location>
```

Run the following command to trigger the ETL:

`python etl.py`

## Project structure

The files found at this project are the following:

- dl.cfg: Various configuration parameters used by the etl.py script. Replace AWS credentials here.
- etl.py: Extracts music app data log from s3 , performs transformations using spark and loads data back for analysis into s3.
- README.md: Documentation of the s3 and spark data pipeline etl process.

## ETL Data pipeline flow

1. Read AWS credentials from configuration file ( dl.cfg )
2. Extract the JSON log data from S3 which resides at the below location.
    - Song data: `s3a://udacity-dend-nj/song-data`
    - Log data: `s3a://udacity-dend-nj/log-data`

3. Transform data using spark.
   Create five different tables schema listed under section `Data Schema`.

4. Load it back to S3

    Write all the tables in S3 under separate analytics directories in parquet file format for further analysis.
    Songs table is partitioned by year and then artist. 
    Time table is partitioned by year and month. 
    Songplays table is partitioned by year and month.


### Source Data
- **Song datasets**: all json files are nested in subdirectories under *s3a://udacity-dend-nj/song-data*. A sample of this files is:

```
{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}
```

- **Log datasets**: all json files are nested in subdirectories under *s3a://udacity-dend-nj/log-data*. A sample of a single row of each files is:

```
{"artist":"Slipknot","auth":"Logged In","firstName":"Aiden","gender":"M","itemInSession":0,"lastName":"Ramirez","length":192.57424,"level":"paid","location":"New York-Newark-Jersey City, NY-NJ-PA","method":"PUT","page":"NextSong","registration":1540283578796.0,"sessionId":19,"song":"Opium Of The People (Album Version)","status":200,"ts":1541639510796,"userAgent":"\"Mozilla\/5.0 (Windows NT 6.1) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"","userId":"20"}
```
Input data has also been uploaded to the local /data/song_data and /data/log_data directory .

### Data Schema

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
