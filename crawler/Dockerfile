# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Install PostgreSQL development files
RUN apt-get update && apt-get install -y libpq-dev gcc && apt-get clean

# Copy the current directory contents into the container at /app
COPY requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

ADD . /app

# Run app.py when the container launches
CMD ["python", "crawl.py"]
