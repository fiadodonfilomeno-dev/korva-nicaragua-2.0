#!/usr/bin/env python
import os
import django
from datetime import datetime, timedelta
from datetime import date, time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'korva_config.settings')
django.setup()

from django.conf import settings
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from users.models import Profile
from social.models import Post, Comment
from marketplace.models import Product, Review, Deal
from messaging.models import Conversation, Message
from events.models import Event
from groups.models import Group, GroupPost
from core.models import KorvaAIConfig


def _img_bytes(fname):
    """Lee una imagen real de static/img/real/"""
    path = os.path.join(settings.STATICFILES_DIRS[0], 'img', 'real', fname)
    with open(path, 'rb') as f:
        return f.read()


def _set_img(instance, field_name, fname):
    """Guarda una imagen local en un ImageField del modelo (sin duplicar)"""
    field = getattr(instance, field_name)
    if field and field.name == fname:
        return
    data = _img_bytes(fname)
    field.save(fname, ContentFile(data), save=True)

users_data = [
    {'username': 'panaderia_nicaraguena', 'email': 'panaderia@korva.com', 'business_name': 'Panadería Nicaragüeña', 'ruc': 'J0310000000002', 'city': 'managua', 'sector': 'alimentos', 'logo_url': '/static/img/real/logo-panaderia.jpg'},
    {'username': 'artesanias_esteli', 'email': 'artesanias@korva.com', 'business_name': 'Artesanías Estelí', 'ruc': 'J0310000000003', 'city': 'esteli', 'sector': 'artesanias', 'logo_url': '/static/img/real/logo-artesanias.jpg'},
    {'username': 'tech_solutions', 'email': 'tech@korva.com', 'business_name': 'Tech Solutions Nicaragua', 'ruc': 'J0310000000004', 'city': 'managua', 'sector': 'tecnologia', 'logo_url': '/static/img/real/logo-tech.jpg'},
    {'username': 'evaluador', 'email': 'evaluador@gmail.com', 'business_name': 'Evaluador Korva', 'ruc': 'J0310000000005', 'city': 'managua', 'sector': 'tecnologia', 'logo_url': '/static/img/real/logo-evaluador.jpg'},
]

print("[*] Creando usuarios de prueba...")
for user_data in users_data:
    password = user_data['username'].replace('_', '')
    if not User.objects.filter(username=user_data['username']).exists():
        user = User.objects.create_user(username=user_data['username'], email=user_data['email'], password=password)
        profile = Profile.objects.create(user=user, business_name=user_data['business_name'], ruc=user_data['ruc'], city=user_data['city'], sector=user_data['sector'], verified=True, popularity_score=2000 if user_data['username'] == 'evaluador' else 1500, followers_count=100 if user_data['username'] == 'evaluador' else 50, associates_count=50 if user_data['username'] == 'evaluador' else 25, collaborations_count=15 if user_data['username'] == 'evaluador' else 8, logo_url=user_data['logo_url'])
        KorvaAIConfig.objects.get_or_create(user=profile)
        print(f"  [OK] Usuario '{user_data['username']}' creado (password: {password})")
    else:
        print(f"  [SKIP] Usuario '{user_data['username']}' ya existe, se conserva su contraseña")

print("[*] Actualizando logos reales en perfiles existentes...")
for user_data in users_data:
    profile = Profile.objects.filter(user__username=user_data['username']).first()
    if profile:
        profile.logo_url = user_data['logo_url']
        profile.save(update_fields=['logo_url'])
        print(f"  [OK] logo_url actualizado para '{user_data['username']}'")

print("[*] Verificando perfil de admin...")
admin_user = User.objects.filter(username='admin').first()
if admin_user and not Profile.objects.filter(user=admin_user).exists():
    profile = Profile.objects.create(user=admin_user, business_name='Korva Nicaragua (Admin)', ruc='J0310000000001', city='managua', sector='servicios', verified=True, logo_url='/static/img/real/logo-admin.jpg')
    KorvaAIConfig.objects.get_or_create(user=profile)
    print("  [OK] Perfil de admin creado (faltaba)")
elif admin_user:
    profile = Profile.objects.get(user=admin_user)
    if profile.logo_url != '/static/img/real/logo-admin.jpg':
        profile.logo_url = '/static/img/real/logo-admin.jpg'
        profile.save(update_fields=['logo_url'])
    KorvaAIConfig.objects.get_or_create(user=profile)
    print("  [SKIP] Perfil de admin ya existe")

profiles = list(Profile.objects.filter(user__username__in=[u['username'] for u in users_data]))

