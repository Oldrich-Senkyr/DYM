from django.urls import path
from entrix import views

app_name = 'entrix'


urlpatterns = [
    path("persons/", views.persons_list, name="persons_list"),
    path('persons/<int:pk>/edit/', views.edit_person, name='person_edit'),
    path('persons/<int:pk>/delete/', views.delete_person, name='person_delete'),
]