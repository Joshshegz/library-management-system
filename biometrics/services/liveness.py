"""Multi-frame and visibility checks before nose template matching."""

from dataclasses import dataclass

import numpy as np
from django.conf import settings

from .nose import NoseProbe


class LivenessError(Exception):
    pass


@dataclass
class LivenessResult:
    passed: bool
    movement_score: float
    blink_score: float
    mouth_score: float
    mean_visibility: float


def _frame_movement(probe_a: NoseProbe, probe_b: NoseProbe) -> float:
    a = np.asarray(probe_a.raw_xy, dtype=np.float64).reshape(-1, 2)
    b = np.asarray(probe_b.raw_xy, dtype=np.float64).reshape(-1, 2)
    if a.shape != b.shape or a.size == 0:
        return 0.0
    return float(np.mean(np.linalg.norm(a - b, axis=1)))


def _pairwise_nose_distance(probe_a: NoseProbe, probe_b: NoseProbe) -> float:
    va = np.asarray(probe_a.normalized, dtype=np.float64)
    vb = np.asarray(probe_b.normalized, dtype=np.float64)
    if va.shape != vb.shape:
        return 999.0
    return float(np.linalg.norm(va - vb))


def _pairwise_face_distance(probe_a: NoseProbe, probe_b: NoseProbe) -> float:
    va = np.asarray(probe_a.face_normalized, dtype=np.float64)
    vb = np.asarray(probe_b.face_normalized, dtype=np.float64)
    if va.shape != vb.shape or va.size == 0:
        return 999.0
    return float(np.linalg.norm(va - vb))


def validate_nose_probes(probes: list[NoseProbe]) -> LivenessResult:
    min_frames = getattr(settings, "BIOMETRIC_LIVENESS_MIN_FRAMES", 3)
    min_visibility = getattr(settings, "BIOMETRIC_LIVENESS_MIN_VISIBILITY", 0.40)
    min_movement = getattr(settings, "BIOMETRIC_LIVENESS_MIN_MOVEMENT", 0.8)
    max_movement = getattr(settings, "BIOMETRIC_LIVENESS_MAX_MOVEMENT", 120.0)
    max_nose_static = getattr(settings, "BIOMETRIC_LIVENESS_MAX_STATIC_SIMILARITY", 0.25)
    max_face_static = getattr(settings, "BIOMETRIC_LIVENESS_MAX_FACE_STATIC_SIMILARITY", 0.20)
    min_blink = getattr(settings, "BIOMETRIC_LIVENESS_MIN_BLINK_DELTA", 0.012)
    min_mouth = getattr(settings, "BIOMETRIC_LIVENESS_MIN_MOUTH_DELTA", 0.04)
    min_z_spread = getattr(settings, "BIOMETRIC_LIVENESS_MIN_Z_SPREAD", 0.006)

    if len(probes) < min_frames:
        raise LivenessError(
            f"Liveness requires {min_frames} live captures. Complete all capture steps."
        )

    mean_vis = float(np.mean([p.mean_visibility for p in probes]))
    if mean_vis < min_visibility:
        raise LivenessError(
            "Nose area not clearly visible. Remove hands or masks covering your nose."
        )

    for probe in probes:
        if probe.z_spread < min_z_spread:
            raise LivenessError(
                "Could not read a clear nose shape. Face the camera with your nose uncovered."
            )

    movements = [_frame_movement(probes[i - 1], probes[i]) for i in range(1, len(probes))]
    movement_score = float(np.median(movements)) if movements else 0.0
    peak_movement = float(max(movements)) if movements else 0.0

    if movement_score < min_movement:
        raise LivenessError(
            "Little movement between steps. Open your mouth wide on step 2, then try again."
        )

    if peak_movement > max_movement:
        raise LivenessError(
            "Camera was too shaky. Keep your face in frame and try again."
        )

    max_nose_dist = 0.0
    max_face_dist = 0.0
    for i in range(len(probes)):
        for j in range(i + 1, len(probes)):
            max_nose_dist = max(max_nose_dist, _pairwise_nose_distance(probes[i], probes[j]))
            max_face_dist = max(max_face_dist, _pairwise_face_distance(probes[i], probes[j]))

    ear_values = [
        (p.ear_left + p.ear_right) / 2.0
        for p in probes
        if p.ear_left > 0 and p.ear_right > 0
    ]
    blink_score = float(max(ear_values) - min(ear_values)) if ear_values else 0.0

    mouth_values = [p.mouth_aspect_ratio for p in probes if p.mouth_aspect_ratio > 0]
    mouth_score = float(max(mouth_values) - min(mouth_values)) if mouth_values else 0.0

    has_blink = blink_score >= min_blink
    has_mouth = mouth_score >= min_mouth
    has_expression = has_blink or has_mouth

    nose_looks_static = max_nose_dist < max_nose_static
    face_looks_static = max_face_dist < max_face_static

    if nose_looks_static and face_looks_static and not has_expression:
        raise LivenessError(
            "Frames look too similar. On step 2, open your mouth wide before capturing — "
            "do not use a still photo."
        )

    if not has_expression and movement_score < min_movement * 2:
        raise LivenessError(
            "Open your mouth wide on step 2 (or blink), then capture that frame."
        )

    return LivenessResult(
        passed=True,
        movement_score=movement_score,
        blink_score=blink_score,
        mouth_score=mouth_score,
        mean_visibility=mean_vis,
    )
