"""
URL configuration for dym project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings

urlpatterns = [
    # Cesty mimo i18n_patterns, např. pro přepínání jazyka
    path('i18n/', include('django.conf.urls.i18n')),  # pro přepínač jazyků
]

# Cesty s podporou pro více jazyků
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('agent/', include('agent.urls')),
    path('entities/', include('entities.urls')),
    path('ingest/', include('ingest.urls')),
    path('entrix/', include('entrix.urls')),
  
    # Add other language-specific URLs here as needed
)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