def get_profile(username):
    return Profile.objects.get(user__username=username)

# POSTS
print("\n[*] Creando posts de prueba...")
posts_data = [
    {'title': 'Buscamos alianza para distribución de productos', 'content': 'Somos una pequeña panadería en Managua buscando socios para ampliar nuestra red de distribución. Ofrecemos productos frescos de calidad.', 'author': 'panaderia_nicaraguena', 'tags': ['negocio', 'alianza', 'distribucion'], 'image': 'post-alianza-pan.jpg'},
    {'title': 'Ofertas de artesanías tradicionales', 'content': 'Vendemos artesanías hechas a mano en Estelí. Ideales para regalos corporativos y souvenirs turísticos. Hacemos envíos a todo el país.', 'author': 'artesanias_esteli', 'tags': ['artesanias', 'ventas', 'esteli'], 'image': 'post-artesanias.jpg'},
    {'title': 'Servicios de desarrollo web y consultoría IT', 'content': 'Ofrecemos servicios profesionales de desarrollo web, aplicaciones móviles y consultoría tecnológica para PyMEs nicaragüenses.', 'author': 'tech_solutions', 'tags': ['tecnologia', 'desarrollo', 'consultoria'], 'image': 'post-tech.jpg'},
    {'title': 'Pan artesanal para tus eventos', 'content': 'Ahora ofrecemos pan artesanal para bodas, cumpleaños y eventos corporativos. Pedidos con 48 hrs de anticipación.', 'author': 'panaderia_nicaraguena', 'tags': ['panaderia', 'eventos', 'managua'], 'image': 'post-pan-eventos.jpg'},
    {'title': 'Cerámica pintada a mano - Nueva colección', 'content': 'Lanzamos nuestra nueva colección de cerámica pintada a mano con diseños tradicionales nicaragüenses. Piezas únicas.', 'author': 'artesanias_esteli', 'tags': ['ceramica', 'arte', 'nicaragua'], 'image': 'post-ceramica.jpg'},
    {'title': '¿Tu PyME necesita una app móvil?', 'content': 'Desarrollamos apps Android e iOS para negocios. Cotización sin compromiso. Clientes en Managua, León y Granada.', 'author': 'tech_solutions', 'tags': ['apps', 'movil', 'pymes'], 'image': 'post-app.jpg'},
]

for p in posts_data:
    profile = get_profile(p['author'])
    if not Post.objects.filter(title=p['title'], author=profile).exists():
        post = Post.objects.create(title=p['title'], content=p['content'], author=profile, moderation_status='approved', upvotes=15, downvotes=2)
        post.tags.add(*p['tags'])
        if p.get('image'):
            _set_img(post, 'image', p['image'])
        print(f"  [OK] Post '{p['title'][:40]}...'")
    else:
        post = Post.objects.filter(title=p['title'], author=profile).first()
        if p.get('image'):
            _set_img(post, 'image', p['image'])
        print(f"  [SKIP] Post '{p['title'][:40]}...' ya existe (imagen actualizada)")

# COMMENTS
print("\n[*] Creando comentarios...")
comments_data = [
    {'post_title': 'Buscamos alianza para distribución de productos', 'author': 'tech_solutions',     'content': 'Nos interesa. Trabajamos con varias PyMEs en Managua. Envíame más info.'},
    {'post_title': 'Buscamos alianza para distribución de productos', 'author': 'evaluador', 'content': 'Excelente iniciativa. ¿Distribuyen solo en Managua o también en otros departamentos?'},
    {'post_title': 'Ofertas de artesanías tradicionales', 'author': 'evaluador', 'content': '¿Tienen envíos a Managua? Me interesa para regalos corporativos.'},
    {'post_title': 'Servicios de desarrollo web y consultoría IT', 'author': 'panaderia_nicaraguena', 'content': 'Estamos buscando crear una tienda en línea. ¿Nos pueden ayudar?'},
]
for c in comments_data:
    post = Post.objects.filter(title=c['post_title']).first()
    author = get_profile(c['author'])
    if post and not Comment.objects.filter(post=post, author=author, content=c['content']).exists():
        Comment.objects.create(post=post, author=author, content=c['content'])
        print(f"  [OK] Comentario de '{c['author']}' en '{c['post_title'][:30]}...'")

