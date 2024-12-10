# Start from a lightweight Python base image
FROM python:3.9-slim

# Update apt-get and install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Set the command to run the application with gunicorn, listening on the port Render provides
# Render expects your app to listen on port 8080 by default
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080"]
