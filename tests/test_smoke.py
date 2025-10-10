"""tests/test_smoke.py"""

import pytest

# tests/test_smoke.py
@pytest.mark.django_db
def test_register_and_login(client):
    # register
    resp = client.post(
        "/api/auth/register/",
        {
            "email": "user@test.com",
            "password": "pass1234",
            "password2": "pass1234",   # required
            "username": "user",         # required by AbstractUser
        },
        content_type="application/json",
    )
    assert resp.status_code == 201
