import base64

from django.conf import settings
from django.db import models


class BiometricTemplate(models.Model):
    """Legacy nose + thumb vectors (thesis pipeline). Optional if using Windows Hello only."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="biometric_template",
    )
    face_features = models.JSONField(
        default=list,
        blank=True,
        help_text="MediaPipe face-shape landmark vector (checked before nose)",
    )
    nose_features = models.JSONField(
        default=list,
        blank=True,
        help_text="MediaPipe nasal landmark vector",
    )
    thumb_features = models.JSONField(
        default=list,
        blank=True,
        help_text="Optional ICA thumbprint vector (Windows Hello handles fingerprint)",
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "biometric template"

    def __str__(self):
        return f"Biometrics — {self.user.matric_no}"


class WebAuthnCredential(models.Model):
    """Windows Hello / platform passkey (WebAuthn — no raw biometric images)."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="webauthn_credentials",
    )
    credential_id = models.TextField(unique=True)
    public_key = models.TextField()
    sign_count = models.PositiveIntegerField(default=0)
    transports = models.JSONField(default=list, blank=True)
    device_label = models.CharField(max_length=120, default="Windows Hello")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.matric_no} — {self.device_label}"

    @property
    def credential_id_bytes(self) -> bytes:
        return base64.urlsafe_b64decode(self.credential_id + "==")
