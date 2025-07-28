#Deployment Instructions

# Start from an official Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application code into the container
COPY app.py .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application using the gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]