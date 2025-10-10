"""
Tests for Plaid mock endpoints
tests/test_plaid_mock.py
"""

import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_plaid_mock_endpoints(user_factory):
    client = APIClient()
    user = user_factory()
    client.force_authenticate(user=user)

    # 1. Create link token
    res = client.post("/api/plaid/create-link-token/")
    assert res.status_code == 200
    assert "link_token" in res.data

    # 2. Exchange public token
    res = client.post("/api/plaid/exchange-token/", {"public_token": "test123"})
    assert res.status_code == 200
    assert "access_token" in res.data

    # 3. Get mock accounts
    res = client.get("/api/plaid/accounts/")
    assert res.status_code == 200
    assert "accounts" in res.data
