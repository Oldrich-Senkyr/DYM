from django.urls import path
from django.contrib.auth import views as auth_views #login  importuje views z danga
from agent.forms import LoginForm
from agent.views import logout_view, signup

app_name = 'agent'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='agent/login.html',authentication_form=LoginForm), name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup, name='signup'),
    ]
