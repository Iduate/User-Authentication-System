#!/bin/bash

# Set default port if PORT is not set
PORT=${PORT:-8000}

echo "Starting gunicorn on port $PORT"

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser if it doesn't exist
python create_superuser.py

# Start gunicorn
exec gunicorn --bind 0.0.0.0:$PORT --workers 3 --timeout 120 auth_service.wsgi:application
