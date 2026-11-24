import numpy as np
from numba import njit


@njit(cache=True)
def delta_troca(a, b, p, r, s):
    pr = p[r]
    ps = p[s]
    delta = (a[r, r] - a[s, s]) * (b[ps, ps] - b[pr, pr]) + (a[r, s] - a[s, r]) * (b[ps, pr] - b[pr, ps])
    for k in range(a.shape[0]):
        if k != r and k != s:
            pk = p[k]
            delta += (a[k, r] - a[k, s]) * (b[pk, ps] - b[pk, pr]) + (a[r, k] - a[s, k]) * (b[ps, pk] - b[pr, pk])
    return delta


@njit(cache=True)
def busca_local_primeira_melhora(a, b, p, custo, limite):
    n = a.shape[0]
    avaliacoes = 0
    melhorou = True
    while melhorou:
        melhorou = False
        for i in range(n):
            for j in range(i + 1, n):
                if avaliacoes >= limite:
                    return custo, avaliacoes
                delta = delta_troca(a, b, p, i, j)
                avaliacoes += 1
                if delta < 0:
                    p[i], p[j] = p[j], p[i]
                    custo += delta
                    melhorou = True
                    break
            if melhorou:
                break
    return custo, avaliacoes
