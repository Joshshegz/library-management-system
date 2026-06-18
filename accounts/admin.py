from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ("matric_no",)
    list_display = (
        "matric_no",
        "email",
        "first_name",
        "last_name",
        "role",
        "biometric_enrolled",
        "is_staff",
    )
    list_filter = ("role", "biometric_enrolled", "is_staff", "department")
    search_fields = ("matric_no", "first_name", "last_name", "email")

    fieldsets = (
        (None, {"fields": ("matric_no", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "email", "department", "phone")},
        ),
        (
            "Library access",
            {"fields": ("role", "biometric_enrolled")},
        ),
        (
            "Permissions",
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "matric_no",
                    "first_name",
                    "last_name",
                    "email",
                    "role",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
