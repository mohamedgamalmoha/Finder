from django.urls import path

from .views import ActivationView, ResetUsernameView, ResetPasswordView, SuccessView


urlpatterns = [
    path('activation/<str:uid>/<str:token>/', ActivationView.as_view()),
    path('reset-username/<str:uid>/<str:token>/', ResetUsernameView.as_view()),
    path('reset-password/<str:uid>/<str:token>/', ResetPasswordView.as_view()),
    path('success/', SuccessView.as_view(), name='success')
]
