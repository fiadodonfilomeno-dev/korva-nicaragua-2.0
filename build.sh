#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit  # Exit on error

echo "=== Instalando dependencias Python ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== Recopilando archivos estáticos ==="
python manage.py collectstatic --no-input

echo "=== Ejecutando migraciones ==="
python manage.py migrate --no-input

echo "=== Creando superusuario si no existe ==="
python manage.py shell -c "
from django.contrib.auth import get_user_model
from users.models import Profile
from core.models import KorvaAIConfig
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser('admin', 'admin@korva.ni', 'admin123')
    profile = Profile.objects.get_or_create(
        user=admin,
        defaults={'business_name': 'Korva Nicaragua (Admin)', 'ruc': 'J0310000000001', 'city': 'managua', 'sector': 'servicios', 'verified': True}
    )[0]
    print('Superusuario admin creado con perfil')
else:
    admin = User.objects.get(username='admin')
    if not hasattr(admin, 'profile'):
        profile = Profile.objects.create(user=admin, business_name='Korva Nicaragua (Admin)', ruc='J0310000000001', city='managua', sector='servicios', verified=True)
        print('Perfil de admin creado (faltaba)')
    else:
        profile = admin.profile
        print('Superusuario admin ya existe con perfil')
KorvaAIConfig.objects.get_or_create(user=profile)
print('Config IA de admin verificada')
"

echo "=== Cargando datos de prueba ==="
python load_test_data.py

echo "=== Build completado ==="