# PRODUCTS
print("\n[*] Creando productos en marketplace...")
products_data = [
    {'name': 'Pan de yema (docena)', 'description': 'Pan de yema artesanal, horneado diariamente. Ingredientes naturales, sin preservantes.', 'price': 80, 'currency': 'NIO', 'category': 'ventas', 'whatsapp': '+50587654321', 'owner': 'panaderia_nicaraguena', 'image_url': '/static/img/real/product-pan-yema.jpg', 'image': 'product-pan-yema.jpg'},
    {'name': 'Pastel de tres leches', 'description': 'Pastel de tres leches tradicional, disponible en tamaños personalizados. Ideal para cumpleaños y eventos.', 'price': 450, 'currency': 'NIO', 'category': 'ventas', 'whatsapp': '+50587654321', 'owner': 'panaderia_nicaraguena', 'image_url': '/static/img/real/product-tres-leches.jpg', 'image': 'product-tres-leches.jpg'},
    {'name': 'Café artesanal molido (1lb)', 'description': 'Café 100% nicaragüense, tostado artesanalmente. Disponible en presentación de 1 libra.', 'price': 180, 'currency': 'NIO', 'category': 'ventas', 'whatsapp': '+50587654321', 'owner': 'panaderia_nicaraguena', 'image_url': '/static/img/real/product-cafe.jpg', 'image': 'product-cafe.jpg'},
    {'name': 'Jarra de cerámica pintada a mano', 'description': 'Jarra decorativa de cerámica, pintada a mano con diseños tradicionales de Nicaragua. Capacidad 1.5 litros.', 'price': 350, 'currency': 'NIO', 'category': 'ventas', 'whatsapp': '+50587123456', 'owner': 'artesanias_esteli', 'image_url': '/static/img/real/product-jarra-ceramica.jpg', 'image': 'product-jarra-ceramica.jpg'},
    {'name': 'Set de tazas artesanales (6 pzs)', 'description': 'Set de 6 tazas de cerámica hechas a mano, cada una con diseño único. Perfectas para cafetería.', 'price': 600, 'currency': 'NIO', 'category': 'ventas', 'whatsapp': '+50587123456', 'owner': 'artesanias_esteli', 'image_url': '/static/img/real/product-tazas.jpg', 'image': 'product-tazas.jpg'},
    {'name': 'Hamaca nicaragüense tejida', 'description': 'Hamaca tradicional tejida a mano en Estelí. Algodón de alta resistencia. Colores variados.', 'price': 1200, 'currency': 'NIO', 'category': 'ventas', 'whatsapp': '+50587123456', 'owner': 'artesanias_esteli', 'image_url': '/static/img/real/product-hamaca.jpg', 'image': 'product-hamaca.jpg'},
    {'name': 'Desarrollo de sitio web corporativo', 'description': 'Sitio web profesional con panel administrativo, diseño responsivo y optimización SEO. Incluye hosting 1 año.', 'price': 300, 'currency': 'USD', 'category': 'ventas', 'whatsapp': '+50588887777', 'owner': 'tech_solutions', 'image_url': '/static/img/real/product-web.jpg', 'image': 'product-web.jpg'},
    {'name': 'App móvil para PyMEs', 'description': 'Aplicación móvil Android/iOS para tu negocio. Incluye catálogo de productos, carrito de compras y notificaciones.', 'price': 800, 'currency': 'USD', 'category': 'ventas', 'whatsapp': '+50588887777', 'owner': 'tech_solutions', 'image_url': '/static/img/real/product-app.jpg', 'image': 'product-app.jpg'},
    {'name': 'Consultoría en transformación digital', 'description': 'Asesoría personalizada para digitalizar tu PyME. Incluye diagnóstico, plan de acción y acompañamiento.', 'price': 200, 'currency': 'USD', 'category': 'ventas', 'whatsapp': '+50588887777', 'owner': 'tech_solutions', 'image_url': '/static/img/real/product-consultoria.jpg', 'image': 'product-consultoria.jpg'},
]
for p in products_data:
    profile = get_profile(p['owner'])
    if not Product.objects.filter(name=p['name'], user=profile).exists():
        product = Product.objects.create(name=p['name'], description=p['description'], price=p['price'], currency=p['currency'], category=p['category'], contact_whatsapp=p['whatsapp'], image_url=p.get('image_url', ''), user=profile, is_active=True)
        if p.get('image'):
            _set_img(product, 'image', p['image'])
        print(f"  [OK] Producto '{p['name']}'")
    else:
        Product.objects.filter(name=p['name'], user=profile).update(image_url=p.get('image_url', ''))
        product = Product.objects.filter(name=p['name'], user=profile).first()
        if p.get('image'):
            _set_img(product, 'image', p['image'])
        print(f"  [OK] Producto '{p['name']}' actualizado (image_url + imagen)")

