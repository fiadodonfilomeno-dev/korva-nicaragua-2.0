"""
URL configuration for korva_config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Vistas de usuarios
from users.views import register, login_view, logout_view, profile_view, edit_profile, dashboard, verify_email

# Vistas de muro social
from social.views import (
    home, create_post, post_detail, upvote_post, downvote_post,
    edit_post, delete_post, check_new_posts
)

# Vistas de marketplace
from marketplace.views import (
    marketplace, create_product, product_detail, edit_product,
    delete_product, my_products
)

# Vistas de rankings
from core.rankings_views import rankings

# Vistas de recomendaciones
from core.views import recommendations

# Vistas de mensajería
from messaging.views import (
    messages_view, conversation_detail, start_conversation, send_message
)

# Vistas de reportes
from reports.views import reports_view, export_csv, export_pdf

# Vistas de IA
from core.ai_views import (
    korva_ai, ai_tutorial, create_conversation, conversation_chat, send_ai_message,
    update_ai_config, quick_prompts
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Autenticación
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('verify-email/<uuid:token>/', verify_email, name='verify_email'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/<str:username>/', profile_view, name='profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    
    # Muro Social
    path('', home, name='home'),
    path('post/create/', create_post, name='create_post'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('post/<int:post_id>/upvote/', upvote_post, name='upvote_post'),
    path('post/<int:post_id>/downvote/', downvote_post, name='downvote_post'),
    path('post/<int:post_id>/edit/', edit_post, name='edit_post'),
    path('post/<int:post_id>/delete/', delete_post, name='delete_post'),
    path('api/check-new-posts/', check_new_posts, name='check_new_posts'),
    
    # Marketplace
    path('marketplace/', marketplace, name='marketplace'),
    path('product/create/', create_product, name='create_product'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('product/<int:product_id>/edit/', edit_product, name='edit_product'),
    path('product/<int:product_id>/delete/', delete_product, name='delete_product'),
    path('my-products/', my_products, name='my_products'),
    
    # Rankings
    path('rankings/', rankings, name='rankings'),
    
    # Alianzas Recomendadas
    path('recommendations/', recommendations, name='recommendations'),
    
    # Mensajería
    path('messages/', messages_view, name='messages'),
    path('conversation/<int:conversation_id>/', conversation_detail, name='conversation_detail'),
    path('start-conversation/<str:username>/', start_conversation, name='start_conversation'),
    path('send-message/', send_message, name='send_message'),
    
    # Reportes
    path('reports/', reports_view, name='reports'),
    path('reports/export-csv/', export_csv, name='export_csv'),
    path('reports/export-pdf/', export_pdf, name='export_pdf'),
    
    # IA
    path('ai/', korva_ai, name='korva_ai'),
    path('ai/tutorial/', ai_tutorial, name='ai_tutorial'),
    path('ai/new/', create_conversation, name='create_ai_conversation'),
    path('ai/conversation/<int:conversation_id>/', conversation_chat, name='conversation_chat'),
    path('ai/conversation/<int:conversation_id>/send/', send_ai_message, name='send_ai_message'),
    path('ai/config/', update_ai_config, name='update_ai_config'),
    path('ai/quick-prompts/', quick_prompts, name='quick_prompts'),
]

# Servir archivos de media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

