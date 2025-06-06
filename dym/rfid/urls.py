from django.urls import path
from . import views

app_name = 'rfid'


urlpatterns = [
    path('list/', views.card_list, name='card_list'),
    path('create/', views.card_create, name='card_create'),
    path('<int:card_id>/assign/', views.card_permission_assign, name='card_permission_assign'),
    path('<int:pk>/edit/', views.card_update, name='card_update'),
    path('<int:pk>/delete/', views.card_delete, name='card_delete'),
    path("<int:card_id>/remove_permission/<int:permission_id>/", views.remove_permission, name="remove_permission"),
    ]