# REVIEWS
print("\n[*] Creando reseñas...")
reviews_data = [
    {'reviewer': 'tech_solutions', 'seller': 'panaderia_nicaraguena', 'rating': 5, 'comment': 'Excelente calidad de productos. Muy recomendados.'},
    {'reviewer': 'evaluador', 'seller': 'artesanias_esteli', 'rating': 4, 'comment': 'Hermosas artesanías. Los envíos llegaron en buen estado.'},
    {'reviewer': 'panaderia_nicaraguena', 'seller': 'tech_solutions', 'rating': 5, 'comment': 'Gran trabajo en el sitio web. Muy profesionales.'},
    {'reviewer': 'artesanias_esteli', 'seller': 'evaluador', 'rating': 5, 'comment': 'Excelente comprador, pago puntual y buena comunicación.'},
]
for r in reviews_data:
    reviewer = get_profile(r['reviewer'])
    seller = get_profile(r['seller'])
    if not Review.objects.filter(reviewer=reviewer, seller=seller, rating=r['rating']).exists():
        Review.objects.create(reviewer=reviewer, seller=seller, rating=r['rating'], comment=r['comment'])
        print(f"  [OK] Reseña de '{r['reviewer']}' a '{r['seller']}' ({r['rating']} estrellas)")

# CONVERSATIONS & MESSAGES
print("\n[*] Creando conversaciones y mensajes...")
conv_pairs = [
    ('panaderia_nicaraguena', 'tech_solutions', [
        ('tech_solutions', 'Hola, vi su post sobre alianzas de distribución. Nos interesa conversar.'),
        ('panaderia_nicaraguena', '¡Excelente! Claro, ¿qué tipo de distribución necesitan?'),
        ('tech_solutions', 'Buscamos distribuir nuestros servicios IT entre PyMEs del sector alimentos. ¿Les interesa una alianza?'),
        ('panaderia_nicaraguena', 'Suena bien. Trabajamos con varias panaderías y cafeterías en Managua. Podríamos recomendar sus servicios.'),
    ]),
    ('artesanias_esteli', 'evaluador', [
        ('evaluador', 'Hola, vi sus artesanías en el marketplace. ¿Tienen envíos a Managua?'),
        ('artesanias_esteli', '¡Hola! Sí, hacemos envíos a Managua cada semana. El costo es de C$50.'),
        ('evaluador', 'Perfecto. Me interesa el set de tazas artesanales. ¿Lo tienen disponible?'),
        ('artesanias_esteli', 'Sí, tenemos disponibilidad. Le puedo reservar el set.'),
    ]),
    ('panaderia_nicaraguena', 'evaluador', [
        ('evaluador', 'Buen día, ¿tienen pan de yema hoy?'),
        ('panaderia_nicaraguena', 'Buen día. Sí, acabamos de hornear. Tenemos disponible.'),
    ]),
]
for user1, user2, msgs in conv_pairs:
    p1 = get_profile(user1)
    p2 = get_profile(user2)
    for (u1, u2) in [(p1, p2), (p2, p1)]:
        if not Conversation.objects.filter(user1=u1, user2=u2).exists():
            conv = Conversation.objects.create(user1=u1, user2=u2)
            for sender_username, text in msgs:
                sender = get_profile(sender_username)
                Message.objects.create(sender=sender, recipient=p2 if sender == p1 else p1, content=text)
            print(f"  [OK] Conversación '{user1}' <-> '{user2}' ({len(msgs)} msgs)")
            break

