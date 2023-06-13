from django.urls import path, include

from rest_framework import routers

from .views import ProfileViewSet


app_name = 'accounts'

router = routers.DefaultRouter()
router.register(r'', ProfileViewSet, basename='profile')

urlpatterns = [
    path('auth/', include('djoser.urls.base'), name='base'),
    path('auth/', include('djoser.urls.jwt'), name='jwt'),
    path('auth/', include('djoser.social.urls'), name='social'),
    path('profile/', include(router.urls), name='profile'),
]
