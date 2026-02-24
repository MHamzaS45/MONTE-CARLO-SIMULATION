import numpy as np


def antithetic_normals(n_paths: int, n_steps: int):
    half = n_paths // 2
    z = np.random.standard_normal((half, n_steps))

    return np.vstack([z, -z])