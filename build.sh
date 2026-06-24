#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit  # Exit on error

echo "=== Instalando dependencias ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== Recopilando archivos estáticos ==="
python manage.py collectstatic --no-input

echo "=== Ejecutando migraciones ==="
python manage.py migrate --no-input

echo "=== Creando superusuario si no existe ==="
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@korva.ni', 'admin123')
    print('Superusuario admin creado')
else:
    print('Superusuario admin ya existe')
"

echo "=== Build completado ==="