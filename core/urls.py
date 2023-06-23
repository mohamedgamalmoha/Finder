"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView
from django.urls import path, re_path, include
from django.views.i18n import JavaScriptCatalog

from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView,
                                   SpectacularJSONAPIView)


urlpatterns = [
    # Admin page
    path('admin/', admin.site.urls),

    # Translation
    path('i18n/', include('django.conf.urls.i18n')),
    *i18n_patterns(
        path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog')
    ),

    # API Docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/json/', SpectacularJSONAPIView.as_view(), name='spec_json'),

    # Custom Apps
    path('api/', include('accounts.api.urls', namespace='accounts')),

    # Default Page
    # re_path(r'^.*', TemplateView.as_view(template_name='index.html'))
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
