from django.urls import path
from . import views

app_name = 'ingest'

urlpatterns = [
    path('read/', views.ingest_data, name='read_data'),
    path('export/', views.export_data, name='export_data'),
    path('delete/<int:pk>/', views.delete_data, name='delete_data'),
]
