#!/bin/bash
set -e

# Run all tests with verbose output
echo "Running all tests..."
python manage.py test users.tests

# Run specific test modules
echo -e "\nRunning registration tests..."
python manage.py test users.tests.test_registration

echo -e "\nRunning login tests..."
python manage.py test users.tests.test_login

echo -e "\nRunning password reset tests..."
python manage.py test users.tests.test_password_reset

echo -e "\nAll tests completed successfully!"
