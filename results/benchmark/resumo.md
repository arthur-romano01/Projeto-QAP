# Benchmark semeado - Metaheurísticas

- **Gerado em:** 18/11/2026 20:25
- **Execuções por modelo e instância:** 30
- **Sementes:** 0 a 29
- **Orçamento:** 800 varreduras da vizinhança, ou 800 · n(n-1)/2 avaliações de troca
- **Duração total:** 156 s com 8 processos
- **Parâmetros de GRASP:** `{'max_iteracoes': 150, 'alfa': 0.35}`
- **Parâmetros de Simulated Annealing:** `{'taxa_temp_inicial': 0.05, 'fator_resfriamento': 1e-06, 'alfa': 0.95, 'iter_por_temp': 150}`
- **Parâmetros de Busca Tabu:** `{'max_iteracoes': 800, 'tamanho_lista_tabu': 10}`

## `nug12` (n=12)

| Modelo | Gap médio (%) | Desvio | Melhor | Pior | Ótimo atingido | Tempo médio (s) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| GRASP | 0.05 | 0.25 | 0.00 | 1.38 | 29/30 | 0.443 |
| SA | 1.23 | 0.89 | 0.00 | 3.11 | 8/30 | 0.642 |
| Tabu | 0.66 | 1.20 | 0.00 | 3.81 | 21/30 | 0.005 |

## `chr15a` (n=15)

| Modelo | Gap médio (%) | Desvio | Melhor | Pior | Ótimo atingido | Tempo médio (s) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| GRASP | 6.53 | 5.00 | 0.83 | 21.26 | 0/30 | 0.495 |
| SA | 16.18 | 10.44 | 0.00 | 42.56 | 1/30 | 0.913 |
| Tabu | 11.89 | 12.65 | 0.00 | 41.92 | 2/30 | 0.009 |

## `had18` (n=18)

| Modelo | Gap médio (%) | Desvio | Melhor | Pior | Ótimo atingido | Tempo médio (s) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| GRASP | 0.00 | 0.03 | 0.00 | 0.15 | 29/30 | 0.317 |
| SA | 0.12 | 0.16 | 0.00 | 0.75 | 13/30 | 1.290 |
| Tabu | 0.32 | 0.48 | 0.00 | 1.27 | 15/30 | 0.019 |

## `els19` (n=19)

| Modelo | Gap médio (%) | Desvio | Melhor | Pior | Ótimo atingido | Tempo médio (s) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| GRASP | 3.50 | 1.51 | 0.00 | 4.80 | 1/30 | 0.256 |
| SA | 8.69 | 7.45 | 0.00 | 30.92 | 1/30 | 1.555 |
| Tabu | 22.45 | 16.53 | 0.00 | 57.36 | 1/30 | 0.018 |

## `rou20` (n=20)

| Modelo | Gap médio (%) | Desvio | Melhor | Pior | Ótimo atingido | Tempo médio (s) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| GRASP | 1.00 | 0.49 | 0.18 | 2.07 | 0/30 | 0.677 |
| SA | 1.63 | 0.98 | 0.08 | 3.60 | 0/30 | 2.018 |
| Tabu | 0.37 | 0.26 | 0.00 | 1.19 | 1/30 | 0.018 |

## `bur26a` (n=26)

| Modelo | Gap médio (%) | Desvio | Melhor | Pior | Ótimo atingido | Tempo médio (s) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| GRASP | 0.10 | 0.05 | 0.00 | 0.16 | 2/30 | 0.497 |
| SA | 0.12 | 0.05 | 0.00 | 0.21 | 2/30 | 3.224 |
| Tabu | 0.23 | 0.12 | 0.09 | 0.58 | 0/30 | 0.027 |

## `kra30a` (n=30)

| Modelo | Gap médio (%) | Desvio | Melhor | Pior | Ótimo atingido | Tempo médio (s) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| GRASP | 2.78 | 0.71 | 1.35 | 4.05 | 0/30 | 0.612 |
| SA | 2.37 | 1.18 | 0.00 | 6.37 | 2/30 | 4.610 |
| Tabu | 4.93 | 1.71 | 2.14 | 8.55 | 0/30 | 0.047 |

## `nug30` (n=30)

| Modelo | Gap médio (%) | Desvio | Melhor | Pior | Ótimo atingido | Tempo médio (s) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| GRASP | 1.21 | 0.40 | 0.42 | 2.12 | 0/30 | 0.491 |
| SA | 0.80 | 0.54 | 0.07 | 1.73 | 0/30 | 5.107 |
| Tabu | 0.54 | 0.42 | 0.07 | 1.60 | 0/30 | 0.030 |

## `ste36a` (n=36)

| Modelo | Gap médio (%) | Desvio | Melhor | Pior | Ótimo atingido | Tempo médio (s) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| GRASP | 3.91 | 1.33 | 1.01 | 6.30 | 0/30 | 0.727 |
| SA | 1.83 | 1.34 | 0.23 | 4.93 | 0/30 | 6.628 |
| Tabu | 6.61 | 3.41 | 0.97 | 14.38 | 0/30 | 0.064 |

## `sko42` (n=42)

| Modelo | Gap médio (%) | Desvio | Melhor | Pior | Ótimo atingido | Tempo médio (s) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| GRASP | 1.32 | 0.25 | 0.68 | 1.73 | 0/30 | 0.918 |
| SA | 0.56 | 0.29 | 0.00 | 1.51 | 1/30 | 9.294 |
| Tabu | 1.11 | 0.66 | 0.21 | 2.68 | 0/30 | 0.088 |
