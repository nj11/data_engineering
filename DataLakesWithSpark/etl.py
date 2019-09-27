import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col,monotonically_increasing_id
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format
from pyspark.sql.types import StructType,StructField,DoubleType,StringType,IntegerType,TimestampType

config = configparser.ConfigParser()
config.read('dl.cfg')
print('Reading config files')

os.environ['AWS_ACCESS_KEY_ID']=config.get('AWS', 'AWS_ACCESS_KEY_ID')
os.environ['AWS_SECRET_ACCESS_KEY']=config.get('AWS', 'AWS_SECRET_ACCESS_KEY')

def create_spark_session():
    ''' Create SPARK session for the ETL pipeline'''
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark

def process_song_data(spark, input_data, output_data):
    ''' Method to process SONG JSON log data  from input path and write it to the output 
        directory as PARQUET files.
    '''
    print("Processing song JSON data.")
    
    songSchema = StructType([
        StructField("artist_id",StringType()),
        StructField("artist_latitude",DoubleType()),
        StructField("artist_location",StringType()),
        StructField("artist_longitude",DoubleType()),
        StructField("artist_name",StringType()),
        StructField("duration",DoubleType()),
        StructField("num_songs",IntegerType()),
        StructField("title",StringType()),
        StructField("year",IntegerType()),
        StructField("song_id",StringType())
    ])
    
    # read song data file into spark data frame.
    df = spark.read.json(input_data,songSchema) 
    
    # print schema for the song JSON data.
    print("1.Printing song  JSON file schema....")
    df.printSchema()

    # extract columns to create songs table
    df.createOrReplaceTempView("songs_table")
    songs_table = spark.sql("""
        SELECT distinct song_id, title, artist_id, year, duration
        FROM songs_table
        ORDER BY song_id
    """)
    
    print("2.Printing song table schema....")
    songs_table.printSchema()
    
    # write songs table to parquet files partitioned by year and artist
    print("3.Writing song data to output parquet files partitioned by year and artist.........")
    song_data_output_path = output_data + "song_data_parquet" 
    songs_table.write.format('parquet').mode('overwrite').partitionBy("year", "artist_id").save(song_data_output_path)

    # extract columns to create artists table
    artists_table = spark.sql("""
        SELECT distinct artist_id        AS artist_id,
                artist_name      AS name,
                artist_location  AS location,
                artist_latitude  AS latitude,
                artist_longitude AS longitude
        FROM songs_table
        ORDER BY artist_id desc
    """) 
    
    print("4.Printing artists tables chema....")
    artists_table.printSchema()
    
    # write artists table to parquet files
    print("5.Writing artists data to output parquet files ......")
    artitsts_data_output_path = output_data + "artists_data_parquet" 
    artists_table.write.format('parquet').mode('overwrite').save(artitsts_data_output_path)
    print("Song JSON input data successfully processed.")
    
    return songs_table,artists_table

def process_log_data(spark, log_input_data, song_input_data,output_data):
    ''' Process app event JSON logs and extract and load user,time and songplays data into S3'''
    print("Processing input log data JSON files.")

    # read log data file
    df = spark.read.json(log_input_data)
    print("1.Printing schema for log JSON data...")
    df.printSchema()
    
    # filter dataframe by actions for song plays
    df_filtered = df.filter(df.page == 'NextSong') 

    # extract columns for users table 
    df_filtered.createOrReplaceTempView("users_table")
    
    users_table = spark.sql("""
        SELECT  DISTINCT userId    AS user_id,
                         firstName AS first_name,
                         lastName  AS last_name,
                         gender,
                         level
        FROM users_table
        ORDER BY last_name
    """)
    
    print("2.Printing user table schema.....")
    users_table.printSchema()
    
    # write users table to parquet files
    print("3.Writing users table to parquet files....")
    users_data_output_path = output_data + "users_data_parquet" 
    users_table.write.format('parquet').mode('overwrite').save(users_data_output_path)

    # extract columns to create time table
    df_filtered.createOrReplaceTempView("time_table")
    
    # write time table to parquet files partitioned by year and month
    time_table = spark.sql("""
        SELECT  DISTINCT to_timestamp(ts/1000) AS start_time,
                         hour(to_timestamp(ts/1000)) AS hour,
                         day(to_timestamp(ts/1000))  AS day,
                         weekofyear(to_timestamp(ts/1000)) AS week,
                         month(to_timestamp(ts/1000)) AS month,
                         year(to_timestamp(ts/1000)) AS year,
                         dayofweek(to_timestamp(ts/1000)) AS weekday
                         
        FROM time_table
        ORDER BY start_time
    """)
    
    print("4.Time table schema....")
    time_table.printSchema()
    
    print("5.Saving time table data to parquet files....")
    time_data_output_path = output_data + "time_data_parquet" 
    time_table.write.format('parquet').mode('overwrite').partitionBy("year","month").save(time_data_output_path)

    # read in song data to use for songplays table
    print("6.Reading song data files for use in song plays table....")
    df_songs = spark.read.parquet(output_data + 'song_data_parquet')
    song_logs=df_songs.join(df_filtered,df_songs.title==df_filtered.song)
    
    # extract columns from joined song and log datasets to create songplays table 
    # Add a  unique ID to each row
    song_logs = song_logs.withColumn("songplay_id",monotonically_increasing_id())
    song_logs.createOrReplaceTempView("songplays_table")
    
    songplays_table = spark.sql("""
        SELECT  songplay_id AS songplay_id,
                to_timestamp(ts/1000) AS start_time,
                month(to_timestamp(ts/1000)) as month,
                year(to_timestamp(ts/1000)) as year,
                userId      AS user_id,
                level       AS level,
                song_id     AS song_id,
                artist_id   AS artist_id,
                sessionId   AS session_id,
                location    AS location,
                userAgent   AS user_agent
        FROM songplays_table
        ORDER BY (user_id, session_id)
    """)
    
    
    print('7.Song plays table schema...')
    songplays_table.printSchema()
    
    # write songplays table to parquet files partitioned by year and month
    songplays_table_output_path = output_data + "songplays_data_parquet" 
    songplays_table.write.format('parquet').mode('overwrite').partitionBy("year","month").save(songplays_table_output_path)
    
    return users_table,time_table,songplays_table

    
def main():
    ''' Create spark session.Load music apps json log data from S3, transform it using spark dataframes and then load results back into S3'''
    spark = create_spark_session()
    print("Spark session successfully created.")
    
    #Uncomment to run etl on local ..
    #input_song_data=config.get('LOCAL', 'INPUT_SONG_DATA')
    #input_log_data=config.get('LOCAL', 'INPUT_LOG_DATA')
    #output_data=config.get('LOCAL', 'OUTPUT_DATA')
    
    #Run on S3
    input_data=config.get('AWS', 'INPUT_DATA')
    input_song_data=input_data+'song-data/*/*/*/*.json'
    input_log_data = input_data + 'log-data/*.json'
    output_data=config.get('AWS', 'OUTPUT_DATA')
   
    songs_table, artists_table=process_song_data(spark, input_song_data, output_data)    
    users_table,time_table,songplays_table=process_log_data(spark, input_log_data, input_song_data,output_data)
    print("ETL script completed successfully")


if __name__ == "__main__":
    main()
