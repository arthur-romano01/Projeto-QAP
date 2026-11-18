import math
import random
import numpy as np


class SimulatedAnnealing:
    def __init__(self, distancias, fluxos):
        self.distancias = np.array(distancias)
        self.fluxos = np.array(fluxos)
        self.n = len(distancias)

    def calcular_custo(self, solucao):
        dist_permutada = self.distancias[np.ix_(solucao, solucao)]
        return int(np.sum(self.fluxos * dist_permutada))

    def executar(self, taxa_temp_inicial=0.05, fator_resfriamento=1e-6, alfa=0.95, iter_por_temp=150):
        solucao_atual = list(range(self.n))
        random.shuffle(solucao_atual)
        custo_atual = self.calcular_custo(solucao_atual)

        melhor_solucao = solucao_atual.copy()
        melhor_custo = custo_atual

        temp = custo_atual * taxa_temp_inicial
        temp_final = temp * fator_resfriamento

        while temp > temp_final:
            for _ in range(iter_por_temp):
                i, j = random.sample(range(self.n), 2)
                vizinho = solucao_atual.copy()
                vizinho[i], vizinho[j] = vizinho[j], vizinho[i]

                custo_viz = self.calcular_custo(vizinho)
                delta = custo_viz - custo_atual

                if delta < 0 or random.random() < math.exp(-delta / temp):
                    solucao_atual = vizinho
                    custo_atual = custo_viz

                    if custo_atual < melhor_custo:
                        melhor_custo = custo_atual
                        melhor_solucao = solucao_atual.copy()

            temp *= alfa

        return melhor_solucao, melhor_custo