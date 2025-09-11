#!/bin/bash
set -e

# Install custom python packages if requirements.txt is present
if [ -e "/opt/airflow/requirements.txt" ]; then
    pip install --no-cache-dir -r /opt/airflow/requirements.txt
fi

# Initialize the database (only needed for first run)
# Since you're using Postgres, skip SQLite check
airflow db init

# Check if the environment variable for the password is set
if [ -z "${AIRFLOW_ADMIN_PASSWORD}" ]; then
    echo "ERROR: The AIRFLOW_ADMIN_PASSWORD environment variable is not set. This is required for security."
    echo "Please set it in your .env file and run again."
    exit 1
fi

# Create user using environment variables, with fallbacks for names/email
airflow users create \
    --username "${AIRFLOW_ADMIN_USERNAME:-admin}" \
    --firstname "${AIRFLOW_ADMIN_FIRSTNAME:-Admin}" \
    --lastname "${AIRFLOW_ADMIN_LASTNAME:-User}" \
    --role Admin \
    --email "${AIRFLOW_ADMIN_EMAIL:-admin@example.com}" \
    --password "${AIRFLOW_ADMIN_PASSWORD}"

# Always run the database upgrade command
airflow db upgrade

# Start the webserver
exec airflow webserver