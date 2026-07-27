import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'korva_config.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import Profile
from core.models import KorvaAIConfig

# Check if profiles exist in DB
print('=== PROFILES IN DB ===')
for p in Profile.objects.all():
    print(f'  Profile: {p.business_name} | User: {p.user.username}')

# Check relationship
u = User.objects.get(username='admin')
print(f'Admin user: {u.username}')
print(f'Has profile attr: {hasattr(u, "profile")}')
try:
    p = u.profile
    print(f'Profile: {p.business_name}')
except Exception as e:
    print(f'Error: {e}')
    # Try direct query
    p = Profile.objects.filter(user=u).first()
    print(f'Direct query: {p}')

# Check all users with profiles
print('\n=== ALL USERS WITH PROFILES ===')
for u in User.objects.all():
    try:
        p = u.profile
        print(f'  {u.username} -> {p.business_name}')
    except Exception as e:
        print(f'  {u.username} -> ERROR: {e}')
