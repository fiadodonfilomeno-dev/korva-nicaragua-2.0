"""
URL configuration for korva_config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


# Vistas de usuarios
from users.views import register, login_view, logout_view, profile_view, edit_profile, dashboard, verify_email, pymes_map
from users.report_views import report_user, block_user, unblock_user, blocked_users_list

# Vistas de muro social
from social.views import (
    home, create_post, post_detail, upvote_post, downvote_post,
    edit_post, delete_post, check_new_posts, toggle_favorite_post
)

# Vistas de marketplace
from marketplace.views import (
    marketplace, create_product, product_detail, edit_product,
    delete_product, my_products, toggle_favorite_product, my_favorites,
    add_review, seller_reviews, deals_list, create_deal, export_catalog_pdf,
    buy_product, my_purchases, my_sales, transaction_detail,
    confirm_payment, confirm_receipt, complete_transaction, cancel_transaction,
    seller_wallet, bank_account_view, request_payout, download_receipt,
)

# Vistas de rankings
from core.rankings_views import rankings

# Vistas de recomendaciones
from core.views import recommendations, search, activity_feed

# Vistas de mensajería
from messaging.views import (
    messages_view, conversation_detail, start_conversation, send_message
)

# Vistas de reportes
from reports.views import reports_view, export_csv, export_pdf, analytics_view

# Vistas de IA
from core.ai_views import (
    korva_ai, ai_tutorial, create_conversation, conversation_chat, send_ai_message,
    update_ai_config, quick_prompts
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    
    # Autenticación
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('verify-email/<uuid:token>/', verify_email, name='verify_email'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/<str:username>/', profile_view, name='profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('map/', pymes_map, name='pymes_map'),
    path('report/<str:username>/', report_user, name='report_user'),
    path('block/<str:username>/', block_user, name='block_user'),
    path('unblock/<str:username>/', unblock_user, name='unblock_user'),
    path('blocked-users/', blocked_users_list, name='blocked_users_list'),
    
    # Muro Social
    path('', home, name='home'),
    path('post/create/', create_post, name='create_post'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('post/<int:post_id>/upvote/', upvote_post, name='upvote_post'),
    path('post/<int:post_id>/downvote/', downvote_post, name='downvote_post'),
    path('post/<int:post_id>/edit/', edit_post, name='edit_post'),
    path('post/<int:post_id>/delete/', delete_post, name='delete_post'),
    path('api/check-new-posts/', check_new_posts, name='check_new_posts'),
    path('post/<int:post_id>/favorite/', toggle_favorite_post, name='toggle_favorite_post'),
    
    # Marketplace
    path('marketplace/', marketplace, name='marketplace'),
    path('product/create/', create_product, name='create_product'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('product/<int:product_id>/edit/', edit_product, name='edit_product'),
    path('product/<int:product_id>/delete/', delete_product, name='delete_product'),
    path('my-products/', my_products, name='my_products'),
    path('product/<int:product_id>/favorite/', toggle_favorite_product, name='toggle_favorite_product'),
    path('my-favorites/', my_favorites, name='my_favorites'),
    path('review/<str:username>/', add_review, name='add_review'),
    path('reviews/<str:username>/', seller_reviews, name='seller_reviews'),
    path('deals/', deals_list, name='deals_list'),
    path('product/<int:product_id>/deal/', create_deal, name='create_deal'),
    path('export-catalog/', export_catalog_pdf, name='export_catalog_pdf'),
    
    # Pagos y Comisiones
    path('product/<int:product_id>/buy/', buy_product, name='buy_product'),
    path('my-purchases/', my_purchases, name='my_purchases'),
    path('my-sales/', my_sales, name='my_sales'),
    path('transaction/<int:transaction_id>/', transaction_detail, name='transaction_detail'),
    path('transaction/<int:transaction_id>/confirm-payment/', confirm_payment, name='confirm_payment'),
    path('transaction/<int:transaction_id>/confirm-receipt/', confirm_receipt, name='confirm_receipt'),
    path('transaction/<int:transaction_id>/complete/', complete_transaction, name='complete_transaction'),
    path('transaction/<int:transaction_id>/cancel/', cancel_transaction, name='cancel_transaction'),
    path('seller-wallet/', seller_wallet, name='seller_wallet'),
    path('bank-account/', bank_account_view, name='bank_account'),
    path('request-payout/', request_payout, name='request_payout'),
    path('transaction/<int:transaction_id>/receipt/', download_receipt, name='download_receipt'),
    
    # Rankings
    path('rankings/', rankings, name='rankings'),
    
    # Alianzas Recomendadas
    path('recommendations/', recommendations, name='recommendations'),
    
    # Busqueda Avanzada
    path('search/', search, name='search'),
    path('activity/', activity_feed, name='activity_feed'),
    
    # Mensajería
    path('messages/', messages_view, name='messages'),
    path('conversation/<int:conversation_id>/', conversation_detail, name='conversation_detail'),
    path('start-conversation/<str:username>/', start_conversation, name='start_conversation'),
    path('send-message/', send_message, name='send_message'),
    
    # Reportes
    path('reports/', reports_view, name='reports'),
    path('reports/export-csv/', export_csv, name='export_csv'),
    path('reports/export-pdf/', export_pdf, name='export_pdf'),
    path('analytics/', analytics_view, name='analytics'),
    
    # IA
    path('ai/', korva_ai, name='korva_ai'),
    path('ai/tutorial/', ai_tutorial, name='ai_tutorial'),
    path('ai/new/', create_conversation, name='create_ai_conversation'),
    path('ai/conversation/<int:conversation_id>/', conversation_chat, name='conversation_chat'),
    path('ai/conversation/<int:conversation_id>/send/', send_ai_message, name='send_ai_message'),
    path('ai/config/', update_ai_config, name='update_ai_config'),
    path('ai/quick-prompts/', quick_prompts, name='quick_prompts'),
    
    # Eventos
    path('events/', include('events.urls')),
    
    # Grupos
    path('groups/', include('groups.urls')),
    
    # Notificaciones
    path('notifications/', include('notifications.urls')),

    # API REST
    path('api/', include('api.urls')),

    # Cambio de idioma
    path('i18n/', include('django.conf.urls.i18n')),
]

# Servir archivos de media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

