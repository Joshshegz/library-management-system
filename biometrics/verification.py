from django.http import HttpRequest

from accounts.models import User

from .models import BiometricTemplate
from .services import NoseExtractionError
from .services.liveness import LivenessError
from .services.matcher import MatchResult, verify_face_only, verify_nose_only
from .utils import extract_biometrics_from_request


class NoseVerificationError(Exception):
    pass


def verify_user_nose(user: User, request: HttpRequest) -> MatchResult:
    """Liveness, then face shape match, then nose landmark match."""
    try:
        template = user.biometric_template
    except BiometricTemplate.DoesNotExist as exc:
        raise NoseVerificationError(
            "No biometric profile found. Complete enrollment first."
        ) from exc

    if not template.nose_features:
        raise NoseVerificationError(
            "Nose landmarks not enrolled. Complete Step 2 of enrollment."
        )

    if not template.face_features:
        raise NoseVerificationError(
            "Face profile not enrolled. Re-complete Step 2 (nose capture) on the enrolment page."
        )

    try:
        live_face, live_nose = extract_biometrics_from_request(request)
    except ValueError as exc:
        raise NoseVerificationError(str(exc)) from exc
    except LivenessError as exc:
        raise NoseVerificationError(str(exc)) from exc
    except NoseExtractionError as exc:
        raise NoseVerificationError(str(exc)) from exc

    face_result = verify_face_only(live_face, template.face_features)
    if not face_result.accepted:
        raise NoseVerificationError(
            f"Face does not match your enrolled profile (distance {face_result.face_distance:.2f}). "
            "Use your own account and face the camera directly."
        )

    nose_result = verify_nose_only(live_nose, template.nose_features)
    if not nose_result.accepted:
        raise NoseVerificationError(
            f"Nose verification failed (distance {nose_result.nose_distance:.2f}). "
            "Centre your nose in the circle and try again."
        )

    return MatchResult(
        accepted=True,
        nose_distance=nose_result.nose_distance,
        thumb_distance=0.0,
        face_distance=face_result.face_distance,
        elapsed_ms=face_result.elapsed_ms + nose_result.elapsed_ms,
    )
