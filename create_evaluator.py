#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'korva_config.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import Profile
from core.models import KorvaAIConfig

username = 'evaluador'
email = 'evaluador@gmail.com'
password = 'evaluadorPassword2026!'

if not User.objects.filter(username=username).exists():
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )
    
    # El perfil es creado por la señal, lo obtenemos y actualizamos.
    profile = user.profile
    profile.business_name = 'Evaluador Oficial'
    profile.ruc = 'J0310000001999'
    profile.city = 'managua'
    profile.sector = 'servicios'
    profile.verified = True
    profile.popularity_score = 2000
    profile.save()
    
    # Crear configuración de IA
    KorvaAIConfig.objects.get_or_create(user=profile)
    
    print("[OK] Usuario de prueba para el evaluador creado exitosamente")
    print(f"     Usuario: {username}")
    print(f"     Email: {email}")
    print(f"     Contraseña: {password}")
else:
    # Si ya existe, aseguremos su contraseña
    user = User.objects.get(username=username)
    user.email = email
    user.set_password(password)
    user.save()
    print("[OK] Usuario 'evaluador' ya existe. Contraseña y email actualizados.")
