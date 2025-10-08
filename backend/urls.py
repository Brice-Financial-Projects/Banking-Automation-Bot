"""
URL configuration for backend authentication endpoints.
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'backend'

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', views.register_view, name='register'),
    path('auth/login/', views.CustomTokenObtainPairView.as_view(), name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # User profile endpoints
    path('auth/me/', views.current_user_view, name='current_user'),
    path('auth/me/update/', views.update_user_view, name='update_user'),
    path('auth/password/change/', views.change_password_view, name='change_password'),
]
