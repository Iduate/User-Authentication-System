#!/bin/bash
set -e

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
while ! pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER 2>/dev/null
do
  echo "PostgreSQL not ready yet... waiting"
  sleep 2
done

echo "PostgreSQL is ready!"

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Create superuser if doesn't exist
echo "Checking if superuser exists..."
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(email='admin@example.com').exists():
    User.objects.create_superuser('admin@example.com', 'Admin User', 'adminpassword');
    print('Superuser created.');
else:
    print('Superuser already exists.');
"

# Start the server
echo "Starting server..."
exec python manage.py runserver 0.0.0.0:8000
