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
    
    # Actualizar perfil
    profile = user.profile
    profile.business_name='Administrador Korva'
    profile.ruc='J0310000000001'
    profile.city='managua'
    profile.sector='servicios'
    profile.verified=True
    profile.popularity_score=5000
    profile.save()
    
    # Crear configuración de IA
    KorvaAIConfig.objects.get_or_create(user=profile)
    
    print("[OK] Superusuario 'admin' creado exitosamente")
    print("     Usuario: admin")
    print("     Contraseña: admin123")
else:
    print("[OK] El usuario 'admin' ya existe")
