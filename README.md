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
- PyME: `panaderia_nicaraguica` / `test1234`

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