# EVENTS
print("\n[*] Creando eventos...")
events_data = [
    {'title': 'Feria de la PyME 2026', 'description': 'Evento anual para pequeñas y medianas empresas nicaragüenses. Habrá expositores, charlas y networking.', 'category': 'feria', 'organizer': 'tech_solutions', 'date': date.today() + timedelta(days=30), 'time': time(9, 0), 'location': 'Centro de Convenciones Olof Palme', 'city': 'managua', 'image': 'event-feria-pyme.jpg'},
    {'title': 'Taller de panadería artesanal', 'description': 'Aprende a hacer pan artesanal desde cero. Incluye ingredientes y herramientas. Cupo limitado.', 'category': 'taller', 'organizer': 'panaderia_nicaraguena', 'date': date.today() + timedelta(days=15), 'time': time(14, 0), 'location': 'Panadería Nicaragüeña - Managua', 'city': 'managua', 'image': 'event-taller-pan.jpg'},
    {'title': 'Charla: Transformación digital para PyMEs', 'description': 'Conferencia gratuita sobre cómo digitalizar tu negocio. Casos de éxito y herramientas prácticas.', 'category': 'conferencia', 'organizer': 'tech_solutions', 'date': date.today() + timedelta(days=7), 'time': time(10, 0), 'location': 'Coworking Meta, Managua', 'city': 'managua', 'image': 'event-charla-tech.jpg'},
    {'title': 'Expo Artesanías Estelí', 'description': 'Exposición y venta de artesanías tradicionales de Estelí. Productos únicos hechos a mano.', 'category': 'feria', 'organizer': 'artesanias_esteli', 'date': date.today() + timedelta(days=45), 'time': time(8, 0), 'location': 'Parque Central de Estelí', 'city': 'esteli', 'image': 'event-expo-artesanias.jpg'},
]
for e in events_data:
    org = get_profile(e['organizer'])
    if not Event.objects.filter(title=e['title'], organizer=org).exists():
        event = Event.objects.create(title=e['title'], description=e['description'], category=e['category'], organizer=org, date=e['date'], time=e['time'], location=e['location'], city=e['city'], is_active=True)
        if e.get('image'):
            _set_img(event, 'image', e['image'])
        print(f"  [OK] Evento '{e['title']}'")
    else:
        event = Event.objects.filter(title=e['title'], organizer=org).first()
        if e.get('image'):
            _set_img(event, 'image', e['image'])
        print(f"  [SKIP] Evento '{e['title']}' ya existe (imagen actualizada)")

# GROUPS
print("\n[*] Creando grupos...")
groups_data = [
    {'name': 'PyMEs de Alimentos Nicaragua', 'description': 'Grupo para negocios del sector alimentos. Comparte proveedores, recetas y oportunidades de negocio.', 'sector': 'alimentos', 'admin': 'panaderia_nicaraguena', 'members': ['artesanias_esteli', 'tech_solutions', 'evaluador']},
    {'name': 'Tecnología y Emprendimiento', 'description': 'Comunidad de emprendedores tech en Nicaragua. Networking, colaboraciones y mentoría.', 'sector': 'tecnologia', 'admin': 'tech_solutions', 'members': ['panaderia_nicaraguena', 'evaluador']},
    {'name': 'Artesanías Nicaragüenses', 'description': 'Espacio para artesanos de todo el país. Promociona y vende tus artesanías.', 'sector': 'artesanias', 'admin': 'artesanias_esteli', 'members': ['evaluador']},
]
for g in groups_data:
    admin = get_profile(g['admin'])
    if not Group.objects.filter(name=g['name'], admin=admin).exists():
        group = Group.objects.create(name=g['name'], description=g['description'], sector=g['sector'], admin=admin)
        for m in g['members']:
            group.members.add(get_profile(m))
        print(f"  [OK] Grupo '{g['name']}'")
    else:
        print(f"  [SKIP] Grupo '{g['name']}' ya existe")

# GROUP POSTS
print("\n[*] Creando posts en grupos...")
group_posts_data = [
    {'group': 'PyMEs de Alimentos Nicaragua', 'author': 'panaderia_nicaraguena', 'content': '¡Buenos días! Conseguimos un nuevo proveedor de harina a mejor precio. Si alguien quiere el dato, escríbame.'},
    {'group': 'PyMEs de Alimentos Nicaragua', 'author': 'evaluador', 'content': '¿Alguien sabe de proveedores de empaques biodegradables en Managua?'},
    {'group': 'Tecnología y Emprendimiento', 'author': 'tech_solutions', 'content': 'Estamos ofreciendo 3 becas para el taller de desarrollo web básico. Interesados confirmar aquí.'},
    {'group': 'Tecnología y Emprendimiento', 'author': 'evaluador', 'content': 'Excelente iniciativa. Yo tengo experiencia en UI/UX, puedo dar una charla si les interesa.'},
    {'group': 'Artesanías Nicaragüenses', 'author': 'artesanias_esteli', 'content': 'Pronto lanzaremos una nueva línea de cerámica con diseños precolombinos. Fotografías pronto.'},
]
for gp in group_posts_data:
    group = Group.objects.filter(name=gp['group']).first()
    author = get_profile(gp['author'])
    if group and not GroupPost.objects.filter(group=group, author=author, content=gp['content']).exists():
        GroupPost.objects.create(group=group, author=author, content=gp['content'])
        print(f"  [OK] GroupPost de '{gp['author']}' en '{gp['group']}'")

print("\n[*] Datos de prueba cargados exitosamente!")
print("\nCuentas de prueba:")
print("  admin / admin123 (Administrador)")
print("  panaderia_nicaraguena / panaderianicaraguena")
print("  artesanias_esteli / artesaniasesteli")
print("  tech_solutions / techsolutions")
print("  evaluador / evaluador")
