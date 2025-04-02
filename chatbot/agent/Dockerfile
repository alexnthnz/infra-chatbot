# Use a lightweight official Python image.
FROM python:3.9-slim

# Set the working directory in the container.
WORKDIR /app

# Copy the requirements file and install dependencies.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container.
COPY . .

# Expose the port the app runs on.
EXPOSE 8080

# Run the application using Uvicorn.
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
