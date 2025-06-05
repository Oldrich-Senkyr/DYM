from django.urls import path
from . import views

app_name = 'rfid'




urlpatterns = [
    path('rfid/', views.card_list, name='card_list'),
    path('rfid/create/', views.card_create, name='card_create'),
    path('rfid/<int:card_id>/assign/', views.card_permission_assign, name='card_permission_assign'),
]
