@echo off
echo Running all tests...
python manage.py test users.tests

echo.
echo Running registration tests...
python manage.py test users.tests.test_registration

echo.
echo Running login tests...
python manage.py test users.tests.test_login

echo.
echo Running password reset tests...
python manage.py test users.tests.test_password_reset

echo.
echo All tests completed successfully!
