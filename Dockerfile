
# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy only the dependency definition files to leverage Docker cache
COPY pyproject.toml poetry.lock* ./

# Install project dependencies
RUN poetry config virtualenvs.create false && poetry install --without dev --no-interaction --no-ansi

# Copy the rest of the application code
COPY . .

# Make scripts executable
RUN chmod +x /app/scripts/*.sh

# Expose the port the app runs on
EXPOSE 8081

# Command to run the application
CMD ["make", "run"]
