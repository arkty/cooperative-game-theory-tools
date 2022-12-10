import numpy as np
from scipy.stats import rankdata


def kirchhoff_tournament(a: np.ndarray, delta, round_to=5):
    n = len(a)
    one = np.full((n, n), 1.0, dtype=float)
    w = np.divide(one, a, out=np.zeros_like(one), where=a != 0)
    d = np.sum(w, axis=1)
    l = -w
    np.fill_diagonal(l, d + delta)

    l_inv = np.linalg.inv(l)
    t_matrix = np.zeros((n, n))
    b = np.zeros((n, 1), dtype=float)

    for i in range(0, n):
        if i > 0:
            b[i - 1][0] = 0
        b[i][0] = 1
        phi = np.dot(l_inv, b).sum(axis=1)

        t_matrix[i] = rankdata(
            list(map(lambda it: np.round(-it, round_to), phi)),
            method='dense'
        )

    return t_matrix
