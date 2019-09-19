# Project :

## Introduction

A music streaming apps data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.
Build a ETL pipeline that extracts the data from S3 stages it in AWS Redshift and transforms the data into a set of dimensional tables for analytics.

### Project Datasets

Song data: s3://udacity-dend/song_data
Log data: s3://udacity-dend/log_data
Log data json path: s3://udacity-dend/log_json_path.json

## Database Modelling

**Staging Tables **

![Alt desc](https://github.com/nj11/data_engineering/blob/master/CloudDataWarehouse/Cloud_DW_Modelling_and_ETL/screenshots/staging_tables.png)

**Analytics Tables **

![Alt desc](https://github.com/nj11/data_engineering/blob/master/CloudDataWarehouse/Cloud_DW_Modelling_and_ETL/screenshots/analytics_tables.png)

## Project structure

1. **create_redshift_cluster.py** - Infrastructure as a code python script to create Redsshift cluster and necessary IAM roles to reaD S3 buckets.
2. **delete_redshift_cluster.py** - Infrastructure as a code python script to delete AWS resources used for this project.
3. **create_tables.py** Python script to drop and recreate tables 
4. **sql_queries.py** Python script that contains all SQL queries used by create_tables.py
5. **etl.py** Python script contains ETL code to transfer data from s3 to staging tables and then from staging to analytics tables in redshift
6. **read_s3data.py** Python script contains code to demonstrate reading S3 data using python AWS SDK libraries
7. **dwh.cfg ** Configuration parameters for project are defined here
8. **Validate_etl_run_ipynb ** Notebook that tests ETL ran successfully by querying the analytics tables.
9.**README.md** Documentation for the project.

### To run the project.

 **Run  the below steps in exact same order.**
 
```python create_redshift_cluster.py ```

Wait for the cluster to complete creation and its in a healthy and ready state.Then move to the next step.

```python create_tables.py ```

```python etl.py ```

```Run the Validate_etl_run.ipynb notebook file to validate data in inserted properly by checking record counts ```

```python delete_redshift_cluster.py```





