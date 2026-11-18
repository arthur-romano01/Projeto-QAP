import random


class GRASP:
    def __init__(self, distancias, fluxos):
        self.distancias = distancias
        self.fluxos = fluxos
        self.n = len(distancias)

    def calcular_custo(self, solucao):
        custo = 0
        for i in range(self.n):
            for j in range(self.n):
                custo += self.fluxos[solucao[i]][solucao[j]] * self.distancias[i][j]
        return custo

    def _construir_solucao(self, alfa):
        """Fase construtiva gulosa-aleatória baseada na RCL."""
        solucao = [-1] * self.n
        instalacoes_livres = list(range(self.n))
        locais_livres = list(range(self.n))

        for _ in range(self.n):
            candidatos = []
            for inst in instalacoes_livres:
                for loc in locais_livres:
                    custo_inc = sum(
                        self.fluxos[inst][solucao[loc_oc]] * self.distancias[loc][loc_oc]
                        + self.fluxos[solucao[loc_oc]][inst] * self.distancias[loc_oc][loc]
                        for loc_oc in range(self.n) if solucao[loc_oc] != -1
                    )
                    candidatos.append((custo_inc, inst, loc))

            candidatos.sort(key=lambda x: x[0])
            min_c, max_c = candidatos[0][0], candidatos[-1][0]
            limite = min_c + alfa * (max_c - min_c)

            rcl = [item for item in candidatos if item[0] <= limite]
            _, inst_escolhida, loc_escolhido = random.choice(rcl)

            solucao[loc_escolhido] = inst_escolhida
            instalacoes_livres.remove(inst_escolhida)
            locais_livres.remove(loc_escolhido)

        return solucao

    def _busca_local(self, solucao, custo_atual):
        """Refinamento 2-opt (First Improvement)."""
        melhorou = True
        while melhorou:
            melhorou = False
            for i in range(self.n):
                for j in range(i + 1, self.n):
                    vizinho = solucao.copy()
                    vizinho[i], vizinho[j] = vizinho[j], vizinho[i]
                    custo_viz = self.calcular_custo(vizinho)

                    if custo_viz < custo_atual:
                        solucao = vizinho
                        custo_atual = custo_viz
                        melhorou = True
                        break
                if melhorou:
                    break
        return solucao, custo_atual

    def executar(self, max_iteracoes=150, alfa=0.15):
        melhor_solucao = None
        melhor_custo = float("inf")

        for _ in range(max_iteracoes):
            solucao = self._construir_solucao(alfa)
            custo = self.calcular_custo(solucao)
            solucao, custo = self._busca_local(solucao, custo)

            if custo < melhor_custo:
                melhor_custo = custo
                melhor_solucao = solucao.copy()

        return melhor_solucao, melhor_custo