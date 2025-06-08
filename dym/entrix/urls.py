from django.urls import path
from entrix import views

app_name = 'entrix'


urlpatterns = [
    path("persons/", views.persons_list, name="persons_list"),
    path('persons/<int:pk>/edit/', views.person_edit, name='person_edit'),
    path('persons/<int:pk>/delete/', views.person_delete, name='person_delete'),
    path('persons/export/', views.person_export_csv, name='person_export_csv'),
    path('persons/import/', views.person_import_csv, name='person_import_csv'),
    path("persons/add/", views.person_add, name="person_add"),
    path("persons/presence", views.persons_presence, name="persons_presence"),
]