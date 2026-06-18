from .models import BiometricTemplate


def has_windows_hello(user) -> bool:
    return user.webauthn_credentials.exists()


def has_nose_template(user) -> bool:
    try:
        template = user.biometric_template
    except BiometricTemplate.DoesNotExist:
        return False
    return bool(template.nose_features) and bool(template.face_features)


def is_fully_enrolled(user) -> bool:
    return has_windows_hello(user) and has_nose_template(user)


def sync_enrolled_flag(user) -> None:
    enrolled = is_fully_enrolled(user)
    if user.biometric_enrolled != enrolled:
        user.biometric_enrolled = enrolled
        user.save(update_fields=["biometric_enrolled"])
