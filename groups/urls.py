from django.urls import path
from . import views

urlpatterns = [
    path('', views.groups_list, name='groups_list'),
    path('create/', views.create_group, name='create_group'),
    path('<int:group_id>/', views.group_detail, name='group_detail'),
    path('<int:group_id>/join/', views.toggle_group_member, name='toggle_group_member'),
]
