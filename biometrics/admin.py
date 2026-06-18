from django.contrib import admin

from .models import BiometricTemplate, WebAuthnCredential


@admin.register(BiometricTemplate)
class BiometricTemplateAdmin(admin.ModelAdmin):
    list_display = ("user", "enrolled_at", "updated_at")
    search_fields = ("user__matric_no",)


@admin.register(WebAuthnCredential)
class WebAuthnCredentialAdmin(admin.ModelAdmin):
    list_display = ("user", "device_label", "sign_count", "created_at")
    search_fields = ("user__matric_no", "credential_id")
    readonly_fields = ("credential_id", "public_key", "created_at")
