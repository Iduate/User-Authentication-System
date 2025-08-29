import redis
import secrets
import logging
from django.conf import settings
from django.core.cache import cache

# Set up logging
logger = logging.getLogger(__name__)

# Try to connect to Redis or use Django's default cache as a fallback
try:
    redis_client = redis.from_url(settings.REDIS_URL)
    redis_available = True
except redis.exceptions.ConnectionError:
    logger.warning("Redis connection failed. Using Django cache as fallback.")
    redis_client = None
    redis_available = False


def generate_password_reset_token(user_id):
    """
    Generate a random token for password reset and store it in Redis or Django cache.
    
    Args:
        user_id: The ID of the user requesting a password reset
        
    Returns:
        str: The generated token
    """
    # Generate a secure random token
    token = secrets.token_urlsafe(32)
    
    # Store the token with an expiry time of 10 minutes (600 seconds)
    key = f"password_reset:{token}"
    
    # First try storing in Redis if available
    redis_success = False
    if redis_available and redis_client:
        try:
            redis_client.setex(key, 600, str(user_id))
            redis_success = True
        except Exception as e:
            logger.error(f"Redis error storing token: {str(e)}")
    
    # If Redis failed or is not available, fallback to Django's cache
    if not redis_success:
        try:
            cache.set(key, str(user_id), timeout=600)
            logger.info(f"Token stored in Django cache: {token[:6]}...")
        except Exception as e:
            logger.error(f"Cache error storing token: {str(e)}")
            # Even if both Redis and cache fail, return a token so the app doesn't crash
    
    return token


def validate_password_reset_token(token):
    """
    Validate a password reset token from Redis or Django cache.
    
    Args:
        token: The token to validate
        
    Returns:
        str or None: The user ID associated with the token if valid, None otherwise
    """
    # Get the user ID associated with the token
    key = f"password_reset:{token}"
    user_id = None
    
    # First try Redis if available
    if redis_available and redis_client:
        try:
            user_id_bytes = redis_client.get(key)
            if user_id_bytes:
                user_id = user_id_bytes.decode('utf-8')
                # Delete the token to prevent reuse
                redis_client.delete(key)
                return user_id
        except Exception as e:
            logger.error(f"Redis error validating token: {str(e)}")
            # Continue to try the cache fallback
    
    # Then try Django's cache as a fallback
    try:
        user_id = cache.get(key)
        if user_id:
            # Delete the token to prevent reuse
            cache.delete(key)
            return user_id
    except Exception as e:
        logger.error(f"Cache error validating token: {str(e)}")
    
    return None
