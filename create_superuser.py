#!/usr/bin/env python
"""
Script to create a Django superuser for Railway deployment
"""
import os
import django
from django.contrib.auth import get_user_model
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
    django.setup()
    
    User = get_user_model()
    
    # Check if superuser already exists
    if User.objects.filter(is_superuser=True).exists():
        print("Superuser already exists!")
    else:
        # Create superuser with environment variables or defaults
        email = os.environ.get('SUPERUSER_EMAIL', 'admin@example.com')
        password = os.environ.get('SUPERUSER_PASSWORD', 'admin123')
        
        User.objects.create_superuser(
            email=email,
            password=password
        )
        print(f"Superuser '{email}' created successfully!")
