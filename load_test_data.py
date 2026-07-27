#!/usr/bin/env python
import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'korva_config.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import Profile
from social.models import Post, Comment
from marketplace.models import Product
from core.models import KorvaAIConfig

# Crear usuarios de prueba
users_data = [
    {
        'username': 'panaderia_nicaraguena',
        'email': 'panaderia@korva.com',
        'business_name': 'Panadería Nicaragüeña',
        'ruc': 'J0310000000002',
        'city': 'managua',
        'sector': 'alimentos'
    },
    {
        'username': 'artesanias_esteli',
        'email': 'artesanias@korva.com',
        'business_name': 'Artesanías Estelí',
        'ruc': 'J0310000000003',
        'city': 'esteli',
        'sector': 'artesanias'
    },
    {
        'username': 'tech_solutions',
        'email': 'tech@korva.com',
        'business_name': 'Tech Solutions Nicaragua',
        'ruc': 'J0310000000004',
        'city': 'managua',
        'sector': 'tecnologia'
    }
]

print("[*] Creando usuarios de prueba...")
for user_data in users_data:
    if not User.objects.filter(username=user_data['username']).exists():
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password='test1234'
        )
        
        profile = user.profile
        profile.business_name=user_data['business_name']
        profile.ruc=user_data['ruc']
        profile.city=user_data['city']
        profile.sector=user_data['sector']
        profile.verified=True
        profile.popularity_score=1500
        profile.followers_count=50
        profile.associates_count=25
        profile.collaborations_count=8
        profile.save()
        
        KorvaAIConfig.objects.get_or_create(user=profile)
        
        print(f"  [OK] Usuario '{user_data['username']}' creado")
    else:
        print(f"  [SKIP] Usuario '{user_data['username']}' ya existe")

# Crear posts de prueba
print("\n[*] Creando posts de prueba...")
profiles = Profile.objects.all()[:3]

posts_data = [
    {
        'title': 'Buscamos alianza para distribución de productos',
        'content': 'Somos una pequeña panadería en Managua buscando socios para ampliar nuestra red de distribución. Ofrecemos productos frescos de calidad.',
        'author': profiles[0] if profiles else None
    },
    {
        'title': 'Ofertas de artesanías tradicionales',
        'content': 'Vendemos artesanías hechas a mano en Estelí. Ideales para regalos corporativos y souvenirs turísticos.',
        'author': profiles[1] if len(profiles) > 1 else None
    },
    {
        'title': 'Servicios de desarrollo web y consultoría IT',
        'content': 'Ofrecemos servicios profesionales de desarrollo web, aplicaciones móviles y consultoría tecnológica para PyMEs.',
        'author': profiles[2] if len(profiles) > 2 else None
    }
]

for post_data in posts_data:
    if post_data['author']:
        post = Post.objects.create(
            title=post_data['title'],
            content=post_data['content'],
            author=post_data['author'],
            moderation_status='approved',
            upvotes=15,
            downvotes=2
        )
        post.tags.add('negocio', 'alianza', 'oportunidad')
        print(f"  [OK] Post '{post_data['title'][:40]}...' creado")

print("\n[*] Datos de prueba cargados exitosamente!")
print("\nAcceso a la aplicación:")
print("  URL: http://localhost:8000")
print("  Admin: http://localhost:8000/admin")
print("\nCuentas de prueba:")
print("  admin / admin123 (Administrador)")
print("  panaderia_nicaraguena / admin123")
print("  artesanias_esteli / admin123")
print("  tech_solutions / admin123")
