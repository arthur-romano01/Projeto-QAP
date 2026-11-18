import random
import numpy as np
from algoritmos.delta import busca_local_primeira_melhora
from algoritmos.registro import Modelo


class GRASP:
    def __init__(self, distancias, fluxos):
        self.distancias = np.array(distancias, dtype=np.int64)
        self.fluxos = np.array(fluxos, dtype=np.int64)
        self.n = len(distancias)

    def calcular_custo(self, solucao):
        fluxo_permutado = self.fluxos[np.ix_(solucao, solucao)]
        return int(np.sum(fluxo_permutado * self.distancias))

    def _custos_incrementais(self, solucao, instalacoes_livres, locais_livres):
        locais_ocupados = [loc for loc in range(self.n) if solucao[loc] != -1]
        instalacoes_ocupadas = [solucao[loc] for loc in locais_ocupados]

        fluxo_saida = self.fluxos[np.ix_(instalacoes_livres, instalacoes_ocupadas)]
        dist_saida = self.distancias[np.ix_(locais_livres, locais_ocupados)]
        fluxo_entrada = self.fluxos[np.ix_(instalacoes_ocupadas, instalacoes_livres)]
        dist_entrada = self.distancias[np.ix_(locais_ocupados, locais_livres)]

        return fluxo_saida @ dist_saida.T + fluxo_entrada.T @ dist_entrada

    def _construir_solucao(self, alfa):
        solucao = [-1] * self.n
        instalacoes_livres = list(range(self.n))
        locais_livres = list(range(self.n))

        for _ in range(self.n):
            custos = self._custos_incrementais(solucao, instalacoes_livres, locais_livres).ravel()
            ordem = np.argsort(custos, kind="stable")

            min_c, max_c = int(custos.min()), int(custos.max())
            limite = min_c + alfa * (max_c - min_c)
            tamanho_rcl = int(np.count_nonzero(custos <= limite))

            escolhido = int(ordem[random.choice(range(tamanho_rcl))])
            idx_inst, idx_loc = divmod(escolhido, len(locais_livres))
            inst_escolhida = instalacoes_livres[idx_inst]
            loc_escolhido = locais_livres[idx_loc]

            solucao[loc_escolhido] = inst_escolhida
            instalacoes_livres.remove(inst_escolhida)
            locais_livres.remove(loc_escolhido)

        return solucao

    def _busca_local(self, solucao, custo_atual, limite):
        permutacao = np.array(solucao, dtype=np.int64)
        custo, avaliacoes = busca_local_primeira_melhora(
            self.distancias, self.fluxos, permutacao, custo_atual, limite
        )
        return permutacao.tolist(), int(custo), int(avaliacoes)

    def executar(self, max_iteracoes=150, alfa=0.15, orcamento=None):
        melhor_solucao = None
        melhor_custo = float("inf")
        limite_total = int(np.iinfo(np.int64).max) if orcamento is None else orcamento
        total_iteracoes = max_iteracoes if orcamento is None else orcamento
        self.avaliacoes = 0

        for _ in range(total_iteracoes):
            if self.avaliacoes >= limite_total:
                break

            solucao = self._construir_solucao(alfa)
            custo = self.calcular_custo(solucao)
            solucao, custo, avaliacoes = self._busca_local(solucao, custo, limite_total - self.avaliacoes)
            self.avaliacoes += avaliacoes

            if custo < melhor_custo:
                melhor_custo = custo
                melhor_solucao = solucao.copy()

        return melhor_solucao, melhor_custo


MODELO = Modelo(
    chave="grasp",
    nome="GRASP",
    rotulo="GRASP",
    classe=GRASP,
    params={"max_iteracoes": 150, "alfa": 0.35},
)
