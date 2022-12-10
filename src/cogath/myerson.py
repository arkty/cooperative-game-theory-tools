import numpy as np


def myerson(a, k):
    """
    Calculate Modified Myerson-value for given graph
    http://dx.doi.org/10.1134/S0005117921010100
    a - Adjacency matrix of graph
    k - path length
    """

    n = len(a)
    a_k = np.empty(k + 1, dtype=np.ndarray)
    a_k[0] = a
    a_k[1] = a

    for i in range(2, k + 1):
        a_k[i] = np.matmul(a_k[i - 1], a)

    a_sums = np.empty(n, dtype=np.ndarray)
    for i in range(k + 1):
        a_sums[i] = np.sum(a_k[i], axis=1)

    s_k = np.empty(n, dtype=np.int32)
    l_sum = np.sum(a_k[k], axis=0)

    for i in range(n):
        l_inside = np.empty(n, dtype=np.int32)
        for l in range(n):
            l_inside[l] = sum(
                a_k[r][l, i] * a_sums[k - r][i, 0]
                for r in range(1, k)
            )
        main = l_inside.sum() + l_sum[0, i]
        s_k[i] = a_sums[k][i, 0] + main
    return s_k
