FROM python:3.9-slim

WORKDIR /app

COPY . /app
COPY bank.xlsx /app/bank.xlsx
COPY env.py /app/env.py
COPY diagram.mmd /app/diagram.mmd

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y postgresql-client

EXPOSE 80

CMD ["sh", "-c", "python wait_for_postgres.py && python load_data.py && uvicorn app:app --host 0.0.0.0 --port 80"]