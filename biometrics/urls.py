from django.urls import path

from . import webauthn_views as views

app_name = "biometrics"

urlpatterns = [
    path("enroll/", views.enroll, name="enroll"),
    path("enroll/nose/", views.enroll_nose, name="enroll_nose"),
    path("login/", views.biometric_login, name="login"),
    path("verify/", views.verify_self, name="verify"),
    path(
        "webauthn/register/options/",
        views.register_options,
        name="webauthn_register_options",
    ),
    path(
        "webauthn/register/complete/",
        views.register_complete,
        name="webauthn_register_complete",
    ),
    path("webauthn/auth/options/", views.auth_options, name="webauthn_auth_options"),
    path(
        "webauthn/verify/options/",
        views.verify_options,
        name="webauthn_verify_options",
    ),
    path("webauthn/auth/complete/", views.auth_complete, name="webauthn_auth_complete"),
]
