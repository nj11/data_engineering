# Project : Data Modeling with Apache Cassandra and ETL pipeline with Python. 

## Introduction

Analyze the songs and user activity data generated by the Sparkify music streaming app. The data is generated in a csv file.

### Data
- **Song  and user activity datasets**: CSV file event_datafile_new.csv **. 


![Alt desc](https://github.com/nj11/data_engineering/blob/master/DataModelling/Cassandra-Modelling_and_ETL/images/image_event_datafile_new.jpg)


## Database Modelling

3 types of searches need to be performed on the Apache Cassandra tables.

**Query 1** : Search the music app history logs for artist and song details that was heard during a particular session and item in session.

**Query 2** : Search music app history logs for ame of artist, song (sorted by itemInSession) and user (first and last name) by userid and session ID.

**Query 3** : Search music app history logs for user first and last name who listened to a particular song.

### Tables created in Apache Cassandra
**musichistory_searchby_itemsession TABLE - Supports Query 1**  
        PRIMARY KEY IS sessionId (partition key) and itemInSession (clustering key)
        sessionId int  - session ID
        itemInSession int - item in session
        artist text - artist of the song
        song_title text - song title
        song_length float - song duration
        
**musichistory_searchby_usersession TABLE - Supports Query 2**  
        PRIMARY KEY((userId, sessionId), itemInSession))  userId and  sessionId = Partition Key itemInSession = CLUSTERING key         for sorting.
        userId int  - User ID
        itemInSession int - item in session
        song text -  song being played
        firstName text - user first name
        lastName text - user last name

**musichistory_searchby_song TABLE - Supports Query 3**  
        PRIMARY KEY(song, userId)  song and  userId = Partition Key
        song text - song being played
        userId int - user playing song
        firstName text - user firstname
        lastName text - user lastname
        
## Project structure
1. **images/image_event_datafile_new.jpg**  CSV sample data structure and format.
2. **event_datafile_new.csv** CSV that contains music streaming apps log data ( This is in turn generated from /event_data).
3. **create_tables.py** Python script to drop and recreate tables .This is run first before you run the ETL script
4. **Project_1B_ Project_Template.ipynb** Test script that creates Cassandra tables and performs ETL via python from logs files into these tabless.
5.**README.md** Documentation for the project.

### To run the project.
1. Run Project_1B_ Project_Template.ipynb Jupyter Notebook to verify that all the tables are created and populated properly.


