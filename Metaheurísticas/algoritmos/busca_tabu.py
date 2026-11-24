import random
import numpy as np
from algoritmos.delta import busca_tabu
from algoritmos.registro import Modelo


class BuscaTabu:
    def __init__(self, distancias, fluxos):
        self.distancias = np.array(distancias, dtype=np.int64)
        self.fluxos = np.array(fluxos, dtype=np.int64)
        self.n = len(distancias)

    def calcular_custo(self, solucao):
        dist_permutada = self.distancias[np.ix_(solucao, solucao)]
        return int(np.sum(self.fluxos * dist_permutada))

    def executar(self, max_iteracoes=800, tamanho_lista_tabu=10, orcamento=None):
        vizinhanca = self.n * (self.n - 1) // 2
        if orcamento is not None:
            max_iteracoes = orcamento // vizinhanca
        self.avaliacoes = max_iteracoes * vizinhanca

        solucao_inicial = list(range(self.n))
        random.shuffle(solucao_inicial)

        melhor_solucao, melhor_custo = busca_tabu(
            self.fluxos,
            self.distancias,
            np.array(solucao_inicial, dtype=np.int64),
            self.calcular_custo(solucao_inicial),
            max_iteracoes,
            tamanho_lista_tabu,
        )
        return melhor_solucao.tolist(), int(melhor_custo)


MODELO = Modelo(
    chave="tabu",
    nome="Busca Tabu",
    rotulo="Tabu",
    classe=BuscaTabu,
    params={"max_iteracoes": 800, "tamanho_lista_tabu": 10},
)
