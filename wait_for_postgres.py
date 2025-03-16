import time
import psycopg2
import os

while True:
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST")
        )
        conn.close()
        break
    except psycopg2.OperationalError:
        print("Waiting for PostgreSQL to be ready...")
        time.sleep(2)