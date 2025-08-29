# Use an official lightweight Python image as the base
FROM python:3.9-slim-buster

# Set environment variables to prevent Python from writing .pyc files and to unbuffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements file first to leverage Docker caching
COPY requirements.txt /app/requirements.txt

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the entire application code into the container
COPY ./app.py /app/app.py
COPY /templates /app/template

# Expose the port your Flask application will run on (default Flask port is 5000)
EXPOSE 5000

# Command to run the Flask application when the container starts
CMD ["python", "app.py"]