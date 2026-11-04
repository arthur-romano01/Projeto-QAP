import numpy as np
import random
import math
import time
from pathlib import Path

class SimulatedAnnealingQAP:
    def __init__(self, caminho_arquivo):
        self.n, self.fluxo, self.distancia = self._carregar_dados_numpy(caminho_arquivo)

    def _carregar_dados_numpy(self, caminho):
        with open(caminho, 'r') as arquivo:
            valores = np.array([int(x) for x in arquivo.read().split()])
        
        n = valores[0]
        distancia = valores[1 : 1 + n*n].reshape((n, n))
        fluxo = valores[1 + n*n : 1 + 2*n*n].reshape((n, n))
        return n, fluxo, distancia

    def calcular_custo(self, solucao):
        distancia_permutada = self.distancia[np.ix_(solucao, solucao)]
        return np.sum(self.fluxo * distancia_permutada)

    def executar_sa(self, temp_inicial=5000, temp_final=0.1, alfa=0.95, iter_por_temp=150):
        solucao_atual = list(range(self.n))
        random.shuffle(solucao_atual)
        custo_atual = self.calcular_custo(solucao_atual)
        
        melhor_solucao = solucao_atual.copy()
        melhor_custo = custo_atual
        
        temp_atual = temp_inicial
        
        while temp_atual > temp_final:
            for _ in range(iter_por_temp):
                i, j = random.sample(range(self.n), 2)
                
                vizinho = solucao_atual.copy()
                vizinho[i], vizinho[j] = vizinho[j], vizinho[i]
                
                custo_vizinho = self.calcular_custo(vizinho)
                
                delta = custo_vizinho - custo_atual
                
                if delta < 0:
                    aceitar = True # É melhor, aceita na hora
                else:
                    probabilidade = math.exp(-delta / temp_atual)
                    aceitar = random.random() < probabilidade
                    
                if aceitar:
                    solucao_atual = vizinho
                    custo_atual = custo_vizinho
                    
                    if custo_atual < melhor_custo:
                        melhor_custo = custo_atual
                        melhor_solucao = solucao_atual.copy()
                        
            temp_atual *= alfa
            
        return melhor_solucao, melhor_custo

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent
    caminho_instancia = BASE_DIR.parent / "data" / "instances" / "nug12.dat"
    if not caminho_instancia.exists():
        caminho_instancia = BASE_DIR / "data" / "instances" / "nug12.dat"
    
    print(f"Carregando instância: {caminho_instancia.name}...\n")
    
    sa_solver = SimulatedAnnealingQAP(caminho_instancia)
    
    inicio = time.perf_counter()
    melhor_sol, custo_final = sa_solver.executar_sa(
        temp_inicial=5000, 
        temp_final=0.01, 
        alfa=0.95, 
        iter_por_temp=150
    )
    fim = time.perf_counter()
    
    custo_otimo_gurobi = 578 
    gap = ((custo_final - custo_otimo_gurobi) / custo_otimo_gurobi) * 100
    
    print("==========================================")
    print(" RESULTADOS METAHEURÍSTICA (SIM. ANNEALING) ")
    print("==========================================")
    print(f"Custo Encontrado : {custo_final}")
    print(f"Alocação Final   : {melhor_sol}")
    print(f"Tempo Decorrido  : {fim - inicio:.4f} segundos")
    print(f"Gap p/ Exato     : {gap:.2f}%")
    print("==========================================")