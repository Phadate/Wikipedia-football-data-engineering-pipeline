#!/bin/bash
set -e

# Install custom python packages if requirements.txt is present
if [ -e "/opt/airflow/requirements.txt" ]; then
    $(command -v pip) install --user -r requirements.txt
fi

# Initialize the database if it hasn't been initialized yet
if [ ! -f "/opt/airflow/airflow.db" ]; then
  airflow db init

  # Check if the environment variable for the password is set.
  # If not, throw a massive error and stop the container because it's insecure.
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
    --password "${AIRFLOW_ADMIN_PASSWORD}" # This one has no fallback and is required.
fi

# Always run the database upgrade command
$(command -v airflow) db upgrade

# Start the webserver
exec airflow webserverSc