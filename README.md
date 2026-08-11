# Korva Nicaragua 2.0

Plataforma de red social y marketplace para PyMEs de Nicaragua. Networking, marketplace, mensajería, eventos, IA y analytics.

**Demo en producción:** https://korva-nicaragua-2-0-1.onrender.com

---

## Resumen de la aplicacion

### Arquitectura
- **Backend:** Django 6.0.5 + Python 3.14
- **Base de datos:** SQLite (configurable a MySQL)
- **Frontend:** Tailwind CSS (CDN) + vanilla JavaScript
- **Deploy:** Render (auto-deploy desde GitHub)
- **11 apps Django** — 22 modelos

### Apps
| App | Funcion |
|-----|---------|
| `users` | Perfiles, autenticacion, verificacion email, bloqueos, reportes |
| `social` | Muro, posts, votos, comentarios, favoritos |
| `marketplace` | Productos, ofertas, reviews, transacciones, pagos, catalogo PDF |
| `messaging` | Chat privado con fotos/videos y doble check de lectura |
| `events` | Ferias y eventos empresariales |
| `groups` | Grupos por sector con posts internos |
| `core` | IA (Gemini), recomendaciones, busqueda, modelos globales |
| `reports` | Metricas Chart.js + exportacion CSV/PDF |
| `notifications` | Sistema de notificaciones |
| `api` | REST endpoints |

### Funcionalidades

**Muro Social**
- Publicaciones con imagenes, videos, galeria multiple
- Votos AJAX (upvote/downvote), comentarios, hashtags clickeables
- Favoritos, filtro por sector, tiempo relativo ("hace 5 min")
- Auto-refresh cada 30s

**Marketplace**
- Publicacion y busqueda de productos con imagenes reales locales
- Filtros por categoria (ventas/compras) + busqueda por texto
- Tarjetas con logo del vendedor, precio, animacion tilt 3D
- Ofertas/descuentos con % y fecha de expiracion
- Calificacion de vendedores (estrellas 1-5 + comentarios)
- Carrito, compras/ventas, banco, payouts
- Exportar catalogo PDF (ReportLab)

**Colaboracion**
- Alianzas recomendadas (algoritmo por ciudad/sector/tags/verificacion)
- Rankings con niveles Bronce/Plata/Oro/VIP y categorias (General/Novatos/Establecidas)
- Mensajeria privada (fotos, videos, doble check de lectura)
- Eventos/ferias (crear, listar, asistir)
- Grupos por sector con posts internos
- Mapa interactivo de PyMEs (Leaflet/OpenStreetMap)

**Korva IA**
- Asistente inteligente con Google Gemini API
- Chat con conversaciones persistentes + tutorial interactivo
- Configurable por usuario (tono, estilo, longitud)
- Quick prompts predefinidos

**Analytics**
- Dashboard con Chart.js (posts por mes, votos, vistas, upvotes vs downvotes)
- Exportacion de reportes en CSV y PDF
- Busqueda avanzada unificada (empresas, productos, posts, grupos)

### Diseno
- **Tema Forest Tech oscuro** — Paleta `#0c1012` fondo, `#15191c` tarjetas, `#167208` primario, `#7ddf55` acentos
- Toggle claro/oscuro (sol/luna en navbar)
- Tipografia Montserrat (titulos) + Inter (cuerpo)
- Iconografia Material Symbols Outlined + Font Awesome
- Animaciones: orbes flotantes, fade-in escalonado, tilt 3D, shine, precios pulsantes
- Navbar glassmorphism (blur)
- Responsive total (movil/desktop)

---

## Tecnologias

- Django 6.0.5 / Python 3.14
- SQLite (configurable a MySQL)
- Tailwind CSS (CDN) — Tema oscuro
- Google Gemini API
- Chart.js — Graficas de metricas
- Leaflet / OpenStreetMap — Mapa interactivo
- ReportLab — Generacion de PDFs

## Inicio rapido

```bash
pip install -r requirements.txt
python manage.py migrate
python load_test_data.py
python manage.py runserver
```

## Credenciales de prueba

| Usuario | Password | Rol |
|---------|----------|-----|
| `admin` | `admin123` | Administrador |
| `panaderia_nicaraguena` | `panaderianicaraguena` | PyME alimentos |
| `artesanias_esteli` | `artesaniasesteli` | PyME artesanias |
| `tech_solutions` | `techsolutions` | PyME tecnologia |
| `evaluador` | `evaluador` | Evaluador |

## Estructura del proyecto

```
korva_config/       - Configuracion Django (settings, urls)
core/               - Rankings, Korva IA, recomendaciones, busqueda
users/              - Perfiles, autenticacion, mapa PyMEs
social/             - Posts, comentarios, votos, favoritos
marketplace/        - Productos, ofertas, reviews, pagos, PDF
messaging/          - Mensajeria privada entre empresas
reports/            - Reportes CSV/PDF, metricas Chart.js
events/             - Eventos y ferias empresariales
groups/             - Grupos por sector
notifications/      - Sistema de notificaciones
api/                - REST endpoints
templates/          - Templates HTML (tema oscuro)
static/             - Archivos estaticos + imagenes reales (img/real/)
media/              - Subidas de usuarios
```

## Rutas principales

| Ruta | Descripcion |
|------|-------------|
| `/` | Muro social |
| `/marketplace/` | Marketplace de productos |
| `/recommendations/` | Alianzas recomendadas |
| `/analytics/` | Metricas de alcance (Chart.js) |
| `/search/` | Busqueda avanzada |
| `/deals/` | Ofertas activas |
| `/events/` | Eventos y ferias |
| `/groups/` | Grupos por sector |
| `/map/` | Mapa de PyMEs |
| `/rankings/` | Rankings de empresas |
| `/export-catalog/` | Exportar catalogo PDF |
| `/ai/` | Korva IA |
| `/reports/` | Reportes y analytics |

