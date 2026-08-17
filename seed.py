#!/usr/bin/env python
import os, sys, random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'korva_config.settings')

parent = os.path.dirname
sys.path.insert(0, parent(os.path.abspath(__file__)))

import django
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from users.models import Profile
from social.models import Post, Comment, Vote, Favorite
from marketplace.models import Product, Review, Deal, BankAccount, Transaction
from messaging.models import Conversation, Message
from notifications.models import Notification, NotificationPreference
from core.models import KorvaAIConfig
from events.models import Event
from groups.models import Group, GroupPost

CITY_CHOICES = [c[0] for c in Profile.CITY_CHOICES]
SECTOR_CHOICES = [s[0] for s in Profile.SECTOR_CHOICES]
BANK_CHOICES = [b[0] for b in BankAccount.BANK_CHOICES]

RUC_BASE = 1000000000000

def ok(msg):
    print(f"  [OK] {msg}")

def section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def create_user(username, email, password, business_name, city, sector, ruc, verified=False, score=0, bio=""):
    u = User.objects.filter(username=username).first()
    if u:
        u.set_password(password)
        u.is_active = True
        u.save()
        ok(f"Usuario '{username}' actualizado")
        return u, u.profile
    u = User.objects.create_user(username=username, email=email, password=password)
    p = Profile.objects.create(
        user=u, business_name=business_name, ruc=ruc,
        city=city, sector=sector, verified=verified,
        popularity_score=score, bio=bio,
        followers_count=random.randint(10, 200),
        associates_count=random.randint(2, 50),
        collaborations_count=random.randint(1, 20),
    )
    try:
        NotificationPreference.objects.create(user=u)
    except Exception:
        pass
    try:
        KorvaAIConfig.objects.create(user=p)
    except Exception:
        pass
    ok(f"Usuario '{username}' ({business_name})")
    return u, p

def create_post(author, title, content, tags=None, upvotes=0):
    tags = tags or []
    p = Post.objects.create(
        title=title, content=content, author=author,
        moderation_status='approved', upvotes=upvotes,
        timestamp=timezone.now() - timedelta(hours=random.randint(1, 720)),
    )
    for t in tags:
        p.tags.add(t)
    return p

def create_comment(post, author, content):
    return Comment.objects.create(post=post, author=author, content=content)

def create_product(user, name, desc, price, currency, category, whatsapp):
    return Product.objects.create(
        user=user, name=name, description=desc,
        price=Decimal(str(price)), currency=currency,
        category=category, contact_whatsapp=whatsapp,
        is_active=True, views_count=random.randint(5, 300),
    )

def create_review(reviewer, seller, rating, comment):
    try:
        return Review.objects.create(
            reviewer=reviewer, seller=seller,
            rating=rating, comment=comment,
        )
    except Exception:
        return None

def create_conversation(u1, u2):
    c, _ = Conversation.objects.get_or_create(
        user1=u1, user2=u2,
        defaults={'created_at': timezone.now() - timedelta(days=random.randint(1, 60))},
    )
    return c

def create_message(sender, recipient, content, minutes_ago=0):
    return Message.objects.create(
        sender=sender, recipient=recipient,
        content=content,
        timestamp=timezone.now() - timedelta(minutes=minutes_ago),
    )

section("CREANDO USUARIOS DEMO")

u_admin, p_admin = create_user('admin', 'admin@korva.ni', 'admin123',
    'Administración Korva', 'managua', 'servicios', f'J031{RUC_BASE+0}', verified=True, score=9999,
    bio="Administrador de la red de PyMEs de Nicaragua")

u_panaderia, p_panaderia = create_user('panaderia_nic', 'pan@korva.ni', 'demo1234',
    'Panadería Nicaragüeña', 'managua', 'alimentos', f'J031{RUC_BASE+1}', verified=True, score=4200,
    bio="Panadería artesanal desde 1998. Pan de casa, postres tradicionales y repostería fina.")

u_artesanias, p_artesanias = create_user('artesanias_esteli', 'arte@korva.ni', 'demo1234',
    'Artesanías Estelí', 'esteli', 'artesanias', f'J031{RUC_BASE+2}', verified=True, score=3800,
    bio="Artesanía nicaragüense con más de 20 años de tradición. Cerámica, cuero, madera y textiles.")

