import base64

from django.conf import settings
from django.http import HttpRequest
from webauthn.helpers.options_to_json_dict import options_to_json_dict


def rp_id(request: HttpRequest) -> str:
    """Must match the hostname in the browser URL (localhost ≠ 127.0.0.1)."""
    override = getattr(settings, "WEBAUTHN_RP_ID", None)
    if override:
        return override
    return request.get_host().split(":")[0]


def origin(request: HttpRequest) -> str:
    override = getattr(settings, "WEBAUTHN_ORIGIN", None)
    if override:
        return override.rstrip("/")
    return f"{request.scheme}://{request.get_host()}".rstrip("/")


def rp_name() -> str:
    return getattr(settings, "WEBAUTHN_RP_NAME", "LAUTECH Library")


def user_id_bytes(user) -> bytes:
    return int(user.pk).to_bytes(8, byteorder="big")


def b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def options_for_browser(options) -> dict:
    """Convert WebAuthn options to a JSON-serializable dict for the browser."""
    return options_to_json_dict(options)
