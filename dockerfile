# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy the Excel file into the container
COPY bank.xlsx /app/bank.xlsx

# Copy the env.py file into the container
COPY env.py /app/env.py

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["sh", "-c", "python wait_for_postgres.py && python load_data.py && uvicorn app:app --host 0.0.0.0 --port 80"]