u_tech, p_tech = create_user('tech_nic', 'tech@korva.ni', 'demo1234',
    'Tech Solutions Nicaragua', 'managua', 'tecnologia', f'J031{RUC_BASE+3}', verified=True, score=5100,
    bio="Empresa de desarrollo de software y consultoría IT. Especialistas en soluciones web y móviles.")

u_cafe, p_cafe = create_user('cafe_montana', 'cafe@korva.ni', 'demo1234',
    'Café de Montaña', 'jinotega', 'alimentos', f'J031{RUC_BASE+4}', verified=True, score=3500,
    bio="Café orgánico de altura cultivado en las montañas de Jinotega. Sabor inigualable.")

u_textil, p_textil = create_user('textiles_leon', 'textil@korva.ni', 'demo1234',
    'Textiles León', 'leon', 'textil', f'J031{RUC_BASE+5}', verified=True, score=2900,
    bio="Fabricantes de textiles desde 2005. Ropa de calidad, uniformes empresariales y más.")

u_agro, p_agro = create_user('agro_masaya', 'agro@korva.ni', 'demo1234',
    'AgroMasaya', 'masaya', 'agropecuario', f'J031{RUC_BASE+6}', verified=True, score=2700,
    bio="Productos agropecuarios frescos directo del campo a tu mesa. Frutas, verduras y lácteos.")

u_granada, p_granada = create_user('granada_servicios', 'serv@korva.ni', 'demo1234',
    'Servicios Granada', 'granada', 'servicios', f'J031{RUC_BASE+7}', verified=True, score=2100,
    bio="Servicios profesionales para PyMEs: contabilidad, legal, marketing y más.")

u_bio, p_bio = create_user('bio_nic', 'bio@korva.ni', 'demo1234',
    'Bio Nicaragua', 'matagalpa', 'alimentos', f'J031{RUC_BASE+8}', verified=False, score=800,
    bio="Emprendimiento de productos orgánicos y naturales. Cosméticos naturales y alimentos saludables.")

users_list = [
    (u_panaderia, p_panaderia), (u_artesanias, p_artesanias),
    (u_tech, p_tech), (u_cafe, p_cafe), (u_textil, p_textil),
    (u_agro, p_agro), (u_granada, p_granada), (u_bio, p_bio),
]
all_profiles = [p_admin] + [p for _, p in users_list]

section("CREANDO POSTS SOCIALES")

