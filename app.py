from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import psycopg2
import os

app = FastAPI()

# Set up OpenAI API key
openai.api_key = 'your_openai_api_key'

# Connect to PostgreSQL using environment variables
conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST")
)
cursor = conn.cursor()

# Allow CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

def get_table_metadata(cursor):
    cursor.execute("""
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
    """)
    metadata = cursor.fetchall()
    return metadata

def text_to_sql(query_text, metadata):
    metadata_str = "\n".join([f"Table: {table}, Column: {column}, Data Type: {data_type}" for table, column, data_type in metadata])
    prompt = f"Convert the following text to SQL based on the table metadata:\n{metadata_str}\n\nQuery: {query_text}"
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    sql_query = response.choices[0].text.strip()
    return sql_query

@app.post("/query")
def query(request: QueryRequest):
    query_text = request.query
    metadata = get_table_metadata(cursor)
    sql_query = text_to_sql(query_text, metadata)
    cursor.execute(sql_query)
    results = cursor.fetchall()
    return {"results": results}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=80)