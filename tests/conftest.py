"""tests/conftest.py"""

import pytest
from django.contrib.auth import get_user_model

@pytest.fixture
def user_factory():
    """
    Factory fixture to create test users easily.
    """
    def create_user(**kwargs):
        User = get_user_model()
        defaults = {
            "email": "testuser@example.com",
            "username": "testuser",  
            "password": "Secur3!Passw0rd",
        }
        defaults.update(kwargs)
        user = User.objects.create_user(**defaults)
        return user

    return create_user
