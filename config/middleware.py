from django.conf import settings
from django.shortcuts import redirect


class LocalhostWebAuthnMiddleware:
    """
    WebAuthn / Windows Hello does not accept 127.0.0.1 as rpId on many setups.
    In DEBUG, redirect to localhost so fingerprint/face registration works.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.DEBUG:
            host = request.get_host().split(":")[0]
            if host == "127.0.0.1":
                new_url = request.build_absolute_uri().replace(
                    "127.0.0.1", "localhost", 1
                )
                return redirect(new_url)
        return self.get_response(request)
