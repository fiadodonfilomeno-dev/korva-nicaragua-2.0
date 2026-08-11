# Korva Nicaragua 2.0

Plataforma de red social PyME para empresas en Nicaragua. Networking, marketplace, mensajería y colaboración empresarial.

## Características

### Core
- **Landing Page** - Página de inicio atractiva para usuarios no autenticados
- **Perfiles estilo Discord** - Banner, avatar circular, badges/logros, stats cards, verificación
- **Admin** - Panel de moderación completo con acciones masivas
- **Korva IA** - Asistente inteligente con restricciones temáticas + tutorial interactivo (Gemini API)

### Social
- **Muro Social** - Publicaciones con imágenes, videos, galería múltiple, votos AJAX, hashtags clickeables
- **Favoritos** - Guardar posts y productos favoritos con toggle rápido
- **Tiempo Relativo** - Posts muestran "hace 5 min", auto-refresh cada 30s
- **Comentarios** - Sistema de comentarios en publicaciones

### Marketplace
- **Marketplace** - Publicación y búsqueda de productos con imágenes, filtros por categoría
- **Ofertas y Descuentos** - Crear ofertas con % descuento, precio con descuento, fecha de expiración
- **Calificación de Vendedores** - Reviews con estrellas (1-5) y comentarios
- **Exportar Catálogo PDF** - Generar PDF del catálogo de productos con reportlab
- **Favoritos de Productos** - Guardar productos en lista de deseos

### Colaboración
- **Alianzas Recomendadas** - Algoritmo de compatibilidad (ciudad, sector, tags, productos, verificado)
- **Rankings** - Leaderboard con categorías (General/Novatos/Establecidas) y niveles Bronce/Plata/Oro/VIP
- **Mensajería** - Chat privado entre empresas con fotos, videos y doble check de lectura
- **Eventos y Ferias** - Crear, listar y asistir a eventos empresariales
- **Grupos por Sector** - Grupos temáticos con posts, unión y conteo de miembros
- **Mapa de PyMEs** - Visualización en mapa interactivo (Leaflet/OpenStreetMap)

### Analytics
- **Metricas de Alcance** - Dashboard con Chart.js: posts por mes, votos, vistas, Upvotes vs Downvotes
- **Reportes** - Exportación de analytics en CSV/PDF
- **Búsqueda Avanzada** - Buscar empresas, productos, publicaciones y grupos en un solo lugar

## Tecnologías

- Django 6.0.5 / Python 3.14
- SQLite (configurable a MySQL)
- Tailwind CSS (CDN) - Tema oscuro
- Google Gemini API
- Chart.js - Gráficas de métricas
- Leaflet / OpenStreetMap - Mapa interactivo
- ReportLab - Generación de PDFs

## Inicio rápido

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Credenciales de prueba:
- Admin: `admin` / `admin123`
- PyME: `panaderia_nicaraguena` / `panaderianicaraguena`
- PyME: `artesanias_esteli` / `artesaniasesteli`
- PyME: `tech_solutions` / `techsolutions`
- Evaluador: `evaluador` / `evaluador`

## Estructura del proyecto

```
korva_config/       - Configuración Django (settings, urls)
core/               - Rankings, Korva IA, recomendaciones, búsqueda, modelos globales
users/              - Perfiles, autenticación, mapa PyMEs
social/             - Posts, comentarios, votos, favoritos, hashtags, tiempo relativo
marketplace/        - Productos, ofertas, reviews, favoritos, exportar catálogo PDF
messaging/          - Mensajería privada entre empresas
reports/            - Reportes CSV/PDF, métricas de alcance (Chart.js)
events/             - Eventos y ferias empresariales
groups/             - Grupos por sector
templates/          - Templates HTML (tema oscuro)
static/             - Archivos estáticos
media/              - Subidas de usuarios
```

## Rutas principales

| Ruta | Descripción |
|------|-------------|
| `/` | Muro social |
| `/marketplace/` | Marketplace de productos |
| `/recommendations/` | Alianzas recomendadas |
| `/analytics/` | Métricas de alcance (Chart.js) |
| `/search/` | Búsqueda avanzada |
| `/deals/` | Ofertas activas |
| `/events/` | Eventos y ferias |
| `/groups/` | Grupos por sector |
| `/map/` | Mapa de PyMEs |
| `/rankings/` | Rankings de empresas |
| `/export-catalog/` | Exportar catálogo PDF |
| `/ai/` | Korva IA |
| `/reports/` | Reportes y analytics |

## Changelog

### 2026-08-11 — Fixes de renderizado y tema claro/oscuro
- **Imágenes del marketplace arregladas** — Cambiadas de `background-image` CSS a etiqueta `<img>` para que rendericen correctamente (antes salían negras)
- **Tema claro/oscuro funcional** — Toggle ☀️/🌙 en el navbar para cambiar entre fondo blanco y oscuro (antes se quedaba negro sin opción visible)
- **Service worker eliminado** — Removido el SW que servía páginas cacheadas en negro; la página siempre carga fresca
- **Animación CSS nativa** — `.stagger-in` y `.reveal` usan `@keyframes` en vez de `opacity:0` inicial que ocultaba tarjetas si JS fallaba
- **Keep-alive con GitHub Actions** — Ping cada 5 min para evitar que Render Free duerma el sitio (cold start de 30-60s)

