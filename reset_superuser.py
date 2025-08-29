#!/usr/bin/env python
"""
Script to delete existing superuser and create a new one
"""
import os
import django
from django.contrib.auth import get_user_model

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
    django.setup()
    
    User = get_user_model()
    
    # Delete all existing superusers
    existing_superusers = User.objects.filter(is_superuser=True)
    if existing_superusers.exists():
        for user in existing_superusers:
            print(f"Deleting existing superuser: {user.email}")
            user.delete()
        print("All existing superusers deleted!")
    
    # Create new superuser
    email = os.environ.get('SUPERUSER_EMAIL', 'admin@example.com')
    password = os.environ.get('SUPERUSER_PASSWORD', 'admin123')
    
    User.objects.create_superuser(
        email=email,
        password=password
    )
    print(f"New superuser created: {email}")
    print(f"You can now login with: {email}")
