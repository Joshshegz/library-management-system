import json

from .services.liveness import LivenessError, validate_nose_probes
from .services.nose import NoseExtractionError, NoseProbe, extract_nose_probe
from .services.preprocessing import decode_data_url


def _decode_frames_from_request(request) -> list:
    """Liveness frames as JSON list of data URLs, or single nose_image fallback."""
    raw = request.POST.get("nose_liveness_frames", "").strip()
    if raw:
        try:
            frames = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid liveness data. Run the liveness capture again.") from exc
        if not isinstance(frames, list) or not frames:
            raise ValueError("Liveness capture is empty. Try again.")
        return frames

    single = request.POST.get("nose_image", "").strip()
    if single:
        return [single]

    raise ValueError(
        "Complete the liveness check first (multiple live captures required)."
    )


def extract_nose_probes_from_request(request) -> list[NoseProbe]:
    probes = []
    for data_url in _decode_frames_from_request(request):
        image_bgr = decode_data_url(data_url)
        probes.append(extract_nose_probe(image_bgr))
    validate_nose_probes(probes)
    return probes


def extract_biometrics_from_request(request) -> tuple[list[float], list[float]]:
    """Last frame after liveness: (face_shape_vector, nose_vector)."""
    probes = extract_nose_probes_from_request(request)
    last = probes[-1]
    return last.face_normalized, last.normalized


def extract_nose_from_request(request) -> list[float]:
    """Last frame nose vector only (legacy callers)."""
    _, nose = extract_biometrics_from_request(request)
    return nose


