# -*- coding: utf-8 -*-
"""Genera conversaciones de ejemplo entre todos los perfiles para evitar estados vacíos."""
import os, django, sys
sys.path.insert(0, r"C:\Users\DELL 5591\Downloads\korva-nicaragua-main (3)\korva-nicaragua-main")
os.chdir(sys.path[0])
os.environ['DJANGO_SETTINGS_MODULE'] = 'korva_config.settings'
django.setup()
from django.db.models import Q
from users.models import Profile
from messaging.models import Conversation, Message

order = [
    'admin', 'artesanias_esteli', 'cafe_el_cedro', 'consultoria_juridica_nica',
    'granja_don_roberto', 'moda_textil_masaya', 'panaderia_nicaraguena',
    'tech_solutions', 'transporte_cacao_express',
]

by_username = {p.user.username: p for p in Profile.objects.all()}
profiles = [by_username[u] for u in order if u in by_username]
n = len(profiles)

CREATED = 0
SKIPPED = 0

def get_or_create_conv(a, b):
    global CREATED, SKIPPED
    conv = Conversation.objects.filter(
        (Q(user1=a, user2=b) | Q(user1=b, user2=a))
    ).first()
    if conv:
        SKIPPED += 1
        return conv
    # user1 = menor pk para consistencia
    if a.id > b.id:
        a, b = b, a
    conv = Conversation.objects.create(user1=a, user2=b)
    CREATED += 1
    return conv

# Mensajes de ejemplo genéricos pero temáticos por perfil
SAMPLE = {
    'admin': [
        ("Hola, le escribimos desde Administración Korva. ¿Cómo va su negocio?", None),
        ("Recuerde mantener su perfil actualizado con fotos y promociones.", None),
        ("Estamos disponibles ante cualquier consulta sobre la plataforma.", None),
    ],
    'artesanias_esteli': [
        ("Hola, nos interesa ofrecer nuestras piezas artesanales a más clientes.", None),
        ("Tenemos bordados y cerámica hechos a mano con calidad certificada.", None),
        ("¿Les interesaría una muestra para un pedido piloto?", None),
    ],
    'cafe_el_cedro': [
        ("Ofrecemos café de especialidad con tueste medio y oscuro.", None),
        ("Nuestra finca certificada de Jinotega garantiza granos de altura.", None),
        ("Podemos distribuir a negocios de la zona. ¿Conversamos?", None),
    ],
    'consultoria_juridica_nica': [
        ("Brindamos asesoría legal para constitución y formalización de PyMEs.", None),
        ("Manejo de contratos comerciales y cumplimiento DGI.", None),
        ("¿Necesita una revisión de sus procesos legales?", None),
    ],
    'granja_don_roberto': [
        ("Buenas, producimos queso y lácteos frescos cada semana.", None),
        ("Podemos abastecer comercios con entrega puntual.", None),
        ("¿Les gustaría un pedido de prueba?", None),
    ],
    'moda_textil_masaya': [
        ("Elaboramos prendas textiles y bordados en Masaya.", None),
        ("Buenas opciones de precio para proveedores y tiendas.", None),
        ("Podemos enviar catálogo por si les interesa.", None),
    ],
    'panaderia_nicaraguena': [
        ("Producimos pan artesanal y repostería a diario.", None),
        ("Ideal para cafés y restaurantes que buscan proveedor constante.", None),
        ("¿Coordinamos un pedido de prueba?", None),
    ],
    'tech_solutions': [
        ("Ofrecemos desarrollo web, facturación y sistemas a la medida.", None),
        ("Planes desde los primeros meses para PyMEs.", None),
        ("Podemos agendar una demo del sistema.", None),
    ],
    'transporte_cacao_express': [
        ("Somos especialistas en transporte y logística de carga.", None),
        ("Rutas consolidadas hacia Managua, León y Granada.", None),
        ("¿Cotizamos un envío para su producto?", None),
    ],
}

def add_messages(a, b, conv):
    msgs = []
    sender_msgs = [m for m in SAMPLE.get(a.user.username, [])][:2]
    b_side = [m for m in SAMPLE.get(b.user.username, [])][:2]
    # Aprox: un diálogo de 4 mensajes alternados
    for i, (t, _img) in enumerate(sender_msgs[:2]):
        msg = Message.objects.create(sender=a, recipient=b, content=t)
        msg.read_by.add(b)
        msgs.append(msg)
    for i, (t, _img) in enumerate(b_side[:2]):
        msg = Message.objects.create(sender=b, recipient=a, content=t)
        msg.read_by.add(a)
        msgs.append(msg)
    # actualizar updated_at del conv
    if msgs:
        conv.updated_at = msgs[-1].timestamp
        conv.save()

for i in range(n):
    a = profiles[i]
    b = profiles[(i + 1) % n]
    conv = get_or_create_conv(a, b)
    add_messages(a, b, conv)

print(f'Conversaciones creadas: {CREATED}')
print(f'Conversaciones existentes omitidas: {SKIPPED}')

# Verificación final
from django.db.models import Count, F
for p in Profile.objects.all():
    n1 = p.conversations_as_user1.count() + p.conversations_as_user2.count()
    print(f'  {p.business_name}: {n1} conversaciones')