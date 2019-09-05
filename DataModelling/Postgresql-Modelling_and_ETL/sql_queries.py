# DROP TABLES

songplay_table_drop = "drop table if exists songplays"
user_table_drop = "drop table if exists users"
song_table_drop = "drop table if exists songs"
artist_table_drop = "drop table if exists artists"
time_table_drop = "drop table if exists time"

# CREATE TABLES

songplay_table_create = (""" 
create table IF NOT EXISTS songplays( 
        songplay_id int PRIMARY KEY, 
        start_time date , 
        user_id int REFERENCES users(user_id), 
        level text ,
        song_id text REFERENCES songs(song_id) ,
        artist_id text ,
        session_id text ,
        location text,
        user_agent text
  ) 
""")

user_table_create = (""" 
    create table IF NOT EXISTS users(
    user_id int PRIMARY KEY,
    first_name text NOT NULL,
    last_name text NOT NULL,
    gender text NOT NULL,
    level text
    )
""")

song_table_create = (""" create table IF NOT EXISTS songs (
                        song_id text PRIMARY KEY , 
                        title text NOT NULL,
                        artist_id text ,
                        year int,
                        duration float
                        )
""")

artist_table_create = (""" create table IF NOT EXISTS artists(
                           artist_id text PRIMARY KEY, 
                           name text NOT NULL,
                           location text,
                           latitude float,
                           longitude float
                           )
""")

time_table_create = (""" create table IF NOT EXISTS time (
                            start_time date PRIMARY KEY ,
                            hour int,
                            day int,
                            week int ,
                            month int,
                            year int ,
                            weekday text
                        )
""")

# INSERT RECORDS
#Implement Upsert using on conflict clause.DO nothing if row already exists in the table.

songplay_table_insert = ("""
    INSERT INTO songplays
    (songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (songplay_id) DO NOTHING;  
""")

user_table_insert = ("""
    INSERT INTO users
    (user_id, first_name, last_name, gender, level)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (user_id) DO NOTHING;  
""")

song_table_insert = ("""
    INSERT INTO songs
    (song_id, title, artist_id, year, duration)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (song_id) DO NOTHING;  
    
""")

artist_table_insert = ("""
    INSERT INTO artists
    (artist_id, name, location, latitude, longitude)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (artist_id) DO NOTHING;  
""")

time_table_insert = ("""
    INSERT INTO time
    (start_time, hour, day, week, month, year, weekday)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
     ON CONFLICT (start_time) DO NOTHING;
""")

# FIND SONGS

song_select = ("""
    SELECT song_id, artists.artist_id
    FROM songs JOIN artists ON songs.artist_id = artists.artist_id
    WHERE songs.title = %s
    AND artists.name = %s
    AND songs.duration = %s
""")

# QUERY LISTS

create_table_queries = [user_table_create, artist_table_create, song_table_create, time_table_create, songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]