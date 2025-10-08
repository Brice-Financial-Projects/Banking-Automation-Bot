"""tests/test_smoke.py"""

import pytest

@pytest.mark.django_db
def test_register_and_login(client):
    # register
    resp = client.post("/api/auth/register/", {"email": "user@test.com", "password": "pass1234"})
    assert resp.status_code == 201

    # login
    resp = client.post("/api/auth/login/", {"email": "user@test.com", "password": "pass1234"})
    assert "access" in resp.json()
