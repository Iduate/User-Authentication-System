# Authentication Service

This is a Django-based authentication service with JWT authentication and password reset functionality using Redis.

## Features

- User registration and login with JWT authentication
- PostgreSQL database for user storage
- Password reset functionality with Redis token caching (with Django cache fallback)
- API documentation with Swagger/OpenAPI
- Docker support for local development
- Comprehensive unit tests for all main functionality
- Rate limiting on sensitive endpoints (login and password reset)

## Setup Instructions

### Using Docker (Recommended)

Docker provides the easiest way to get the service up and running with all dependencies.

1. Make sure you have Docker and Docker Compose installed on your system.

2. Clone the repository:
```bash
git clone https://github.com/yourusername/auth_service.git
cd auth_service
```

3. Start the services using Docker Compose:
```bash
# Using the standard Docker Compose setup
docker-compose up -d

# OR use the simpler setup (without building a custom image)
docker-compose -f docker-compose.simple.yml up -d
```

4. The service will be available at http://localhost:8000/
   - API Documentation: http://localhost:8000/swagger/

5. To view logs:
```bash
docker-compose logs -f web
```

6. To stop the services:
```bash
docker-compose down
```

### Local Development (Without Docker)

1. Clone the repository:
```bash
git clone https://github.com/yourusername/auth_service.git
cd auth_service
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the project root with the following variables:
```
SECRET_KEY=your-secret-key
DEBUG=True

# Database configuration
DATABASE_NAME=auth_db
DATABASE_USER=postgres
DATABASE_PASSWORD=your-db-password
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Redis configuration
REDIS_URL=redis://localhost:6379/0

# Note: If Redis is not available, the system will fall back to using Django's cache

# JWT settings
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
```

4. Create the database in PostgreSQL:
```bash
createdb auth_db
```

5. Apply migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

### Deployment

The application is configured for deployment on Railway or Render.

#### Environment Variables for Deployment

Set the following environment variables in your deployment platform:

- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to False for production
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

## API Documentation

The API documentation is available at:
- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`

## Running Tests

There are comprehensive unit tests for all main functionality including user registration, login, and password reset.

### Option 1: Run All Tests

```bash
# Without Docker
python manage.py test users

# With Docker
docker-compose run web python manage.py test users
```

### Option 2: Run Specific Test Modules

```bash
# Registration tests
python manage.py test users.tests.test_registration

# Login tests
python manage.py test users.tests.test_login

# Password reset tests
python manage.py test users.tests.test_password_reset
```

### Option 3: Use the Test Script (Unix/Linux/Mac)

```bash
# Make the script executable
chmod +x run_tests.sh

# Run the tests
./run_tests.sh
```

### Option 4: Run Tests in Docker

```bash
docker-compose run web python manage.py test users.tests.test_registration
docker-compose run web python manage.py test users.tests.test_login
docker-compose run web python manage.py test users.tests.test_password_reset
```

## Rate Limiting Protection

The service implements rate limiting on sensitive endpoints to protect against brute force attacks:

- **Login endpoint**: Limited to 5 attempts per minute
- **Password reset endpoints**: Limited to 3 attempts per hour

These limits can be adjusted in the settings.py file under the `REST_FRAMEWORK` configuration:

```python
'DEFAULT_THROTTLE_RATES': {
    'anon': '100/day',  # Default anonymous rate limit
    'user': '1000/day',  # Default authenticated user rate limit
    'login': '5/minute',  # Rate limit for login attempts
    'password_reset': '3/hour',  # Rate limit for password reset requests
}
```

### API Endpoints

#### Authentication

- `POST /api/v1/users/register/`: Register a new user
  - Request body: 
    ```json
    {
      "email": "user@example.com",
      "full_name": "John Doe",
      "password": "secure_password",
      "password_confirm": "secure_password"
    }
    ```
- `POST /api/v1/register/`: Alternative register endpoint
  - Request body: 
    ```json
    {
      "email": "user@example.com",
      "full_name": "John Doe",
      "password": "secure_password",
      "password_confirm": "secure_password"
    }
    ```

- `POST /api/v1/users/login/`: Log in with email and password
  - Request body:
    ```json
    {
      "email": "user@example.com",
      "password": "secure_password"
    }
    ```
- `POST /api/v1/login/`: Alternative login endpoint
  - Request body:
    ```json
    {
      "email": "user@example.com",
      "password": "secure_password"
    }
    ```

- `POST /api/v1/users/token/refresh/`: Refresh JWT token
  - Request body:
    ```json
    {
      "refresh": "your-refresh-token"
    }
    ```

#### User Profile

- `GET /api/v1/users/profile/`: Get user profile (requires authentication)
- `GET /api/v1/profile/`: Alternative endpoint for getting user profile (requires authentication)

#### Password Reset

- `POST /api/v1/users/password-reset/`: Request password reset
  - Request body:
    ```json
    {
      "email": "user@example.com"
    }
    ```
- `POST /api/v1/password-reset/`: Alternative endpoint for requesting password reset
  - Request body:
    ```json
    {
      "email": "user@example.com"
    }
    ```

- `POST /api/v1/users/password-reset/confirm/`: Confirm password reset
  - Request body:
    ```json
    {
      "token": "reset-token-from-email",
      "new_password": "new_secure_password",
      "new_password_confirm": "new_secure_password"
    }
    ```
- `POST /api/v1/password-reset/confirm/`: Alternative endpoint for confirming password reset
  - Request body:
    ```json
    {
      "token": "reset-token-from-email",
      "new_password": "new_secure_password",
      "new_password_confirm": "new_secure_password"
    }
    ```

## Rate Limiting

The application implements rate limiting on sensitive endpoints to prevent abuse:

- Login endpoints: 5 requests per minute per IP address
- Password reset endpoints: 3 requests per hour per IP address

This helps protect the application from brute force attacks and potential DoS attacks.

## Deployment Link

[Live Deployment](https://your-deployment-url.onrender.com)

## License

[MIT](LICENSE)
