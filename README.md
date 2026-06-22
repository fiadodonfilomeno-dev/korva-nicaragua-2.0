# Korva Nicaragua 2.0

Plataforma de red social PyME para empresas en Nicaragua. Networking, marketplace, mensajería y colaboración empresarial.

## Bugs

### Resueltos ✅
- **Mensajería** - Fotos, videos, burbujas de chat, doble check de lectura
- **Chatbot tutorial** - Tutorial + links para API key cuando no está configurada
- **Posts con imágenes/videos** - Campo video en Post, upload y display
- **Perfil estilo Discord** - Banner, avatar circular, badges, stats
- **Rankings divididos** - General, Novatos (&lt; 1000 pts), Establecidas (1000+ pts)
- **Frontend mejorado** - Animaciones, scrollbar, transiciones, sombras
- Rankings sin template → Creado `rankings/rankings.html`
- Korva IA sin templates ni error handling → Creados templates + try-except
- Mensajería sin templates ni error handling → Creados templates + try-except
- Perfiles sin template ni error handling → Creado `users/profile.html` + try-except
- Like/Dislike: AttributeError → Operaciones directas en campos + modelo Vote
- Image Upload sin error handling → try-except en vistas
- Comentarios sin template funcional → Integrado en `post_detail.html`

### Pendientes
- [ ] Configurar Google Gemini API key en `settings.py` para chatbot funcional
- [ ] Sistema de notificaciones en tiempo real (WebSockets)
- [ ] Verificación de email al registrarse
- [ ] Modo oscuro/claro toggle
- [ ] API REST para app móvil

## Características

- **Landing Page** - Página de inicio atractiva para usuarios no autenticados
- **Muro Social** - Publicaciones con imágenes, videos, galería múltiple, votos (uno por cuenta) y comentarios
- **Marketplace** - Publicación y búsqueda de productos con imágenes
- **Rankings** - Leaderboard con categorías (General/Novatos/Establecidas) y niveles Bronce/Plata/Oro/VIP
- **Mensajería** - Chat privado entre empresas con fotos, videos y doble check de lectura
- **Korva IA** - Asistente inteligente con restricciones temáticas + tutorial interactivo
- **Perfiles estilo Discord** - Banner, avatar circular, badges/logros, stats cards
- **Reportes** - Exportación de analytics en CSV/PDF
- **Admin** - Panel de moderación completo con acciones masivas

## Tecnologías

- Django 6.0.5 / Python 3.14
- SQLite (configurable a MySQL)
- Tailwind CSS (CDN) - Tema oscuro
- Google Gemini API

## Inicio rápido

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Admin: `admin` / `admin123`

## Estructura del proyecto

```
korva_config/       - Configuración Django (settings, urls)
core/               - Rankings, Korva IA, modelos globales
users/              - Perfiles, autenticación
social/             - Posts, comentarios, votos
marketplace/        - Productos, marketplace
messaging/          - Mensajería entre empresas
reports/            - Reportes y analytics
templates/          - Templates HTML
static/             - Archivos estáticos
media/              - Subidas de usuarios
```
