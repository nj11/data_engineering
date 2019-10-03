from datetime import datetime, timedelta
import os
from airflow import DAG #DAG object used to instantiate a DAG.
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,
                                LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries

#default_args = {
    #'owner': 'udacity',
    #'start_date': datetime.datetime.now()
    #'depends_on_past': False, #dag doesnt have dependencies on past runs.
    #'retries': 1, 
    #'retry_delay': timedelta(seconds=300), #retries happen every 5 mins
    #'catchup': False  #catch up is turned off.
#}

dag = DAG(
        'redshift_data_load',
        start_date=datetime.now())

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)


stage_events_to_redshift = StageToRedshiftOperator(
    task_id='Stage_events',
    dag=dag,
    table = "staging_events",
    s3_path = "s3://udacity-dend/log_data",
    redshift_conn_id="redshift",
    aws_conn_id="aws_credentials",
    region_name="us-west-2",
    json_path="s3://udacity-dend/log_json_path.json",
)

stage_songs_to_redshift = StageToRedshiftOperator(
    task_id='Stage_songs',
    dag=dag,
    table = "staging_songs",
    s3_path = "s3://udacity-dend/song_data",
    redshift_conn_id="redshift",
    aws_conn_id="aws_credentials",
    region_name="us-west-2",
    json_path="auto"
)

load_songplays_table = LoadFactOperator(
    task_id='Load_songplays_fact_table',
    dag=dag,
    table='songplays',
    redshift_conn_id="redshift",
    load_sql_stmt=SqlQueries.songplay_table_insert
)

load_user_dimension_table = LoadDimensionOperator(
    task_id='Load_user_dim_table',
    dag=dag,
    table='users',
    redshift_conn_id="redshift",
    load_sql_stmt=SqlQueries.user_table_insert,
    insert_mode="truncate_insert"
)

load_song_dimension_table = LoadDimensionOperator(
    task_id='Load_song_dim_table',
    dag=dag,
    table='songs',
    redshift_conn_id="redshift",
    load_sql_stmt=SqlQueries.song_table_insert,
    insert_mode="truncate_insert"
)

load_artist_dimension_table = LoadDimensionOperator(
    task_id='Load_artist_dim_table',
    dag=dag,
    table='artists',
    redshift_conn_id="redshift",
    load_sql_stmt=SqlQueries.artist_table_insert,
    insert_mode="truncate_insert"
)

load_time_dimension_table = LoadDimensionOperator(
    task_id='Load_time_dim_table',
    dag=dag,
    table='time',
    redshift_conn_id="redshift",
    load_sql_stmt=SqlQueries.time_table_insert,
    insert_mode="truncate_insert"
)


run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag,
    tables=['songplays', 'users', 'songs', 'artists', 'time'],
    redshift_conn_id="redshift"
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

# Load data from JSON logs in s3 to staging tables in redshift
start_operator >> stage_events_to_redshift
start_operator >> stage_songs_to_redshift

# Load data from staging tables in redshift to the songplays fact table.
stage_events_to_redshift >> load_songplays_table
stage_songs_to_redshift >> load_songplays_table

# Load the dimensions table from the songplays table in redshift
load_songplays_table >> load_song_dimension_table
load_songplays_table >> load_user_dimension_table
load_songplays_table >> load_artist_dimension_table
load_songplays_table >> load_time_dimension_table


# Run quality checks to see if data exists after etl finishes.
#Quality checks will only run after all fact and dimension tables are loaded.
load_song_dimension_table >> run_quality_checks
load_user_dimension_table >> run_quality_checks
load_artist_dimension_table >> run_quality_checks
load_time_dimension_table >> run_quality_checks


# Run the END task once the quality checks are complete.
run_quality_checks >> end_operator

