from django.urls import path
from . import views

urlpatterns = [
    path('ws-config/', views.ws_config, name='ws_config'),
    path('notifications/unread/', views.notifications_unread, name='api_notifications_unread'),
    path('messages/unread/', views.messages_unread, name='api_messages_unread'),
]
