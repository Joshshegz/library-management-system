from functools import wraps

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def biometric_enrolled_required(view_func):
    @login_required
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not getattr(settings, "BIOMETRIC_REQUIRE_ENROLLMENT_TO_BORROW", True):
            return view_func(request, *args, **kwargs)
        from biometrics.enrollment import is_fully_enrolled

        if not is_fully_enrolled(request.user):
            messages.warning(
                request,
                "Complete enrollment: Step 1 Windows Hello and Step 2 nose capture.",
            )
            return redirect("biometrics:enroll")
        return view_func(request, *args, **kwargs)

    return wrapper