---

## Changelog

### 2026-08-11 — Fixes de renderizado y tema claro/oscuro
- **Imagenes del marketplace arregladas** — Cambiadas de `background-image` CSS a etiqueta `<img>` para que rendericen correctamente (antes salian negras)
- **Tema claro/oscuro funcional** — Toggle en el navbar para cambiar entre fondo blanco y oscuro
- **Service worker eliminado** — Removido el SW que servia paginas cacheadas en negro; la pagina siempre carga fresca
- **Animacion CSS nativa** — `.stagger-in` y `.reveal` usan `@keyframes` en vez de `opacity:0` inicial que ocultaba tarjetas si JS fallaba
- **Keep-alive con GitHub Actions** — Ping cada 5 min para evitar que Render Free duerma el sitio (cold start de 30-60s)

### 2026-08-11 — Imagenes reales locales
- **Fotos reales alojadas en el proyecto** (`static/img/real/`) — pan, tres leches, cafe, ceramica, hamacas, computacion, apps y eventos; sin dependencia de enlaces externos
- **Logos de empresas reales** — Panaderia, Artesanias, Tech Solutions, Evaluador y Admin con foto local
- **Posts con imagen** — Los 6 posts del muro muestran foto real
- **Eventos con imagen** — Los 4 eventos muestran foto real
- Los productos priorizan `image_url` (estaticas) sobre ImageField para maxima confiabilidad

### 2026-08-11 — Hackathon: actividad en vivo
- **Ticker "EN VIVO"** — Barra bajo el navbar para usuarios logueados que rota las ultimas publicaciones/productos/eventos cada 4.5s; endpoint JSON ligero `/api/activity-ticker/` consultado cada 15s

### 2026-08-10 — Sitio mas vivo: animaciones y micro-interacciones
- **Fondo ambiental** — Orbes verdes flotantes animados en todo el sitio (sutiles en modo claro)
- **Fade-in escalonado** — Las tarjetas aparecen en cascada al hacer scroll
- **Marketplace vivo** — Tarjetas con tilt 3D al pasar el mouse, brillo (shine) que barre la imagen, y precio con pulso sutil
- **Contadores animados** — Las stats del landing cuentan de 0 al valor al entrar en pantalla
- **Navbar con micro-interacciones** — Iconos que suben y crecen al hover; scroll suave en toda la pagina
- **Logout** — Tras cerrar sesion redirige a `/login/` en lugar de la portada

### 2026-08-10 — Deploy estable en Render + identidad visual
- **Build estable en Render** — `SECRET_KEY` con valor por defecto + versiones fijadas de paquetes `google-*` en `requirements.txt` (sin backtracking de pip); eliminado el servicio duplicado roto
- **Fix error 500 en Alianzas (`/recommendations/`)** — El superusuario `admin` se creaba sin perfil; ahora `build.sh` crea su perfil y la vista redirige amablemente si faltara
- **Fix "User has no profile" en Mensajes** — Mismo origen (perfil de admin faltante), resuelto en el build
- **Fix "Profile has no ai_config"** — `KorvaAIConfig` se crea automaticamente para todo perfil (signal `post_save`)
- **Servir estaticos y media en produccion** — Vista propia con `FileResponse` en `urls.py` (Django solo sirve estaticos con DEBUG=True)
- **Logos reales de empresas** — Nuevo campo `logo_url` en `Profile` (migracion `0005`) con fotos Unsplash para las empresas demo; se muestran en Alianzas, Marketplace, y perfiles
- **Logo Korva** — Imagen del cliente en navbar, landing (hero) y login (en grande)
- **Perfil sin placeholder** — El perfil del admin ya no muestra el avatar generico de edificio

### 2026-08-10 — Forest Tech: Rediseno visual + animaciones
- **Tema Forest Tech aplicado al sitio completo** — Paleta oscura forestal
- **Tipografia profesional** — Montserrat para titulos (h1–h5), Inter para cuerpo
- **Iconografia** — Material Symbols Outlined en toda la interfaz
- **Marketplace redisenado** — Tarjetas con imagen, logo del vendedor, precio en lima, grid responsive 1/2/3 columnas
- **Landing page redisenada** — Hero con gradiente, icono animado, stats y features
- **Animaciones en todo el sitio** — Tarjetas con reveal al hacer scroll, titulos con fade-up, delay escalonado
- **Hover profesional** — Tarjetas se elevan con glow verde, imagenes con zoom, botones con glow
- **Navbar glass** — Efecto glassmorphism (blur) + logo con gradiente lima→verde
- **Responsive total** — Marketplace y landing adaptados a movil y desktop

### 2026-07-29
- **Menu movil limpio** — Drawer con avatar, nombre de negocio, secciones
- **Simplificacion Gemini** — Eliminado `system_instruction` (incompatible con SDK), instrucciones en el mensaje directo
- **Error amigable IA** — Mensaje claro cuando se envian imagenes al chat de texto
- **Registro estable** — `create_user()` → `authenticate()` → `login()` (no crashea)
- **Responsive movil** — 9 plantillas corregidas para pantallas chicas
- **Filtro sector Muro** — Dropdown para filtrar publicaciones por categoria
- **Datos de prueba completos** — Productos, conversaciones, resenas, eventos, grupos
