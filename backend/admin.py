"""
Admin configuration for backend app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom admin interface for User model."""

    list_display = ['email', 'username', 'first_name', 'last_name', 'is_staff', 'email_verified', 'created_at']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'email_verified', 'two_factor_enabled']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-created_at']

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Security', {'fields': ('email_verified', 'two_factor_enabled')}),
        ('Plaid Integration', {'fields': ('plaid_item_id', 'last_plaid_sync')}),
        ('Preferences', {'fields': ('timezone', 'notification_preferences')}),
        ('Important Dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )

    readonly_fields = ['created_at', 'updated_at', 'last_login']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
