#!/usr/bin/env python
"""
Script to create cache table for Railway deployment
"""
import os
import django
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
    django.setup()
    
    # Create cache table
    try:
        execute_from_command_line(['manage.py', 'createcachetable'])
        print("Cache table created successfully!")
    except Exception as e:
        print(f"Cache table creation failed or already exists: {e}")