posts_data = [
    # Panadería
    (p_panaderia, "Buscamos alianza para distribución de productos",
     "Somos una panadería en Managua buscando socios para ampliar nuestra red de distribución. Ofrecemos pan fresco, postres y repostería. ¡Interesados escríbannos!",
     ["negocio", "alianza", "panaderia"], 24),
    (p_panaderia, "Nuevo producto: Pastel de Tres Leches Artesanal",
     "Lanzamos nuestro nuevo pastel de tres leches, horneado diariamente con receta tradicional. Perfecto para celebraciones empresariales. 🎂",
     ["producto", "reposteria"], 18),
    # Artesanías
    (p_artesanias, "Feria de Artesanías en Estelí - Julio 2026",
     "Invitamos a todos los emprendedores a participar en la Feria de Artesanías de Estelí. Habrá stands, talleres y networking. ¡No falten!",
     ["evento", "feria", "artesanias"], 31),
    (p_artesanias, "Nueva colección cerámica tradicional",
     "Acabamos de lanzar nuestra nueva colección de cerámica pintada a mano, inspirada en motivos precolombinos. Envíos a todo el país.",
     ["producto", "ceramica"], 15),
    # Tech
    (p_tech, "Servicios de Desarrollo Web para PyMEs",
     "¿Necesitas una página web para tu negocio? Ofrecemos desarrollo web, apps móviles y consultoría tecnológica con precios especiales para PyMEs nicaragüenses.",
     ["servicios", "tecnologia", "web"], 42),
    (p_tech, "Tips de ciberseguridad para tu negocio",
     "Proteger tu negocio es fundamental. Compartimos 5 tips básicos de ciberseguridad que toda PyME debería implementar hoy mismo.",
     ["seguridad", "tips"], 27),
    # Café
    (p_cafe, "Café de altura: conoce nuestro proceso",
     "Desde las montañas de Jinotega hasta tu taza. Te mostramos el proceso de cultivo, cosecha y tueste de nuestro café orgánico de altura.",
     ["cafe", "organico", "jinotega"], 35),
    (p_cafe, "Oferta especial: Café Orgánico por suscripción",
     "Nueva modalidad de suscripción mensual. Recibe café fresco tostado en tu negocio cada mes. Precios especiales para PyMEs aliadas.",
     ["oferta", "suscripcion"], 20),
    # Textil
    (p_textil, "Fabricamos uniformes empresariales",
     "Cotiza tus uniformes con nosotros. Tela de alta calidad, diseños personalizados y entrega puntual. Trabajamos con empresas de todo el país.",
     ["uniformes", "textil"], 22),
    (p_textil, "Nueva línea de ropa sostenible",
     "Estrenamos línea de ropa hecha con materiales reciclados y procesos sostenibles. Moda consciente para Nicaragua.",
     ["sostenible", "moda"], 14),
    # Agro
    (p_agro, "Cosecha del mes: frutas tropicales",
     "Tenemos disponibilidad de mango, papaya, piña y banano orgánico. Venta al por mayor y por menor. Entregas en Masaya y Managua.",
     ["agricultura", "fresco"], 16),
    # Servicios
    (p_granada, "Asesoría contable gratuita para nuevos emprendedores",
     "Ofrecemos primera asesoría contable gratuita para emprendedores. Ayudamos a formalizar tu negocio y llevar tus cuentas en orden.",
     ["contabilidad", "asesoria"], 29),
    # Bio
    (p_bio, "Lanzamos jabones artesanales naturales",
     "Nuevos jabones artesanales hechos con ingredientes 100% naturales. Sin químicos, amigables con el medio ambiente.",
     ["natural", "cosmetico"], 8),
    (p_admin, "Bienvenidos a Korva - Red de PyMEs Nicaragüenses",
     "Korva es la red social para pequeñas y medianas empresas de Nicaragua. Conéctate, colabora y haz crecer tu negocio. ¡Únete a nuestra comunidad!",
     ["bienvenida", "comunidad"], 56),
]

created_posts = []
for author, title, content, tags, upvotes in posts_data:
    post = create_post(author, title, content, tags, upvotes)
    created_posts.append(post)
    ok(f"Post: {title[:45]}...")

section("CREANDO COMENTARIOS")

comments_data = [
    (created_posts[0], p_tech, "¡Nos interesa! Trabajamos con varias empresas que distribuyen alimentos. Escríbanos."),
    (created_posts[0], p_cafe, "Podríamos distribuir su pan en Jinotega. Contáctenos."),
    (created_posts[1], p_cafe, "El tres leches se ve delicioso. ¿Hacen envíos a Jinotega?"),
    (created_posts[1], p_panaderia, "Sí, hacemos envíos a todo el país. Escríbanos al WhatsApp."),
    (created_posts[2], p_artesanias, "¡Todos invitados! También tendremos talleres de cerámica."),
    (created_posts[2], p_textil, "Confirmamos participación. Llevaremos nuestra nueva colección."),
    (created_posts[3], p_admin, "Excelente trabajo. La cerámica nicaragüense es reconocida mundialmente."),
    (created_posts[4], p_agro, "¿Tienen planes para negocios agrícolas? Nos interesa."),
    (created_posts[4], p_tech, "Sí, tenemos paquetes especiales para el sector agropecuario."),
    (created_posts[5], p_panaderia, "Muy útiles estos tips. Gracias por compartir."),
    (created_posts[6], p_tech, "El café de Jinotega es el mejor. Buen producto."),
    (created_posts[6], p_textil, "¿Venden al por mayor para empresas?"),
    (created_posts[7], p_artesanias, "Nos encantaría distribuir su café en nuestra tienda."),
    (created_posts[8], p_agro, "Cotizamos 50 uniformes para nuestro equipo. Les escribimos."),
    (created_posts[9], p_admin, "Excelente iniciativa. La moda sostenible es el futuro."),
    (created_posts[10], p_panaderia, "Necesitamos fruta fresca para nuestros postres. Cotización por favor."),
    (created_posts[11], p_bio, "Gracias por el apoyo a emprendedores. Excelente iniciativa."),
    (created_posts[11], p_cafe, "Muy buen servicio. Recomendado."),
    (created_posts[12], p_granada, "Me encantan los productos naturales. Buena suerte con el emprendimiento."),
    (created_posts[13], p_tech, "Gran iniciativa. Nos sumamos a la comunidad."),
    (created_posts[13], p_cafe, "Bienvenidos todos. Korva es una gran plataforma."),
    (created_posts[13], p_artesanias, "Contentos de ser parte de esta comunidad."),
]

