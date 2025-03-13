import pandas as pd
import psycopg2
import os

# Connect to PostgreSQL using environment variables
conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST")
)
cursor = conn.cursor()

# Read the Excel file
df = pd.read_excel('bank.xlsx')

# Create table if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS bank (
        id SERIAL PRIMARY KEY,
        column1 VARCHAR(100),
        column2 VARCHAR(100),
        column3 VARCHAR(100)
    );
""")

# Insert data into the table
for index, row in df.iterrows():
    cursor.execute("""
        INSERT INTO bank (column1, column2, column3)
        VALUES (%s, %s, %s)
    """, (row['column1'], row['column2'], row['column3']))

# Commit the transaction
conn.commit()

# Close the connection
cursor.close()
conn.close()