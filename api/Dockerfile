# Start from an official Python base image (e.g., python:3.9-slim).
FROM python:3.9-slim

# Set a working directory inside the container (e.g., /app).
WORKDIR /code

# Copy the requirements.txt file into the container.
COPY requirements.txt /code/

# Install the dependencies.
RUN pip install --no-cache-dir -r /code/requirements.txt

# Copy the rest of the application code into the container.
COPY . /code/

# Run the application.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]