for post, author, content in comments_data:
    create_comment(post, author, content)
ok(f"{len(comments_data)} comentarios creados")

section("CREANDO PRODUCTOS EN MARKETPLACE")

products_data = [
    (p_panaderia, "Pan de Casa x50 unidades", "Pan artesanal horneado diariamente. Ideal para restaurantes y cafeterías.", 250, "NIO", "ventas", "+50588880001"),
    (p_panaderia, "Pastel Tres Leches Grande", "Pastel tres leches tradicional, 30 porciones. Encargos con 24h de anticipación.", 650, "NIO", "ventas", "+50588880001"),
    (p_artesanias, "Set de Cerámica Pintada a Mano", "Juego de 6 piezas de cerámica decorativa pintada a mano. Arte tradicional nicaragüense.", 1200, "NIO", "ventas", "+50588880002"),
    (p_artesanias, "Hamaca Nicaragüense", "Hamaca tejida a mano 100% algodón. Varios colores disponibles.", 1800, "NIO", "ventas", "+50588880002"),
    (p_tech, "Página Web para PyME - Plan Básico", "Sitio web profesional con dominio, hosting y 5 secciones. Incluye WhatsApp integrado.", 250, "USD", "ventas", "+50588880003"),
    (p_tech, "App Móvil Corporativa", "Aplicación móvil para tu negocio. Android y iOS. Incluye panel administrativo.", 800, "USD", "ventas", "+50588880003"),
    (p_cafe, "Café Orgánico de Altura - 1lb", "Café 100% arábica cultivado en Jinotega. Tostado medio, molido o en grano.", 180, "NIO", "ventas", "+50588880004"),
    (p_cafe, "Café Suscripción Mensual x5lbs", "Recibe 5 libras de café fresco cada mes. Precio especial para negocios.", 750, "NIO", "ventas", "+50588880004"),
    (p_textil, "Uniformes Empresariales x10", "Juego de 10 uniformes personalizados con logo bordado. Tela duradera.", 4500, "NIO", "ventas", "+50588880005"),
    (p_textil, "Camisetas Algodón x50", "50 camisetas de algodón 100% personalizadas con serigrafía.", 3500, "NIO", "ventas", "+50588880005"),
    (p_agro, "Canasta de Frutas Tropicales", "Canasta con 10lbs de frutas frescas de temporada. Mango, papaya, piña, banano.", 350, "NIO", "ventas", "+50588880006"),
    (p_agro, "Queso Fresco Artesanal x1lb", "Queso fresco elaborado diariamente. Productos lácteos de calidad.", 80, "NIO", "ventas", "+50588880006"),
    (p_granada, "Asesoría Contable Mensual", "Servicio de contabilidad mensual para PyMEs. Incluye declaraciones y balances.", 150, "USD", "ventas", "+50588880007"),
    (p_granada, "Kit Emprendedor - Constitución Legal", "Te ayudamos a constituir legalmente tu negocio. Incluye registro y permisos.", 300, "USD", "ventas", "+50588880007"),
    (p_bio, "Jabón Artesanal Natural x3", "Set de 3 jabones artesanales: miel, avena y carbón activado. 100% naturales.", 200, "NIO", "ventas", "+50588880008"),
]

created_products = []
for user, name, desc, price, currency, cat, wa in products_data:
    p = create_product(user, name, desc, price, currency, cat, wa)
    created_products.append(p)
