import math
import random
import numpy as np
from algoritmos.delta import delta_troca
from algoritmos.registro import Modelo


class SimulatedAnnealing:
    def __init__(self, distancias, fluxos):
        self.distancias = np.array(distancias, dtype=np.int64)
        self.fluxos = np.array(fluxos, dtype=np.int64)
        self.n = len(distancias)

    def calcular_custo(self, solucao):
        dist_permutada = self.distancias[np.ix_(solucao, solucao)]
        return int(np.sum(self.fluxos * dist_permutada))

    def executar(self, taxa_temp_inicial=0.05, fator_resfriamento=1e-6, alfa=0.95, iter_por_temp=150, orcamento=None):
        if orcamento is not None:
            niveis = math.ceil(math.log(fator_resfriamento) / math.log(alfa))
            iter_por_temp = max(1, orcamento // niveis)
        self.avaliacoes = 0

        solucao_inicial = list(range(self.n))
        random.shuffle(solucao_inicial)
        custo_atual = self.calcular_custo(solucao_inicial)

        solucao_atual = np.array(solucao_inicial, dtype=np.int64)
        melhor_solucao = solucao_atual.copy()
        melhor_custo = custo_atual

        temp = custo_atual * taxa_temp_inicial
        temp_final = temp * fator_resfriamento

        while temp > temp_final and (orcamento is None or self.avaliacoes < orcamento):
            passos = iter_por_temp if orcamento is None else min(iter_por_temp, orcamento - self.avaliacoes)
            self.avaliacoes += passos

            for _ in range(passos):
                i, j = random.sample(range(self.n), 2)
                delta = int(delta_troca(self.fluxos, self.distancias, solucao_atual, i, j))

                if delta < 0 or random.random() < math.exp(-delta / temp):
                    solucao_atual[i], solucao_atual[j] = solucao_atual[j], solucao_atual[i]
                    custo_atual += delta

                    if custo_atual < melhor_custo:
                        melhor_custo = custo_atual
                        melhor_solucao = solucao_atual.copy()

            temp *= alfa

        return melhor_solucao.tolist(), melhor_custo


MODELO = Modelo(
    chave="sa",
    nome="Simulated Annealing",
    rotulo="SA",
    classe=SimulatedAnnealing,
    params={
        "taxa_temp_inicial": 0.05,
        "fator_resfriamento": 1e-6,
        "alfa": 0.95,
        "iter_por_temp": 150,
    },
)
