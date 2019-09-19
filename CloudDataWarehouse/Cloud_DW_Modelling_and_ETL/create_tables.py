import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    #jdbc:redshift://dwhcluster.cujsz8dz5egu.us-west-2.redshift.amazonaws.com:5439/dwh
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    #con=psycopg2.connect("dbname = dwh, host=cujsz8dz5egu.us-west-2.redshift.amazonaws.com, port= 5439, user=dwhuser, password= Passw0rd")
    cur = conn.cursor()
    print("DB connection successful");
    print("Dropping existing tables on redshift cluster.");
    drop_tables(cur, conn)
    print("Creating  tables on redshift cluster.");
    create_tables(cur, conn)

    conn.close()
    print("Script run completed successfully.");


if __name__ == "__main__":
    main()