ok(f"{len(products_data)} productos creados")

section("CREANDO REVIEWS")

reviews_data = [
    (p_tech, p_panaderia, 5, "Excelente panadería, productos frescos y puntuales. Recomendados."),
    (p_cafe, p_artesanias, 4, "Hermosa artesanía. Compramos para regalos corporativos y todos quedaron encantados."),
    (p_panaderia, p_agro, 5, "Fruta fresca de primera calidad. Trabajamos con ellos semanalmente."),
    (p_textil, p_tech, 5, "Desarrollaron nuestra página web. Excelente servicio y atención."),
    (p_agro, p_cafe, 5, "El mejor café de Jinotega. Distribuimos en nuestra tienda."),
    (p_granada, p_tech, 4, "Buen servicio técnico. Resolvieron nuestros problemas IT rápidamente."),
    (p_admin, p_panaderia, 5, "Empresa verificada, productos de excelente calidad."),
    (p_admin, p_tech, 5, "Partner tecnológico de Korva. Profesionalismo y calidad."),
    (p_bio, p_granada, 5, "Gracias a su asesoría pudimos formalizar nuestro emprendimiento."),
    (p_artesanias, p_textil, 4, "Buenos uniformes, tela de calidad y entrega a tiempo."),
]

for reviewer, seller, rating, comment in reviews_data:
    create_review(reviewer, seller, rating, comment)
ok(f"{len(reviews_data)} reseñas creadas")

section("CREANDO CONVERSACIONES Y MENSAJES")

create_conversation(p_panaderia, p_tech)
create_message(p_panaderia, p_tech, "Hola Tech Solutions, nos interesa crear una página web para nuestra panadería. ¿Podrían darnos información?", minutes_ago=2880)
create_message(p_tech, p_panaderia, "¡Claro! Con gusto. Tenemos un plan básico de $250 que incluye dominio, hosting, 5 secciones y WhatsApp integrado.", minutes_ago=2850)
create_message(p_panaderia, p_tech, "Suena bien. ¿Cuánto tiempo toma el desarrollo?")
create_message(p_tech, p_panaderia, "Normalmente 2-3 semanas. Incluye diseño, desarrollo y capacitación. ¿Agendamos una reunión?")
create_message(p_panaderia, p_tech, "Sí, por favor. Estamos listos para empezar.")

create_conversation(p_artesanias, p_cafe)
create_message(p_artesanias, p_cafe, "Hola Café de Montaña. Nos encantaría distribuir su café en nuestra tienda de artesanías.", minutes_ago=4320)
create_message(p_cafe, p_artesanias, "¡Hola! Qué bien. Trabajamos con presentaciones de 1lb y 5lbs. ¿Qué volumen les interesa?")
create_message(p_artesanias, p_cafe, "Empezaríamos con 20lbs mensuales. ¿Tienen precio especial por volumen?")

create_conversation(p_textil, p_agro)
create_message(p_textil, p_agro, "Buenos días, cotizamos 50 uniformes para nuestro equipo de campo.", minutes_ago=720)
create_message(p_agro, p_textil, "¡Hola Textiles! Claro, necesitamos 50 camisas manga corta con logo bordado. ¿Tienen disponibilidad?")

create_conversation(p_bio, p_granada)
create_message(p_bio, p_granada, "Hola, nos recomendaron su asesoría contable. Somos un emprendimiento nuevo de productos naturales.", minutes_ago=1440)
create_message(p_granada, p_bio, "¡Bienvenidos! Tenemos un kit especial para nuevos emprendedores. ¿Cuándo podemos reunirnos?")
create_message(p_bio, p_granada, "Esta semana. ¿Jueves en la tarde?")
create_message(p_granada, p_bio, "Perfecto, jueves a las 3pm. Les enviamos la dirección.")

ok("Conversaciones y mensajes creados")

section("CREANDO EVENTOS")

