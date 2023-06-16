from django.urls import path, include

from rest_framework import routers

from .views import ProfileViewSet, VisitLogViewSet


app_name = 'accounts'

router = routers.DefaultRouter()
router.register(r'profile', ProfileViewSet, basename='profile')
router.register(r'visit', VisitLogViewSet, basename='visit')

urlpatterns = [
    path('auth/', include('djoser.urls.base'), name='base'),
    path('auth/', include('djoser.urls.jwt'), name='jwt'),
    path('auth/', include('djoser.social.urls'), name='social'),
    path('', include(router.urls), name='routes'),
]
