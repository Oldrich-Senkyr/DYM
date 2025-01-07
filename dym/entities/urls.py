from django.urls import path
from .views import entity_create

app_name = 'entities'


urlpatterns = [
    path("entity/new/", entity_create, name="entity_create"),
]
