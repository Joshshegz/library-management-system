import json

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from accounts.models import User
from webauthn import (
    generate_authentication_options,
    generate_registration_options,
    verify_authentication_response,
    verify_registration_response,
)
from webauthn.helpers.parse_authentication_credential_json import (
    parse_authentication_credential_json,
)
from webauthn.helpers.parse_registration_credential_json import (
    parse_registration_credential_json,
)
from webauthn.helpers.structs import (
    AuthenticatorAttachment,
    AuthenticatorSelectionCriteria,
    PublicKeyCredentialDescriptor,
    UserVerificationRequirement,
)

from .enrollment import has_nose_template, has_windows_hello, is_fully_enrolled, sync_enrolled_flag
from .models import BiometricTemplate, WebAuthnCredential
from .services import NoseExtractionError
from .services.liveness import LivenessError
from .utils import extract_biometrics_from_request
from .webauthn_helpers import (
    b64url_decode,
    b64url_encode,
    options_for_browser,
    origin,
    rp_id,
    rp_name,
    user_id_bytes,
)


@login_required
@require_GET
def register_options(request):
    user = request.user
    exclude = [
        PublicKeyCredentialDescriptor(id=cred.credential_id_bytes)
        for cred in user.webauthn_credentials.all()
    ]

    options = generate_registration_options(
        rp_id=rp_id(request),
        rp_name=rp_name(),
        user_id=user_id_bytes(user),
        user_name=user.matric_no,
        user_display_name=user.get_full_name() or user.matric_no,
        authenticator_selection=AuthenticatorSelectionCriteria(
            authenticator_attachment=AuthenticatorAttachment.PLATFORM,
            user_verification=UserVerificationRequirement.REQUIRED,
        ),
        exclude_credentials=exclude or None,
    )

    request.session["webauthn_challenge"] = b64url_encode(options.challenge)
    request.session["webauthn_user_pk"] = user.pk

    return JsonResponse(options_for_browser(options))


@login_required
@require_POST
def register_complete(request):
    try:
        body = json.loads(request.body.decode())
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    challenge = request.session.pop("webauthn_challenge", None)
    session_user_pk = request.session.pop("webauthn_user_pk", None)
    if not challenge or session_user_pk != request.user.pk:
        return JsonResponse({"error": "Registration session expired. Try again."}, status=400)

    credential = parse_registration_credential_json(json.dumps(body))
    verification = verify_registration_response(
        credential=credential,
        expected_challenge=b64url_decode(challenge),
        expected_rp_id=rp_id(request),
        expected_origin=origin(request),
        require_user_verification=True,
    )

    cred_id = b64url_encode(verification.credential_id)
    public_key = b64url_encode(verification.credential_public_key)

    WebAuthnCredential.objects.update_or_create(
        credential_id=cred_id,
        defaults={
            "user": request.user,
            "public_key": public_key,
            "sign_count": verification.sign_count,
            "transports": body.get("transports") or [],
            "device_label": "Windows Hello",
        },
    )
    sync_enrolled_flag(request.user)

    return JsonResponse({
        "ok": True,
        "message": "Step 1 complete. Now capture your nose (Step 2).",
        "step": 2,
    })


@require_GET
def auth_options(request):
    matric = request.GET.get("matric_no", "").strip().upper()
    if not matric:
        return JsonResponse({"error": "matric_no required"}, status=400)

    try:
        user = User.objects.get(matric_no=matric)
    except User.DoesNotExist:
        return JsonResponse({"error": "Unknown matric number."}, status=404)

    credentials = list(user.webauthn_credentials.all())
    if not credentials:
        return JsonResponse(
            {"error": "Windows Hello not set up for this account. Enroll first."},
            status=400,
        )

    allow = [
        PublicKeyCredentialDescriptor(id=c.credential_id_bytes, transports=c.transports)
        for c in credentials
    ]

    options = generate_authentication_options(
        rp_id=rp_id(request),
        allow_credentials=allow,
        user_verification=UserVerificationRequirement.REQUIRED,
    )

    request.session["webauthn_challenge"] = b64url_encode(options.challenge)
    request.session["webauthn_auth_matric"] = matric

    return JsonResponse(options_for_browser(options))


