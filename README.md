# User Authentication System

A simple, secure Django REST API for user authentication with JWT tokens.

## What it does

- **User registration and login** with email validation
- **JWT token authentication** (access + refresh tokens)
- **Password reset functionality** with secure token validation
- **Rate limiting** on login and password reset endpoints
- **PostgreSQL database** with Redis caching support
- **Docker support** for easy local development
- **Comprehensive unit tests** for all authentication flows
- **API documentation** with Swagger/OpenAPI
- **Production-ready** with security best practices

## Quick Start

**Using Docker (recommended for development):**
```bash
git clone https://github.com/Iduate/User-Authentication-System.git
cd User-Authentication-System/auth_service
docker-compose up -d
```

**Access your API:**
- API: http://localhost:8000/api/v1/
- Documentation: http://localhost:8000/swagger/
- Admin: http://localhost:8000/admin/

**Docker includes:**
- PostgreSQL database
- Redis for caching
- All dependencies pre-installed
- Automatic database migrations

## API Documentation

**Interactive API Documentation:**
- **Swagger UI**: http://localhost:8000/swagger/ 
- **ReDoc**: http://localhost:8000/redoc/
- **OpenAPI Schema**: Complete API specification with request/response examples

### Authentication Endpoints

#### Register a new user
```
POST /api/v1/users/register/
{
  "email": "user@example.com",
  "full_name": "John Doe", 
  "password": "SecurePassword123!",
  "password_confirm": "SecurePassword123!"
}
```

#### Login
```
POST /api/v1/users/login/
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

#### Refresh JWT Token
```
POST /api/v1/users/token/refresh/
{
  "refresh": "your-refresh-token-here"
}
```

### User Profile Endpoints

#### Get user profile
```
GET /api/v1/users/profile/
Headers: Authorization: Bearer <your-access-token>
```

### Password Reset Endpoints

#### Request password reset
```
POST /api/v1/users/password-reset/
{
  "email": "user@example.com"
}
```

#### Confirm password reset
```
POST /api/v1/users/password-reset/confirm/
{
  "token": "reset-token-from-email",
  "new_password": "NewSecurePassword123!",
  "new_password_confirm": "NewSecurePassword123!"
}
```

### Development Endpoints

#### Authentication debug (development only)
```
GET /api/v1/users/auth-debug/
```
*Helps debug authentication issues during development*

### Alternative Endpoint Paths

All endpoints are also available at:
- `/api/v1/register/` (alternative to `/api/v1/users/register/`)
- `/api/v1/login/` (alternative to `/api/v1/users/login/`)
- `/api/v1/profile/` (alternative to `/api/v1/users/profile/`)
- `/api/v1/password-reset/` (alternative to `/api/v1/users/password-reset/`)

## Security Features

- **Rate limiting** on login and password reset endpoints
  - Login: 5 attempts per minute per IP
  - Password reset: 3 attempts per hour per IP
- **JWT token authentication** with access and refresh tokens
- **Unit tests** for registration, login, and password reset
- **Docker support** for local development
- **Input validation** and secure password requirements
- **CORS protection** and security headers

## Local Development Setup

**Prerequisites:**
- Python 3.11+ installed
- PostgreSQL 12+ installed and running
- Redis installed (optional, will fallback to Django cache)
- Git installed

**Step-by-step setup:**

1. **Clone the repository:**
```bash
git clone https://github.com/Iduate/User-Authentication-System.git
cd User-Authentication-System/auth_service
```

2. **Create virtual environment:**
```bash
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Setup database:**
```bash
# Create PostgreSQL database
createdb auth_db

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

5. **Start development server:**
```bash
python manage.py runserver
```

6. **Access the application:**
- API: http://localhost:8000/api/v1/
- Admin: http://localhost:8000/admin/
- API Documentation: http://localhost:8000/swagger/

## Environment Variables

**Required Environment Variables:**

Create a `.env` file in your project root:

```env
# Django Core Settings
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DATABASE_URL=postgres://username:password@localhost:5432/auth_db
# Alternative individual database settings:
DATABASE_NAME=auth_db
DATABASE_USER=postgres
DATABASE_PASSWORD=your-db-password
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Redis Configuration (Optional)
REDIS_URL=redis://localhost:6379/0

# JWT Token Settings (Optional - has defaults)
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7

# Email Settings (for password reset)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

**Environment Variables Reference:**

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SECRET_KEY` | Django secret key for cryptographic signing | ✅ | None |
| `DEBUG` | Enable/disable debug mode | ❌ | `False` |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts | ❌ | `localhost` |
| `DATABASE_URL` | PostgreSQL connection string | ✅ | None |
| `REDIS_URL` | Redis connection string | ❌ | None |
| `JWT_ACCESS_TOKEN_LIFETIME_MINUTES` | Access token expiration | ❌ | `60` |
| `JWT_REFRESH_TOKEN_LIFETIME_DAYS` | Refresh token expiration | ❌ | `7` |

**For Production:**
- Set `DEBUG=False`
- Use strong, unique `SECRET_KEY`
- Configure proper `ALLOWED_HOSTS`
- Use production database URLs
- Set up email configuration for password reset

## Testing

**Run all unit tests:**
```bash
python manage.py test users
```

**Test specific functionality:**
```bash
# Test registration
python manage.py test users.tests.test_registration

# Test login
python manage.py test users.tests.test_login

# Test password reset
python manage.py test users.tests.test_password_reset
```

**Unit test coverage includes:**
- User registration validation
- Login authentication
- Password reset flow
- Rate limiting
- JWT token handling

## Production Deployment

**Live Demo:**
🌐 **API Base URL**: https://your-app-name.railway.app/api/v1/
📖 **API Documentation**: https://your-app-name.railway.app/swagger/
🔧 **Admin Panel**: https://your-app-name.railway.app/admin/

**Supported Platforms:**
- ✅ Railway (recommended)
- ✅ Render
- ✅ Heroku
- ✅ DigitalOcean
- ✅ AWS/GCP/Azure

**Quick Deploy to Railway:**
1. Fork this repository
2. Connect to [Railway](https://railway.app)
3. Deploy from GitHub
4. Add environment variables
5. Your API will be live!

**Environment Variables for Production:**
```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.railway.app,your-custom-domain.com
DATABASE_URL=postgresql://... (provided by Railway)
REDIS_URL=redis://... (provided by Railway)
```

## Need Help?

- Check the [API docs](http://localhost:8000/swagger/) for detailed endpoint information
- Run tests to verify everything works: `python manage.py test users`
- For issues, create a GitHub issue with details about your problem

---

Built with Django REST Framework + JWT authentication. Simple, secure, production-ready.