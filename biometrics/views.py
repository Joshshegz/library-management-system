from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from accounts.models import User

from .models import BiometricTemplate
from .services import NoseExtractionError, ThumbExtractionError, verify_templates
from .services.matcher import verify_face_only
from .utils import extract_from_request


@login_required
@require_http_methods(["GET", "POST"])
def enroll(request):
    if request.method == "POST":
        try:
            nose_features, thumb_features, face_features = extract_from_request(request)
        except (ValueError, NoseExtractionError, ThumbExtractionError) as exc:
            messages.error(request, str(exc))
            return render(request, "biometrics/enroll.html")

        BiometricTemplate.objects.update_or_create(
            user=request.user,
            defaults={
                "face_features": face_features,
                "nose_features": nose_features,
                "thumb_features": thumb_features,
            },
        )
        request.user.biometric_enrolled = True
        request.user.save(update_fields=["biometric_enrolled"])

        messages.success(
            request,
            "Biometric enrollment complete. You can now use biometric login and borrow books.",
        )
        return redirect("accounts:dashboard")

    return render(request, "biometrics/enroll.html")


@require_http_methods(["GET", "POST"])
def biometric_login(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")

    if request.method == "POST":
        matric = request.POST.get("matric_no", "").strip().upper()
        if not matric:
            messages.error(request, "Enter your Staff/Student ID.")
            return render(request, "biometrics/login.html")

        try:
            user = User.objects.get(matric_no=matric)
            template = user.biometric_template
        except (User.DoesNotExist, BiometricTemplate.DoesNotExist):
            messages.error(request, "Unknown matric or biometrics not enrolled.")
            return render(request, "biometrics/login.html")

        try:
            nose_features, thumb_features, face_features = extract_from_request(request)
        except (ValueError, NoseExtractionError, ThumbExtractionError) as exc:
            messages.error(request, str(exc))
            return render(request, "biometrics/login.html", {"matric_no": matric})

        if template.face_features:
            face_result = verify_face_only(face_features, template.face_features)
            if not face_result.accepted:
                messages.error(
                    request,
                    "Face does not match the enrolled profile.",
                )
                return render(request, "biometrics/login.html", {"matric_no": matric})

        result = verify_templates(
            nose_features,
            thumb_features,
            template.nose_features,
            template.thumb_features,
        )

        if result.accepted:
            login(
                request,
                user,
                backend="django.contrib.auth.backends.ModelBackend",
            )
            messages.success(
                request,
                f"Biometric verification successful ({result.elapsed_ms:.0f} ms).",
            )
            return redirect("accounts:dashboard")

        messages.error(
            request,
            f"Biometric match failed. Nose distance: {result.nose_distance:.2f}, "
            f"Thumb distance: {result.thumb_distance:.2f}. Try again with better lighting.",
        )
        return render(request, "biometrics/login.html", {"matric_no": matric})

    return render(request, "biometrics/login.html")


@login_required
def verify_self(request):
    """Re-verify biometrics while logged in (for demo / testing)."""
    if not hasattr(request.user, "biometric_template"):
        messages.error(request, "No biometric template on file.")
        return redirect("biometrics:enroll")

    if request.method == "POST":
        try:
            nose_features, thumb_features, face_features = extract_from_request(request)
        except (ValueError, NoseExtractionError, ThumbExtractionError) as exc:
            messages.error(request, str(exc))
            return render(request, "biometrics/verify.html")

        template = request.user.biometric_template
        if template.face_features:
            face_result = verify_face_only(face_features, template.face_features)
            if not face_result.accepted:
                messages.error(request, "Face does not match your enrolled profile.")
                return render(request, "biometrics/verify.html")

        result = verify_templates(
            nose_features,
            thumb_features,
            template.nose_features,
            template.thumb_features,
        )
        if result.accepted:
            messages.success(
                request,
                f"Verified in {result.elapsed_ms:.0f} ms "
                f"(nose {result.nose_distance:.2f}, thumb {result.thumb_distance:.2f}).",
            )
        else:
            messages.error(
                request,
                f"Verification failed (nose {result.nose_distance:.2f}, "
                f"thumb {result.thumb_distance:.2f}).",
            )
        return redirect("biometrics:verify")

    return render(request, "biometrics/verify.html")
