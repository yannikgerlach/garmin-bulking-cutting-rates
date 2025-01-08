# Use an official Python runtime as a parent image
FROM python:3.12-slim

# install poetry dependencies in project
ENV POETRY_VIRTUALENVS_CREATE=false

# Set the working directory in the container
WORKDIR /scripts

# Copy the current directory contents into the container at /scripts
COPY . /scripts

# Copy the run.sh script into the container and make it executable
COPY run.sh /run.sh
RUN chmod +x /run.sh

# Install Poetry
RUN pip install poetry

# Install dependencies
RUN poetry install

# Create environment variables placeholders that will be provided at runtime
ENV GARMIN_EMAIL=""
ENV GARMIN_PASSWORD=""
ENV TARGET_WEEKLY_CHANGE_PERCENTAGE=""
ENV MAKE_API_KEY=""
ENV WEBHOOK_URL=""

# Run the run.sh --send script when the container launches
CMD ["/run.sh", "--send"]
