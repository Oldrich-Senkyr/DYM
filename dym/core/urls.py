from django.urls import path
from .views import index, switch_language

from django.contrib.auth import views as auth_views #login  importuje views z danga
#from .forms import LoginForm                        #login

app_name = 'core'

urlpatterns = [
    path('', index, name='index'),
    path('switch_language/<str:language_code>/', switch_language, name='switch_language'),
    ]