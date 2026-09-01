from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import Profile


class Command(BaseCommand):
    help = 'Creates admin user if it does not exist'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@korva.com',
                password='admin123'
            )
            profile = Profile.objects.get(user__username='admin')
            profile.business_name = 'Korva Admin'
            profile.ruc = 'J0310000000000'
            profile.save(update_fields=['business_name', 'ruc'])
            self.stdout.write(self.style.SUCCESS('Admin user created'))
        else:
            self.stdout.write('Admin user already exists')
