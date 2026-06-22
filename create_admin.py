#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'korva_config.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import Profile
from core.models import KorvaAIConfig

# Crear superusuario de prueba
if not User.objects.filter(username='admin').exists():
    user = User.objects.create_superuser(
        username='admin',
        email='admin@korva.com',
        password='admin123'
    )
    
    # Crear perfil
    profile = Profile.objects.create(
        user=user,
        business_name='Administrador Korva',
        ruc='J0310000000001',
        city='managua',
        sector='servicios',
        verified=True,
        popularity_score=5000
    )
    
    # Crear configuración de IA
    KorvaAIConfig.objects.create(user=profile)
    
    print("[OK] Superusuario 'admin' creado exitosamente")
    print("     Usuario: admin")
    print("     Contraseña: admin123")
else:
    print("[OK] El usuario 'admin' ya existe")
