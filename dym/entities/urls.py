from django.urls import path
from .views import entity_create_view, EntityListView, EntityEditView, EntityDeleteView

app_name = 'entities'


urlpatterns = [
    path("entity/new/", entity_create_view, name="entity_create"),
    path("entity/list/", EntityListView.as_view(), name="entity_list"),
    path("entity/edit/<int:pk>/", EntityEditView.as_view(), name="entity_edit"),
    path("entity/delete/<int:pk>/", EntityDeleteView.as_view(), name="entity_delete"),
]
