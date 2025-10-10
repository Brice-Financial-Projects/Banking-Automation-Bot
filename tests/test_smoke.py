"""tests/test_smoke.py"""

import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_register_and_login():
    client = APIClient()

    # register
    resp = client.post(
        "/api/auth/register/",
        {
            "email": "user@test.com",
            "username": "user",
            "password": "pass1234",
            "password_confirm": "pass1234",  # ✅ must match serializer
        },
        format="json"
    )

    print("REGISTER RESPONSE:", resp.status_code, resp.json())
    assert resp.status_code == 201
