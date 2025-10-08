"""
Custom User model for banking automation application.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):
    """
    Custom user model for banking automation app.
    Uses email as the primary authentication field.
    """
    # Use UUID as primary key for better security
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Override email to make it required and unique
    email = models.EmailField(unique=True, blank=False)

    # Additional contact info
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    # Plaid-specific fields (will be encrypted in production)
    plaid_access_token = models.TextField(blank=True, null=True)
    plaid_item_id = models.CharField(max_length=255, blank=True, null=True)

    # Account management flags
    email_verified = models.BooleanField(default=False)
    two_factor_enabled = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_plaid_sync = models.DateTimeField(null=True, blank=True)

    # User preferences
    notification_preferences = models.JSONField(default=dict, blank=True)
    timezone = models.CharField(max_length=50, default='UTC')

    # Use email for login instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Required for createsuperuser command

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']

    def __str__(self):
        return self.email

    @property
    def has_plaid_connection(self):
        """Check if user has an active Plaid connection."""
        return bool(self.plaid_access_token and self.plaid_item_id)
