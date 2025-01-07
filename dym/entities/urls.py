from django.urls import path
from .views import entity_create_view

app_name = 'entities'


urlpatterns = [
    path("entity/new/", entity_create_view, name="entity_create"),
]