### 2026-08-11 — Imágenes reales locales
- **Fotos reales alojadas en el proyecto** (`static/img/real/`) — pan, tres leches, café, cerámica, hamacas, computación, apps y eventos; sin dependencia de enlaces externos
- **Logos de empresas reales** — Panadería, Artesanías, Tech Solutions, Evaluador y Admin con foto local
- **Posts con imagen** — Los 6 posts del muro muestran foto real
- **Eventos con imagen** — Los 4 eventos muestran foto real
- Los productos priorizan `image_url` (estáticas) sobre ImageField para máxima confiabilidad

### 2026-08-11 — Hackathon: PWA y actividad en vivo
- **Ticker "EN VIVO"** — Barra bajo el navbar para usuarios logueados que rota las últimas publicaciones/productos/eventos cada 4.5s; endpoint JSON ligero `/api/activity-ticker/` consultado cada 15s

### 2026-08-10 — Sitio más vivo: animaciones y micro-interacciones
- **Fondo ambiental** — Orbes verdes flotantes animados en todo el sitio (sutiles en modo claro)
- **Fade-in escalonado** — Las tarjetas aparecen en cascada al hacer scroll
- **Marketplace vivo** — Tarjetas con tilt 3D al pasar el mouse, brillo (shine) que barre la imagen, y precio con pulso sutil
- **Contadores animados** — Las stats del landing cuentan de 0 al valor al entrar en pantalla
- **Navbar con micro-interacciones** — Iconos que suben y crecen al hover; scroll suave en toda la página
- **Logout** — Tras cerrar sesión redirige a `/login/` en lugar de la portada

### 2026-08-10 — Deploy estable en Render + identidad visual
- **Build estable en Render** — `SECRET_KEY` con valor por defecto + versiones fijadas de paquetes `google-*` en `requirements.txt` (sin backtracking de pip); eliminado el servicio duplicado roto `korva-nicaragua-2.0`
- **Fix error 500 en Alianzas (`/recommendations/`)** — El superusuario `admin` se creaba sin perfil; ahora `build.sh` crea su perfil y la vista redirige amablemente si faltara
- **Fix "User has no profile" en Mensajes** — Mismo origen (perfil de admin faltante), resuelto en el build
- **Fix "Profile has no ai_config"** — `KorvaAIConfig` se crea automáticamente para todo perfil (signal `post_save`)
- **Servir estáticos y media en producción** — Vista propia con `FileResponse` en `urls.py` (Django solo sirve estáticos con DEBUG=True)
- **Logos reales de empresas** — Nuevo campo `logo_url` en `Profile` (migración `0005`) con fotos Unsplash para las empresas demo; se muestran en Alianzas, Marketplace, y perfiles
- **Logo Korva** — Imagen del cliente en navbar, landing (hero) y login (en grande)
- **Perfil sin placeholder** — El perfil del admin ya no muestra el avatar genérico de edificio

### 2026-08-10 — Forest Tech: Rediseño visual + animaciones
- **Tema Forest Tech aplicado al sitio completo** — Paleta oscura forestal (`#0c1012` fondo, `#15191c` tarjetas, `#167208` primario, `#7ddf55` acentos/lima)
- **Tipografía profesional** — Montserrat para títulos (h1–h5), Inter para cuerpo
- **Iconografía** — Material Symbols Outlined en toda la interfaz
- **Marketplace rediseñado** — Tarjetas con imagen, logo del vendedor, precio en lima, grid responsive 1/2/3 columnas, búsqueda y filtros en fila en desktop
- **Landing page rediseñada** — Hero con gradiente, icono animado, gradiente de texto, stats y features con nuevo estilo
- **Animaciones en todo el sitio** — Tarjetas con reveal al hacer scroll (IntersectionObserver), títulos con fade-up, delay escalonado
- **Hover profesional** — Tarjetas se elevan con glow verde, imágenes del marketplace con zoom, botones con glow
- **Navbar glass** — Efecto glassmorphism (blur) + logo con gradiente lima→verde
- **Fondo ambiental** — Glow radial verde sutil en todo el sitio
- **Responsive total** — Marketplace y landing adaptados a móvil y desktop

### 2026-07-29
- **Menú móvil limpio** — Drawer con avatar, nombre de negocio, secciones (Navegación / Mi Cuenta / Seguridad)
- **Simplificación Gemini** — Eliminado `system_instruction` (incompatible con SDK 0.8.6), instrucciones en el mensaje directo
- **Error amigable IA** — Mensaje claro cuando se envían imágenes al chat de texto
- **Registro estable** — `create_user()` → `authenticate()` → `login()` (no crashea)
- **Responsive móvil** — 9 plantillas corregidas para pantallas chicas
- **CSS `bg-korva-dark-alt`** — Definido el color que faltaba
- **Filtro sector Muro** — Dropdown para filtrar publicaciones por categoría
- **Preservar contraseñas** — `load_test_data.py` no resetea passwords de usuarios existentes
- **Login redirect** — `LOGIN_URL = '/login/'` + backend hardcode eliminado
- **Botones sociales ocultos** — No se muestran si no hay credenciales API configuradas
- **Imágenes Unsplash** — Todos los productos de prueba tienen imágenes reales
- **Datos de prueba completos** — Productos, conversaciones, reseñas, eventos, grupos
