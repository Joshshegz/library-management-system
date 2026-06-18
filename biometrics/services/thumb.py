import numpy as np
from sklearn.decomposition import FastICA

from .preprocessing import preprocess_grayscale


class ThumbExtractionError(Exception):
    pass


def extract_thumb_features(image_bgr: np.ndarray, n_components: int = 20) -> list[float]:
    gray = preprocess_grayscale(image_bgr, size=128)

    patches = []
    patch_size = 16
    for row in range(0, 128, patch_size):
        for col in range(0, 128, patch_size):
            patch = gray[row : row + patch_size, col : col + patch_size].flatten()
            patches.append(patch)

    matrix = np.array(patches, dtype=np.float64)
    matrix -= matrix.mean(axis=0)
    matrix /= matrix.std(axis=0) + 1e-6

    n_comp = min(n_components, matrix.shape[0], matrix.shape[1])
    if n_comp < 2:
        raise ThumbExtractionError("Thumb image quality too low for ICA.")

    ica = FastICA(n_components=n_comp, random_state=42, max_iter=400)
    transformed = ica.fit_transform(matrix)
    features = np.mean(transformed, axis=0)

    return features.tolist()
