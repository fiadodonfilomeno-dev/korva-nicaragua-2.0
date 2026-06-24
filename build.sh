#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit  # Exit on error

echo "=== Instalando dependencias ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== Esperando a PostgreSQL ==="
if [ -n "$DATABASE_URL" ]; then
    python -c "
import os, time, sys
db_url = os.environ.get('DATABASE_URL', '')
if db_url:
    try:
        import psycopg2
        for i in range(30):
            try:
                conn = psycopg2.connect(db_url)
                conn.close()
                print('PostgreSQL listo')
                break
            except Exception:
                time.sleep(1)
        else:
            print('ERROR: Timeout esperando PostgreSQL')
            sys.exit(1)
    except ImportError:
        print('psycopg2 no disponible, continuando...')
"
fi

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