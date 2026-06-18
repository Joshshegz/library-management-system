import time
from dataclasses import dataclass

import numpy as np
from django.conf import settings


@dataclass
class MatchResult:
    accepted: bool
    nose_distance: float
    thumb_distance: float
    face_distance: float = 0.0
    elapsed_ms: float = 0.0


def euclidean(a: list[float], b: list[float]) -> float:
    va = np.asarray(a, dtype=np.float64)
    vb = np.asarray(b, dtype=np.float64)
    if va.shape != vb.shape:
        raise ValueError("Feature vectors have different dimensions.")
    return float(np.linalg.norm(va - vb))


def fused_distance(
    nose_a: list[float],
    thumb_a: list[float],
    nose_b: list[float],
    thumb_b: list[float],
    *,
    w_nose: float = 0.5,
    w_thumb: float = 0.5,
) -> tuple[float, float, float]:
    dn = euclidean(nose_a, nose_b)
    dt = euclidean(thumb_a, thumb_b)
    fused = w_nose * dn + w_thumb * dt
    return dn, dt, fused


def verify_templates(
    live_nose: list[float],
    live_thumb: list[float],
    stored_nose: list[float],
    stored_thumb: list[float],
) -> MatchResult:
    start = time.perf_counter()
    dn, dt, _ = fused_distance(live_nose, live_thumb, stored_nose, stored_thumb)

    nose_limit = getattr(settings, "BIOMETRIC_NOSE_THRESHOLD", 12.0)
    thumb_limit = getattr(settings, "BIOMETRIC_THUMB_THRESHOLD", 6.0)

    accepted = dn <= nose_limit and dt <= thumb_limit
    elapsed_ms = (time.perf_counter() - start) * 1000

    return MatchResult(
        accepted=accepted,
        nose_distance=dn,
        thumb_distance=dt,
        elapsed_ms=elapsed_ms,
    )


def verify_face_only(live_face: list[float], stored_face: list[float]) -> MatchResult:
    """Match overall face shape before nasal landmark verification."""
    start = time.perf_counter()
    df = euclidean(live_face, stored_face)
    face_limit = getattr(settings, "BIOMETRIC_FACE_THRESHOLD", 22.0)
    accepted = df <= face_limit
    elapsed_ms = (time.perf_counter() - start) * 1000

    return MatchResult(
        accepted=accepted,
        nose_distance=0.0,
        thumb_distance=0.0,
        face_distance=df,
        elapsed_ms=elapsed_ms,
    )


def verify_nose_only(live_nose: list[float], stored_nose: list[float]) -> MatchResult:
    """Match live nose landmarks against enrolled template (Windows Hello handles fingerprint)."""
    start = time.perf_counter()
    dn = euclidean(live_nose, stored_nose)
    nose_limit = getattr(settings, "BIOMETRIC_NOSE_THRESHOLD", 12.0)
    accepted = dn <= nose_limit
    elapsed_ms = (time.perf_counter() - start) * 1000

    return MatchResult(
        accepted=accepted,
        nose_distance=dn,
        thumb_distance=0.0,
        face_distance=0.0,
        elapsed_ms=elapsed_ms,
    )