@require_POST
def auth_complete(request):
    try:
        body = json.loads(request.body.decode())
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    challenge = request.session.pop("webauthn_challenge", None)
    matric = request.session.pop("webauthn_auth_matric", None)
    if not challenge or not matric:
        return JsonResponse({"error": "Login session expired. Try again."}, status=400)

    try:
        user = User.objects.get(matric_no=matric)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    credential = parse_authentication_credential_json(json.dumps(body))
    cred_id = b64url_encode(credential.raw_id)
    stored = get_object_or_404(WebAuthnCredential, credential_id=cred_id, user=user)

    verification = verify_authentication_response(
        credential=credential,
        expected_challenge=b64url_decode(challenge),
        expected_rp_id=rp_id(request),
        expected_origin=origin(request),
        credential_public_key=b64url_decode(stored.public_key),
        credential_current_sign_count=stored.sign_count,
        require_user_verification=True,
    )

    stored.sign_count = verification.new_sign_count
    stored.save(update_fields=["sign_count"])

    login(request, user, backend="django.contrib.auth.backends.ModelBackend")
    sync_enrolled_flag(user)

    return JsonResponse({"ok": True, "redirect": "/accounts/dashboard/"})


@login_required
@require_http_methods(["GET"])
def enroll(request):
    hello_done = has_windows_hello(request.user)
    nose_done = has_nose_template(request.user)
    fully = is_fully_enrolled(request.user)

    if hello_done and not nose_done:
        messages.info(
            request,
            "Step 1 is done. Complete Step 2: capture your nose below.",
        )

    return render(
        request,
        "biometrics/enroll_hello.html",
        {
            "nav_active": "profile",
            "hello_done": hello_done,
            "nose_done": nose_done,
            "fully_enrolled": fully,
            "show_step2": hello_done and not nose_done and not fully,
            "show_step1": not hello_done and not fully,
        },
    )


@login_required
@require_POST
def enroll_nose(request):
    """Step 2: save nose landmarks from webcam capture."""
    if not has_windows_hello(request.user):
        messages.error(request, "Complete Step 1 (Windows Hello) first.")
        return redirect("biometrics:enroll")

    try:
        face_features, nose_features = extract_biometrics_from_request(request)
    except (ValueError, LivenessError, NoseExtractionError) as exc:
        messages.error(request, str(exc))
        return redirect("biometrics:enroll#step-nose")

    BiometricTemplate.objects.update_or_create(
        user=request.user,
        defaults={
            "face_features": face_features,
            "nose_features": nose_features,
            "thumb_features": [],
        },
    )
    sync_enrolled_flag(request.user)
    messages.success(
        request,
        "Enrollment complete — Windows Hello, face profile, and nose landmarks saved.",
    )
    return redirect("accounts:dashboard")


@require_http_methods(["GET"])
def biometric_login(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")
    return render(request, "biometrics/login_hello.html")


@login_required
@require_GET
def verify_options(request):
    """Auth options for the currently logged-in user (test verification page)."""
    user = request.user
    credentials = list(user.webauthn_credentials.all())
    if not credentials:
        return JsonResponse(
            {"error": "Windows Hello not set up yet. Go to Enroll first."},
            status=400,
        )

    allow = [
        PublicKeyCredentialDescriptor(id=c.credential_id_bytes, transports=c.transports)
        for c in credentials
    ]

    options = generate_authentication_options(
        rp_id=rp_id(request),
        allow_credentials=allow,
        user_verification=UserVerificationRequirement.REQUIRED,
    )

    request.session["webauthn_challenge"] = b64url_encode(options.challenge)
    request.session["webauthn_auth_matric"] = user.matric_no

    return JsonResponse(options_for_browser(options))


@login_required
@require_http_methods(["GET", "POST"])
def verify_self(request):
    verify_result = None
    if request.method == "POST":
        from .verification import NoseVerificationError, verify_user_nose

        try:
            match = verify_user_nose(request.user, request)
            verify_result = {
                "ok": True,
                "message": f"Liveness passed. Nose match OK (distance {match.nose_distance:.2f}).",
            }
            messages.success(request, verify_result["message"])
        except NoseVerificationError as exc:
            verify_result = {"ok": False, "message": str(exc)}
            messages.error(request, str(exc))

    return render(
        request,
        "biometrics/verify_hello.html",
        {
            "nav_active": "profile",
            "hello_done": has_windows_hello(request.user),
            "nose_done": has_nose_template(request.user),
            "fully_enrolled": is_fully_enrolled(request.user),
            "verify_result": verify_result,
            "verify_id": f"LAU-BM-{request.user.matric_no[-5:]}",
        },
    )
