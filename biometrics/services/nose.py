from dataclasses import dataclass
from pathlib import Path
import urllib.request

import numpy as np

# Face mesh nasal region indices (MediaPipe face landmarker)
NOSE_LANDMARK_INDICES = [1, 4, 5, 6, 19, 94, 168, 197, 240, 460]

# Broader face shape (oval, eyes, cheeks) — checked before nose-only match
FACE_IDENTITY_INDICES = sorted(
    {
        10,
        21,
        54,
        58,
        67,
        93,
        103,
        109,
        127,
        132,
        136,
        148,
        149,
        150,
        152,
        162,
        172,
        176,
        234,
        251,
        284,
        288,
        297,
        323,
        332,
        338,
        356,
        361,
        365,
        377,
        378,
        379,
        389,
        397,
        400,
        454,
        33,
        133,
        263,
        362,
        61,
        291,
        199,
        175,
    }
)

# For blink / liveness (MediaPipe face mesh)
LEFT_EYE_INDICES = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_INDICES = [362, 385, 387, 263, 373, 380]
# Mouth — open-wide gesture for liveness (corners + lip center)
MOUTH_TOP = 13
MOUTH_BOTTOM = 14
MOUTH_LEFT = 61
MOUTH_RIGHT = 291

FACE_LANDMARKER_URL = (
    "https://storage.googleapis.com/mediapipe-models/face_landmarker/"
    "face_landmarker/float16/1/face_landmarker.task"
)
MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "face_landmarker.task"

_landmarker = None


class NoseExtractionError(Exception):
    pass


def _landmark_vector(landmarks, indices: list[int], w: int, h: int) -> list[float]:
    coords = []
    for index in indices:
        if index >= len(landmarks):
            continue
        lm = landmarks[index]
        coords.extend([lm.x * w, lm.y * h])
    if len(coords) < 6:
        return []
    arr = np.array(coords, dtype=np.float64)
    return ((arr - arr.mean()) / (arr.std() + 1e-6)).tolist()


@dataclass
class NoseProbe:
    """Single frame: face + nose vectors and liveness metrics."""

    normalized: list[float]
    face_normalized: list[float]
    raw_xy: list[float]
    mean_visibility: float
    mean_presence: float
    z_spread: float
    ear_left: float
    ear_right: float
    mouth_aspect_ratio: float


def _ensure_model() -> str:
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not MODEL_PATH.is_file():
        try:
            urllib.request.urlretrieve(FACE_LANDMARKER_URL, MODEL_PATH)
        except OSError as exc:
            raise NoseExtractionError(
                "Could not download face model. Check your internet connection."
            ) from exc
    return str(MODEL_PATH)


def _get_landmarker():
    global _landmarker
    if _landmarker is not None:
        return _landmarker

    try:
        import mediapipe as mp
        from mediapipe.tasks import python
        from mediapipe.tasks.python import vision
    except ImportError as exc:
        raise NoseExtractionError("MediaPipe is not installed.") from exc

    options = vision.FaceLandmarkerOptions(
        base_options=python.BaseOptions(model_asset_path=_ensure_model()),
        running_mode=vision.RunningMode.IMAGE,
        num_faces=1,
        min_face_detection_confidence=0.5,
        min_face_presence_confidence=0.5,
        min_tracking_confidence=0.5,
    )
    _landmarker = vision.FaceLandmarker.create_from_options(options)
    return _landmarker


def _lm_visibility(lm) -> float:
    v = getattr(lm, "visibility", None)
    return float(v) if v is not None else 1.0


def _lm_presence(lm) -> float:
    p = getattr(lm, "presence", None)
    return float(p) if p is not None else 1.0


def _eye_aspect_ratio(landmarks, eye_indices: list[int], w: int, h: int) -> float:
    if len(eye_indices) < 6:
        return 1.0
    pts = []
    for i in eye_indices:
        if i >= len(landmarks):
            continue
        lm = landmarks[i]
        pts.append((lm.x * w, lm.y * h))
    if len(pts) < 6:
        return 1.0
    v1 = np.linalg.norm(np.array(pts[1]) - np.array(pts[5]))
    v2 = np.linalg.norm(np.array(pts[2]) - np.array(pts[4]))
    h_dist = np.linalg.norm(np.array(pts[0]) - np.array(pts[3]))
    if h_dist < 1e-6:
        return 1.0
    return float((v1 + v2) / (2.0 * h_dist))


def _mouth_aspect_ratio(landmarks, w: int, h: int) -> float:
    """Vertical mouth opening divided by width — increases when mouth is open."""
    needed = (MOUTH_TOP, MOUTH_BOTTOM, MOUTH_LEFT, MOUTH_RIGHT)
    if max(needed) >= len(landmarks):
        return 0.0
    top = np.array([landmarks[MOUTH_TOP].x * w, landmarks[MOUTH_TOP].y * h])
    bottom = np.array([landmarks[MOUTH_BOTTOM].x * w, landmarks[MOUTH_BOTTOM].y * h])
    left = np.array([landmarks[MOUTH_LEFT].x * w, landmarks[MOUTH_LEFT].y * h])
    right = np.array([landmarks[MOUTH_RIGHT].x * w, landmarks[MOUTH_RIGHT].y * h])
    vertical = float(np.linalg.norm(top - bottom))
    horizontal = float(np.linalg.norm(left - right))
    if horizontal < 1e-6:
        return 0.0
    return vertical / horizontal


def extract_nose_probe(image_bgr: np.ndarray) -> NoseProbe:
    import cv2
    import mediapipe as mp

    h, w = image_bgr.shape[:2]
    rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

    result = _get_landmarker().detect(mp_image)

    if not result.face_landmarks:
        raise NoseExtractionError(
            "No face detected. Face the camera with good lighting and centre your nose."
        )

    landmarks = result.face_landmarks[0]
    coords = []
    visibilities = []
    z_vals = []

    for index in NOSE_LANDMARK_INDICES:
        if index >= len(landmarks):
            continue
        lm = landmarks[index]
        coords.extend([lm.x * w, lm.y * h])
        visibilities.append(_lm_visibility(lm))
        z_vals.append(float(lm.z))

    if len(coords) < 6:
        raise NoseExtractionError("Could not extract enough nose landmarks.")

    arr = np.array(coords, dtype=np.float64)
    normalized = ((arr - arr.mean()) / (arr.std() + 1e-6)).tolist()
    face_normalized = _landmark_vector(landmarks, FACE_IDENTITY_INDICES, w, h)
    if not face_normalized:
        raise NoseExtractionError("Could not extract enough face landmarks.")

    z_spread = float(max(z_vals) - min(z_vals)) if z_vals else 0.0

    return NoseProbe(
        normalized=normalized,
        face_normalized=face_normalized,
        raw_xy=coords,
        mean_visibility=float(np.mean(visibilities)) if visibilities else 0.0,
        mean_presence=float(np.mean([_lm_presence(landmarks[i]) for i in NOSE_LANDMARK_INDICES if i < len(landmarks)]))
        if landmarks
        else 0.0,
        z_spread=z_spread,
        ear_left=_eye_aspect_ratio(landmarks, LEFT_EYE_INDICES, w, h),
        ear_right=_eye_aspect_ratio(landmarks, RIGHT_EYE_INDICES, w, h),
        mouth_aspect_ratio=_mouth_aspect_ratio(landmarks, w, h),
    )


def extract_nose_features(image_bgr: np.ndarray) -> list[float]:
    return extract_nose_probe(image_bgr).normalized
