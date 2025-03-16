import pandas as pd
import psycopg2
import os
from env import *

# Connect to PostgreSQL using environment variables
conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST")
)
cursor = conn.cursor()

# Read the Excel file
df_dtl = pd.read_excel('bank.xlsx',sheet_name='Detail')

df_meta = pd.read_excel('bank.xlsx',sheet_name='Meta')

df_segment = pd.read_excel('bank.xlsx',sheet_name='Segment')

# Create table if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS bank_transactions (
        account_no VARCHAR(20),
        date DATE,
        transaction_details VARCHAR(255),
        chq_no VARCHAR(20),
        value_date DATE,
        withdrawal_amt NUMERIC,
        deposit_amt NUMERIC,
        balance_amt NUMERIC
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS cus_segment (
        account_no VARCHAR(20),
        segment VARCHAR(20)
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS metadata_ (
        DATAELEMENT VARCHAR(20),
        TABLE_NAME VARCHAR(20),
        COLUMN_NAME VARCHAR(20),
        SCHEMA_NAME VARCHAR(20),
        DATATYPE VARCHAR(20),
        SOURCE_FIELD VARCHAR(20),
        SOURCE_TABLE VARCHAR(20),
        SOURCE_SYSTEM VARCHAR(20),
        MAPPING_RULE VARCHAR(20),
        OWNER VARCHAR(20)
    );
""")


# Insert data into the table
for index, row in df_dtl.iterrows():
    cursor.execute("""
        INSERT INTO bank_transactions (account_no, date, transaction_details, chq_no, value_date, withdrawal_amt, deposit_amt, balance_amt)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        row['ACCOUNT NO'],
        row['DATE'],
        row['TRANSACTION DETAILS'],
        row['CHQ.NO.'],
        row['VALUE DATE'],
        row['WITHDRAWAL AMT'],
        row['DEPOSIT AMT'],
        row['BALANCE AMT']
    ))

for index, row in df_meta.iterrows():
    cursor.execute("""
        INSERT INTO metadata_ (DATAELEMENT, TABLE_NAME, COLUMN_NAME, SCHEMA_NAME, DATATYPE, SOURCE_FIELD, SOURCE_TABLE, SOURCE_SYSTEM, MAPPING_RULE, OWNER)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        row['DATAELEMENT'],
        row['TABLE_NAME'],
        row['COLUMN_NAME'],
        row['SCHEMA_NAME'],
        row['DATATYPE'],
        row['SOURCE_FIELD'],
        row['SOURCE_TABLE'],
        row['SOURCE_SYSTEM'],
        row['MAPPING_RULE'],
        row['OWNER']
    ))

for index, row in df_segment.iterrows():
    cursor.execute("""
        INSERT INTO metadata_ (ACCOUNT_NO,SEGMENT)
        VALUES (%s, %s)
    """, (
        row['ACCOUNT_NO'],
        row['SEGMENT']
    ))


# Commit the transaction
conn.commit()

# Close the connection
cursor.close()
conn.close()