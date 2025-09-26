# Here we are using the official Python image from the Docker Hub
FROM python:3.8-slim-buster 

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Executing the application (app.py) when the container starts
CMD ["python", "app.py"]
