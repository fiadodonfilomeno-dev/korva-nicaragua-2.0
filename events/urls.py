from django.urls import path
from . import views

urlpatterns = [
    path('', views.events_list, name='events_list'),
    path('create/', views.create_event, name='create_event'),
    path('<int:event_id>/', views.event_detail, name='event_detail'),
    path('<int:event_id>/attend/', views.toggle_attend, name='toggle_attend'),
]