for i, (org, title, desc, cat, city, days_ahead) in enumerate([
    (p_tech, "Taller: Marketing Digital para PyMEs", "Aprende estrategias de marketing digital para hacer crecer tu negocio en línea. Cupo limitado.", "taller", "managua", 15),
    (p_artesanias, "Feria de Artesanías y Cultura 2026", "La feria más grande de artesanías en Estelí. Participan más de 50 expositores.", "feria", "esteli", 30),
    (p_cafe, "Cata de Café de Altura", "Evento de cata de café orgánico de las montañas de Jinotega. Entrada gratuita.", "taller", "jinotega", 10),
    (p_admin, "Networking Empresarial Korva", "Evento mensual de networking para miembros de Korva. Conecta con otros emprendedores.", "networking", "managua", 7),
    (p_textil, "Conferencia: Moda Sostenible", "Conferencia sobre moda sostenible y el futuro de la industria textil en Nicaragua.", "conferencia", "leon", 21),
    (p_granada, "Taller: Cómo formalizar tu negocio", "Taller práctico sobre constitución legal, registros y permisos para PyMEs.", "taller", "granada", 14),
]):
    Event.objects.create(
        title=title, description=desc, category=cat,
        organizer=org, date=timezone.now().date() + timedelta(days=days_ahead),
        location=f"{city.title()}, Nicaragua", city=city,
        max_attendees=50 + i * 10,
    )
ok("6 eventos creados")

section("CREANDO GRUPOS POR SECTOR")

group1 = Group.objects.create(
    name="Tecnología & Innovación", sector="tecnologia",
    description="Grupo de empresas del sector tecnología. Compartimos conocimientos, oportunidades y alianzas estratégicas.",
    admin=p_tech,
)
group1.members.add(p_tech, p_panaderia, p_artesanias, p_admin)

group2 = Group.objects.create(
    name="Alimentos y Agroindustria", sector="alimentos",
    description="Red de productores y distribuidores de alimentos. Intercambio de productos, proveedores y mejores prácticas.",
    admin=p_cafe,
)
group2.members.add(p_cafe, p_panaderia, p_agro, p_bio, p_admin)

group3 = Group.objects.create(
    name="Artesanías y Cultura", sector="artesanias",
    description="Preservando la cultura nicaragüense a través de la artesanía. Colaboraciones y ferias.",
    admin=p_artesanias,
)
group3.members.add(p_artesanias, p_admin)

GroupPost.objects.create(group=group1, author=p_tech, content="Comparto este artículo sobre tendencias tecnológicas para PyMEs en 2026.")
GroupPost.objects.create(group=group2, author=p_cafe, content="Buenos días a todos. ¿Alguien conoce proveedores de empaques ecológicos para alimentos?")
GroupPost.objects.create(group=group3, author=p_artesanias, content="Recordatorio: la Feria de Artesanías es en julio. Confirmar participación antes del 15.")

ok("3 grupos creados")

section("CREANDO NOTIFICACIONES")

notif_types = ['like', 'comment', 'follow', 'system', 'message']
for u, _ in users_list[:4]:
    for _ in range(3):
        sender = random.choice([su for su, _ in users_list if su != u])
        nt = random.choice(notif_types)
        titles = {
            'like': 'Nuevo like en tu publicación',
            'comment': 'Nuevo comentario en tu publicación',
            'follow': 'Nuevo seguidor',
            'system': 'Notificación del sistema',
            'message': 'Nuevo mensaje',
        }
        msgs = {
            'like': f'A {sender.profile.business_name} le gustó tu publicación.',
            'comment': f'{sender.profile.business_name} comentó en tu publicación.',
            'follow': f'{sender.profile.business_name} comenzó a seguirte.',
            'system': 'Tu perfil ha sido verificado correctamente.',
            'message': f'{sender.profile.business_name} te envió un mensaje.',
        }
        try:
            Notification.objects.create(
                recipient=u, sender=sender,
                notification_type=nt,
                title=titles[nt], message=msgs[nt],
                is_read=random.choice([True, False]),
                created_at=timezone.now() - timedelta(hours=random.randint(1, 168)),
            )
        except Exception:
            pass

ok("Notificaciones creadas")

section("CREANDO CUENTAS BANCARIAS (DEMO)")

