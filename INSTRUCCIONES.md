# INSTRUCCIONES DE EJECUCIÓN - Korva Nicaragua v2.0

## 📋 Resumen

Korva Nicaragua es una plataforma web completa construida con Django que implementa todas las especificaciones solicitadas:

✓ Muro Social con sistema de votos
✓ Marketplace de Productos y Servicios
✓ Rankings dinámicos de Popularidad
✓ Mensajería Privada entre usuarios
✓ Asistente IA Korva (integración con Google Gemini)
✓ Exportación de Reportes (CSV y PDF)
✓ Sistema de Tiers/Niveles (Bronce, Plata, Oro, VIP)
✓ Validación de RUC con bonificación
✓ Tema Oscuro Sofisticado con Tailwind CSS

---

## 🚀 INICIO RÁPIDO

### 1. Instalar Dependencias
```bash
cd "C:\Users\harif\Desktop\Korva2.0"
pip install -r requirements.txt
```

### 2. Iniciar el Servidor
```bash
python manage.py runserver
```

### 3. Acceder a la Aplicación
- **URL Principal**: http://127.0.0.1:8000
- **Panel Admin**: http://127.0.0.1:8000/admin

---

## 👤 Cuentas de Prueba

```
ADMIN:
  Usuario: admin
  Contraseña: admin123
  
USUARIOS DE PRUEBA:
  Usuario: panaderia_nicaraguena
  Contraseña: test1234
  
  Usuario: artesanias_esteli
  Contraseña: test1234
  
  Usuario: tech_solutions
  Contraseña: test1234
```

---

## 📍 RUTAS PRINCIPALES

### Autenticación
- `/register/` - Registro de nuevos usuarios
- `/login/` - Iniciar sesión
- `/logout/` - Cerrar sesión

### Muro Social
- `/` - Página principal (feed de posts)
- `/post/create/` - Crear nuevo post
- `/post/<id>/` - Ver detalle del post
- `/post/<id>/edit/` - Editar post
- `/post/<id>/delete/` - Eliminar post

### Marketplace
- `/marketplace/` - Catálogo de productos
- `/product/create/` - Publicar nuevo producto
- `/product/<id>/` - Ver detalle del producto
- `/my-products/` - Mis productos publicados

### Usuarios
- `/profile/<username>/` - Ver perfil de usuario
- `/edit-profile/` - Editar mi perfil
- `/dashboard/` - Dashboard personal

### Rankings
- `/rankings/` - Leaderboard de popularidad

### Mensajería
- `/messages/` - Lista de conversaciones
- `/conversation/<id>/` - Ver conversación
- `/start-conversation/<username>/` - Iniciar conversación

### Asistente IA
- `/ai/` - Panel principal de Korva IA
- `/ai/new/` - Nueva conversación
- `/ai/conversation/<id>/` - Chat con IA
- `/ai/quick-prompts/` - Prompts predefinidos

### Reportes
- `/reports/` - Panel de reportes
- `/reports/export-csv/` - Descargar CSV
- `/reports/export-pdf/` - Descargar PDF

---

## 🔧 CONFIGURACIÓN DE GOOGLE GEMINI (Opcional)

Para habilitar el Asistente IA, necesitas una clave de API de Google Gemini:

1. Obtén tu clave en: https://ai.google.dev/
2. Abre `korva_config/settings.py`
3. Agrega esta línea:
```python
GEMINI_API_KEY = 'tu-clave-de-api-aqui'
```

Sin esta configuración, los usuarios verán un mensaje de error al intentar usar la IA.

---

## 📊 ESTRUCTURA DE DATOS

### Modelos Principales

**Profile** (Perfil Empresarial)
- business_name: Nombre comercial
- ruc: Registro Único de Contribuyente
- verified: Sello de verificación oficial
- popularity_score: Puntuación de reputación
- tier: Nivel dinámico (Bronce, Plata, Oro, VIP)

**Post** (Publicación en Muro)
- title: Título del post
- content: Contenido
- tags: Etiquetas
- upvotes/downvotes: Sistema de votos
- moderation_status: Estado de moderación

**Product** (Producto en Marketplace)
- name: Nombre del producto
- price: Precio
- currency: Moneda (NIO o USD)
- category: Ventas o Compras
- contact_whatsapp: Número para contacto

**Message** (Mensaje Privado)
- content: Contenido del mensaje
- read_status: ¿Leído o no?
- timestamp: Fecha/hora

**AIConversation & AIMessage** (Conversaciones con IA)
- Historial de chats con Korva IA

**AnalyticsReport** (Reportes)
- total_posts, total_products, etc.

---

## 🎨 DISEÑO Y COLORES

La aplicación utiliza un tema oscuro sofisticado con:

```
Colores Principales:
- Fondo: #09090b (Slate muy oscuro)
- Cards: #0c0c0e
- Éxito/Botones: #10b981 (Verde Esmeralda)
- Advertencias: #f59e0b (Ámbar)
- Bordes: #1a1a1d (Gris oscuro)

Tipografía:
- Inter: Texto general
- Fira Code: Números y valores
```

---

## 📱 CARACTERÍSTICAS IMPLEMENTADAS

### 1. Muro Social ✓
- Crear, editar y eliminar posts
- Sistema de upvote/downvote (+10/-5 puntos)
- Comentarios en posts
- Etiquetas mediante django-taggit
- Búsqueda de posts
- Moderación de contenido

### 2. Marketplace ✓
- Publicar productos/servicios
- Filtrar por categoría
- Búsqueda avanzada
- Integración WhatsApp (wa.me)
- Galería de imágenes
- Contador de visualizaciones

