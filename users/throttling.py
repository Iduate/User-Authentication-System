from rest_framework.throttling import AnonRateThrottle

class LoginRateThrottle(AnonRateThrottle):
    """Limits the rate of login attempts."""
    scope = 'login'


class PasswordResetRateThrottle(AnonRateThrottle):
    """Limits the rate of password reset requests."""
    scope = 'password_reset'
