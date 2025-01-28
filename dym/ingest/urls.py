from django.urls import path
from . import views

urlpatterns = [
    path('read/', views.ingest_data, name='read_data'),
    path('export/', views.export_data, name='export_data'),
]