### 3. Rankings ✓
- Leaderboard de popularidad
- Posición en tiempo real del usuario
- Sistema de Tiers dinámicos
- Gráfico de progreso

### 4. Mensajería ✓
- Chat privado entre usuarios
- Historial de conversaciones
- Notificaciones de no leídos
- Marca automática como leído

### 5. Asistente IA ✓
- Integración con Google Gemini
- Historial de conversaciones
- Prompts rápidos predefinidos
- Soporte para API personal del usuario

### 6. Reportes ✓
- Exportación a CSV
- Generación de PDF con diseño profesional
- Estadísticas detalladas
- KPIs empresariales

---

## 🔒 SEGURIDAD

✓ Autenticación con Django
✓ CSRF Protection en formularios
✓ Validación de RUC
✓ Contraseñas hasheadas
✓ Control de permisos por usuario
✓ Validación de entrada en formularios

---

## 💻 TECNOLOGÍA USADA

```
Backend:
- Django 6.0.5
- Python 3
- SQLite (desarrollo) / PostgreSQL (producción)
- django-taggit (para tags)
- google-generativeai (API de Gemini)
- reportlab (generación de PDF)
- Pillow (procesamiento de imágenes)

Frontend:
- HTML5
- Tailwind CSS 3 (CDN)
- Font Awesome 6.4
- Chart.js (opcional para gráficos)

Características:
- Responsive Design
- Dark Mode
- Tema de alto contraste
```

---

## 📖 COMANDOS ÚTILES

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Cargar datos de prueba
python manage.py load_test_data

# Shell Django (para debugging)
python manage.py shell

# Recopilar archivos estáticos (producción)
python manage.py collectstatic --noinput

# Ejecutar tests
python manage.py test

# Resetear base de datos (desarrollo)
rm db.sqlite3
python manage.py migrate
```

---

## 📂 ESTRUCTURA DEL PROYECTO

```
Korva2.0/
├── korva_config/           # Configuración principal
│   ├── settings.py        # Configuraciones de Django
│   ├── urls.py            # Rutas principales
│   └── wsgi.py            # WSGI para producción
│
├── users/                  # App de usuarios
│   ├── models.py          # Modelo Profile
│   ├── views.py           # Vistas de autenticación
│   ├── forms.py           # Formularios
│   └── migrations/        # Migraciones
│
├── social/                 # App de muro social
│   ├── models.py          # Post y Comment
│   ├── views.py           # Vistas
│   ├── forms.py           # Formularios
│   └── migrations/
│
├── marketplace/            # App de marketplace
│   ├── models.py          # Modelo Product
│   ├── views.py           # Vistas
│   ├── forms.py           # Formularios
│   └── migrations/
│
├── messaging/              # App de mensajería
│   ├── models.py          # Message y Conversation
│   ├── views.py           # Vistas
│   ├── forms.py           # Formularios
│   └── migrations/
│
├── reports/                # App de reportes
│   ├── models.py          # AnalyticsReport
│   ├── views.py           # Exportación
│   └── migrations/
│
├── core/                   # App core
│   ├── models.py          # IA y Config
│   ├── ai_views.py        # Vistas de IA
│   ├── rankings_views.py  # Vistas de rankings
│   └── migrations/
│
├── templates/              # Templates globales
│   ├── base.html          # Template base
│   ├── navbar.html        # Barra de navegación
│   ├── footer.html        # Pie de página
│   ├── auth/              # Templates de auth
│   ├── social/            # Templates de muro
│   ├── marketplace/       # Templates de marketplace
│   ├── messaging/         # Templates de mensajes
│   ├── rankings/          # Templates de rankings
│   ├── reports/           # Templates de reportes
│   └── ai/                # Templates de IA
│
├── static/                 # Archivos estáticos (CSS, JS)
├── media/                  # Archivos subidos por usuarios
├── manage.py              # Script de gestión
├── db.sqlite3             # Base de datos (desarrollo)
├── requirements.txt       # Dependencias Python
├── README.md              # Documentación
└── create_admin.py        # Script para crear admin
```

---

## 🐛 SOLUCIÓN DE PROBLEMAS

**Problema**: Error de importación
**Solución**:
```bash
pip install --upgrade -r requirements.txt
```

**Problema**: Puerto 8000 en uso
**Solución**:
```bash
python manage.py runserver 8001
```

**Problema**: Base de datos corrupta
**Solución**:
```bash
rm db.sqlite3
python manage.py migrate
```

**Problema**: Archivos de media no se ven
**Solución**: Verificar que DEBUG = True en settings.py

---

## 📞 SOPORTE

Si encuentras problemas:

1. Verifica que todas las dependencias estén instaladas
2. Asegúrate de que la base de datos esté migrada
3. Comprueba que DEBUG = True en desarrollo
4. Revisa los logs en la consola

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

- [x] Estructura base de Django
- [x] Modelos de base de datos
- [x] Autenticación de usuarios
- [x] Muro Social con votos
- [x] Marketplace con WhatsApp
- [x] Rankings dinámicos
- [x] Mensajería privada
- [x] Asistente IA
- [x] Exportación de reportes
- [x] Sistema de Tiers
- [x] Validación de RUC
- [x] Tema oscuro con Tailwind
- [x] Datos de prueba
- [x] Documentación completa

---

**Versión**: 2.0
**Fecha**: 15 de Junio, 2026
**Estado**: Listo para uso
**Framework**: Django 6.0.5

---

¡Disfruta usando Korva Nicaragua! 🚀
