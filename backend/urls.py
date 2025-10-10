"""
URL configuration for backend authentication endpoints.
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'backend'

urlpatterns = [
    # Authentication endpoints
    path('register/', views.register_view, name='register'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # User profile endpoints
    path('me/', views.current_user_view, name='current_user'),
    path('me/update/', views.update_user_view, name='update_user'),
    path('password/change/', views.change_password_view, name='change_password'),
]
