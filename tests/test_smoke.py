"""tests/test_smoke.py"""

import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_register_and_login():
    client = APIClient()

    strong_password = "Secur3!Passw0rd"

    resp = client.post(
        "/api/auth/register/",
        {
            "email": "user@test.com",
            "username": "user",
            "password": strong_password,
            "password_confirm": strong_password,
        },
        format="json"
    )

    print("REGISTER RESPONSE:", resp.status_code, resp.json())
    assert resp.status_code == 201