bank_accounts = [
    (p_tech, "lafise", "ahorro", "100-123-456-789", "Tech Solutions Nicaragua", "J0310000000004", "+50588880003"),
    (p_panaderia, "banpro", "monetaria", "101-987-654-321", "Panadería Nicaragüeña", "J0310000000002", "+50588880001"),
    (p_cafe, "bac", "monetaria", "102-456-789-123", "Café de Montaña", "J0310000000005", "+50588880004"),
]
for seller, bank, atype, acct, holder, idn, phone in bank_accounts:
    BankAccount.objects.update_or_create(
        seller=seller,
        defaults=dict(
            bank=bank, account_type=atype,
            account_number=acct, account_holder=holder,
            id_number=idn, phone=phone, verified=True,
        ),
    )
ok("Cuentas bancarias demo creadas")

section("CREANDO TRANSACCIONES DEMO")

txns = [
    (created_products[0], p_tech, p_panaderia, "250.00", "NIO", "completed", "KORVA-DEMO-001"),
    (created_products[2], p_cafe, p_artesanias, "1200.00", "NIO", "completed", "KORVA-DEMO-002"),
    (created_products[4], p_panaderia, p_tech, "250.00", "USD", "pending", "KORVA-DEMO-003"),
]
for prod, buyer, seller, amt, ccy, status, ref in txns:
    Transaction.objects.update_or_create(
        reference=ref,
        defaults=dict(product=prod, buyer=buyer, seller=seller,
                      amount=Decimal(amt), currency=ccy, status=status),
    )
ok("Transacciones demo creadas")

section("CREANDO DEALS/OFERTAS")

now = timezone.now()
deals = [
    (created_products[6], p_cafe, "Oferta Café 2x1", "Compra 2 libras de café y llévate una gratis.", Decimal("180.00"), Decimal("360.00"), Decimal("180.00"), 7),
    (created_products[1], p_panaderia, "Pastel Tres Leches + Pan", "Pastel tres leches + 10 panes de casa a precio especial.", Decimal("750.00"), Decimal("850.00"), Decimal("100.00"), 10),
    (created_products[5], p_tech, "App + Web Pack", "Contrata app móvil y sitio web juntos y ahorra.", Decimal("950.00"), Decimal("1050.00"), 0, 15),
]
for prod, seller, title, desc, deal_price, orig_price, discount, days in deals:
    Deal.objects.update_or_create(
        product=prod,
        defaults=dict(
            seller=seller, title=title, description=desc,
            discount_percent=int((1 - float(deal_price)/float(orig_price)) * 100) if orig_price > 0 else 0,
            original_price=orig_price, deal_price=deal_price,
            starts_at=now, ends_at=now + timedelta(days=days),
            is_active=True,
        ),
    )
ok("Ofertas activas creadas")

section("ACTIVANDO ADMINISTRADOR KORVA")
try:
    u_admin.is_superuser = True
    u_admin.is_staff = True
    u_admin.save()
    ok("Usuario admin activado como superusuario")
except Exception:
    pass

section("RESUMEN")
total_users = User.objects.count()
total_profiles = Profile.objects.count()
total_posts = Post.objects.count()
total_comments = Comment.objects.count()
total_products = Product.objects.count()
total_reviews = Review.objects.count()
total_conversations = Conversation.objects.count()
total_messages = Message.objects.count()
total_notifications = Notification.objects.count()

print(f"""
  {'='*40}
    USUARIOS:     {total_users}
    PERFILES:     {total_profiles}
    POSTS:        {total_posts}
    COMENTARIOS:  {total_comments}
    PRODUCTOS:    {total_products}
    RESEÑAS:      {total_reviews}
    CONVERSACIONES: {total_conversations}
    MENSAJES:     {total_messages}
    NOTIFICACIONES: {total_notifications}
  {'='*40}

  [OK] Base de datos poblada exitosamente!
  [OK] La app ahora tiene vida!

  Cuentas demo (password: demo1234):
    admin           - Administración Korva
    panaderia_nic   - Panadería Nicaragüeña
    artesanias_esteli - Artesanías Estelí
    tech_nic        - Tech Solutions Nicaragua
    cafe_montana    - Café de Montaña
    textiles_leon   - Textiles León
    agro_masaya     - AgroMasaya
    granada_servicios - Servicios Granada
    bio_nic         - Bio Nicaragua
""")
