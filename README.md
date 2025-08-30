# User Authentication System

A simple, secure Django REST API for user authentication with JWT tokens.

## What it does

- User registration and login
- JWT token authentication 
- Password reset functionality
- Rate limiting for security
- PostgreSQL database with Redis caching

## Quick Start

**Using Docker (easiest way):**
```bash
git clone https://github.com/Iduate/User-Authentication-System.git
cd User-Authentication-System/auth_service
docker-compose up -d
```

**Access your API:**
- API: http://localhost:8000/api/v1/
- Documentation: http://localhost:8000/swagger/
- Admin: http://localhost:8000/admin/

## API Endpoints

### Register a new user
```
POST /api/v1/users/register/
{
  "email": "user@example.com",
  "full_name": "John Doe", 
  "password": "SecurePassword123!",
  "password_confirm": "SecurePassword123!"
}
```

### Login
```
POST /api/v1/users/login/
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

### Get user profile
```
GET /api/v1/users/profile/
Headers: Authorization: Bearer <your-token>
```

### Reset password
```
POST /api/v1/users/password-reset/
{
  "email": "user@example.com"
}
```

## Local Development

**Requirements:** Python 3.11+, PostgreSQL, Redis (optional)

```bash
# Setup
git clone https://github.com/Iduate/User-Authentication-System.git
cd User-Authentication-System/auth_service
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Database
createdb auth_db
python manage.py migrate
python manage.py createsuperuser

# Run
python manage.py runserver
```

## Environment Variables

Create a `.env` file:
```env
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://user:password@localhost/auth_db
REDIS_URL=redis://localhost:6379/0  # optional
DEBUG=True
```

## Testing

```bash
python manage.py test users
```

## Production Deployment

Works with Railway, Render, Heroku, or any platform supporting Django.

## Need Help?

- Check the [API docs](http://localhost:8000/swagger/) for detailed endpoint information
- Run tests to verify everything works: `python manage.py test users`
- For issues, create a GitHub issue with details about your problem

---

Built with Django REST Framework + JWT authentication. Simple, secure, production-ready.