from django.urls import path
from entrix import views

app_name = 'entrix'


urlpatterns = [
    path("persons-list/", views.persons_list, name="persons_list"),
]