#!/bin/bash
set -e

# Install custom python packages if requirements.txt is present
if [ -e "/opt/airflow/requirements.txt" ]; then
    pip install --no-cache-dir -r /opt/airflow/requirements.txt
fi

# Initialize the database (only needed for first run)
airflow db init

# Check if the environment variable for the password is set
if [ -z "${AIRFLOW_ADMIN_PASSWORD}" ]; then
    echo "ERROR: The AIRFLOW_ADMIN_PASSWORD environment variable is not set. This is required for security."
    exit 1
fi

# Create user if not already created
airflow users create \
    --username "${AIRFLOW_ADMIN_USERNAME:-admin}" \
    --firstname "${AIRFLOW_ADMIN_FIRSTNAME:-Admin}" \
    --lastname "${AIRFLOW_ADMIN_LASTNAME:-User}" \
    --role Admin \
    --email "${AIRFLOW_ADMIN_EMAIL:-admin@example.com}" \
    --password "${AIRFLOW_ADMIN_PASSWORD}" || true

# Upgrade DB schema
airflow db upgrade


exec airflow "$@"
