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
def matriz_deltas(a, b, p):
    n = a.shape[0]
    deltas = np.zeros((n, n), dtype=np.int64)
    for u in range(n):
        for v in range(u + 1, n):
            deltas[u, v] = delta_troca(a, b, p, u, v)
    return deltas


@njit(cache=True)
def atualizar_deltas(deltas, a, b, p, r, s):
    n = a.shape[0]
    pr = p[r]
    ps = p[s]
    for u in range(n):
        for v in range(u + 1, n):
            if u == r or u == s or v == r or v == s:
                deltas[u, v] = delta_troca(a, b, p, u, v)
            else:
                pu = p[u]
                pv = p[v]
                deltas[u, v] += (a[r, u] - a[r, v] + a[s, v] - a[s, u]) * (
                    b[ps, pu] - b[ps, pv] + b[pr, pv] - b[pr, pu]
                ) + (a[u, r] - a[v, r] + a[v, s] - a[u, s]) * (b[pu, ps] - b[pv, ps] + b[pv, pr] - b[pu, pr])


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


@njit(cache=True)
def busca_tabu(a, b, p, custo, max_iteracoes, tamanho_lista_tabu):
    n = a.shape[0]
    deltas = matriz_deltas(a, b, p)
    memoria_tabu = np.zeros((n, n), dtype=np.int64)
    melhor_custo = custo
    melhor_solucao = p.copy()

    for it in range(max_iteracoes):
        melhor_i = -1
        melhor_j = -1
        melhor_delta = np.iinfo(np.int64).max

        for i in range(n):
            for j in range(i + 1, n):
                delta = deltas[i, j]
                if delta < melhor_delta and (memoria_tabu[i, j] <= it or custo + delta < melhor_custo):
                    melhor_delta = delta
                    melhor_i = i
                    melhor_j = j

        if melhor_i < 0:
            continue

        p[melhor_i], p[melhor_j] = p[melhor_j], p[melhor_i]
        custo += melhor_delta
        memoria_tabu[melhor_i, melhor_j] = it + tamanho_lista_tabu
        memoria_tabu[melhor_j, melhor_i] = it + tamanho_lista_tabu

        if custo < melhor_custo:
            melhor_custo = custo
            melhor_solucao[:] = p

        atualizar_deltas(deltas, a, b, p, melhor_i, melhor_j)

    return melhor_solucao, melhor_custo
