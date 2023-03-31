# Use an official Python runtime as a parent image
FROM python:3.7-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required packages
RUN pip3 install --no-cache-dir -r requirements.txt
# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run Gunicorn server to serve your Flask app
CMD ["gunicorn", "-b", "0.0.0.0:80", "app:app"]
