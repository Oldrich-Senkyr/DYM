from django.urls import path
from .views import daily_summary

app_name = 'mock'


urlpatterns = [
    path('daily-summary/', daily_summary, name='daily_summary'),
]
