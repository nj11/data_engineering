import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    for query in insert_table_queries:
        print(query)
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')
    print("Connecting to the redshift database")

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    print("Successfully connected to the redshift database")
    print("Loading data in staging tables")
    load_staging_tables(cur, conn)
    print("Successfully loaded data in staging tables")
    print("Loading data in analytics tables")
    insert_tables(cur, conn)
    print("Script completed successfully")

    conn.close()


if __name__ == "__main__":
    main()