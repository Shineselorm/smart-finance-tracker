from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os


class Command(BaseCommand):
    help = 'Creates or resets admin user from environment variables'

    def handle(self, *args, **options):
        username = os.environ.get('ADMIN_USERNAME', 'admin')
        email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
        password = os.environ.get('ADMIN_PASSWORD')
        
        if not password:
            self.stdout.write(
                self.style.WARNING(
                    '⚠️  No ADMIN_PASSWORD environment variable set. Skipping admin creation.'
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    '   Set ADMIN_USERNAME, ADMIN_EMAIL, and ADMIN_PASSWORD in Render environment.'
                )
            )
            return
        
        try:
            # Check if user exists
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                user.set_password(password)
                user.is_staff = True
                user.is_superuser = True
                user.email = email
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Admin password reset successfully for: {username}'
                    )
                )
            else:
                user = User.objects.create_superuser(username, email, password)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Superuser created successfully: {username}'
                    )
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'❌ Error creating/updating admin user: {str(e)}'
                )
            )
            raise

