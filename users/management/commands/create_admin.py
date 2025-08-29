from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a superuser'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Admin email')
        parser.add_argument('--password', type=str, help='Admin password')

    def handle(self, *args, **options):
        email = options.get('email') or 'davididuate11@gmail.com'
        password = options.get('password') or 'admin123'
        
        if User.objects.filter(email=email).exists():
            self.stdout.write(f'User with email {email} already exists')
            # Update password for existing user
            user = User.objects.get(email=email)
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Updated superuser {email}'))
        else:
            User.objects.create_superuser(
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f'Created superuser {email}'))
