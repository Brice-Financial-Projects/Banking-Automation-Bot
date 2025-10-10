"""
URL configuration for config project.

config/urls.py
"""

from django.urls import path

from finance import views as finance_views

urlpatterns = [
    path("api/plaid/create-link-token/", finance_views.create_link_token),
    path("api/plaid/exchange-token/", finance_views.exchange_public_token),
    path("api/plaid/accounts/", finance_views.get_accounts),
]
