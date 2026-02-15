# users/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserProfileView,
    UserUpdateView,
    UserLogoutView
)

urlpatterns = [
    # Autenticación
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    # Perfil del usuario
    path('me/', UserProfileView.as_view(), name='user-profile'),
    path('me/update/', UserUpdateView.as_view(), name='user-update'),
]
