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

df_account = pd.read_excel('bank.xlsx',sheet_name='CusAccount')

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
        account_no VARCHAR(200),
        segment VARCHAR(200)
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS metadata_ (
        DATAELEMENT VARCHAR(200),
        TABLE_NAME VARCHAR(200),
        COLUMN_NAME VARCHAR(200),
        SCHEMA_NAME VARCHAR(200),
        DATATYPE VARCHAR(200),
        SOURCE_FIELD VARCHAR(200),
        SOURCE_TABLE VARCHAR(200),
        SOURCE_SYSTEM VARCHAR(200),
        MAPPING_RULE VARCHAR(200),
        OWNER VARCHAR(200)
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS cus_account (
        cus varchar(200),
        account_no VARCHAR(200),
        status VARCHAR(200)
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
        INSERT INTO cus_segment (ACCOUNT_NO,SEGMENT)
        VALUES (%s, %s)
    """, (
        row['ACCOUNT NO'],
        row['SEGMENT']
    ))

for index, row in df_account.iterrows():
    cursor.execute("""
        INSERT INTO cus_account (CUS, ACCOUNT_NO,STATUS)
        VALUES (%s,%s, %s)
    """, (
        row['CUS'],
        row['ACCOUNT NO'],
        row['STATUS']
    ))


# Commit the transaction
conn.commit()

# Close the connection
cursor.close()
conn.close()