import numpy as np
import random
import time
from pathlib import Path

class SolucionadorQAP:
    def __init__(self, caminho_arquivo):
        self.n, self.fluxo, self.distancia = self._carregar_dados_numpy(caminho_arquivo)

    def _carregar_dados_numpy(self, caminho):
        with open(caminho, 'r') as arquivo:
            # Pega todos os valores ignorando quebras de linha e espaços
            valores = np.array([int(x) for x in arquivo.read().split()])
        
        n = valores[0]
        distancia = valores[1 : 1 + n*n].reshape((n, n))
        fluxo = valores[1 + n*n : 1 + 2*n*n].reshape((n, n))
        
        return n, fluxo, distancia

    def calcular_custo(self, solucao):
        # np.ix_ simula a troca de posições (linhas e colunas) simultaneamente
        distancia_permutada = self.distancia[np.ix_(solucao, solucao)]
        return np.sum(self.fluxo * distancia_permutada)

    def executar_tabu(self, max_iteracoes=1000, tamanho_lista_tabu=12):
        """Executa a Busca Tabu com estrutura de vizinhança 2-opt."""
        solucao_atual = list(range(self.n))
        random.shuffle(solucao_atual)
        
        melhor_solucao_global = solucao_atual.copy()
        melhor_custo_global = self.calcular_custo(melhor_solucao_global)
        
        memoria_tabu = np.zeros((self.n, self.n), dtype=int)
        
        for it in range(max_iteracoes):
            vizinhos = []
            
            for i in range(self.n):
                for j in range(i + 1, self.n):
                    vizinho = solucao_atual.copy()
                    vizinho[i], vizinho[j] = vizinho[j], vizinho[i]
                    custo_viz = self.calcular_custo(vizinho)
                    vizinhos.append((custo_viz, vizinho, i, j))
            
            vizinhos.sort(key=lambda x: x[0])
            
            for custo_viz, viz, i, j in vizinhos:
                movimento_proibido = memoria_tabu[i][j] > it
                criterio_aspiracao = custo_viz < melhor_custo_global
                
                if not movimento_proibido or criterio_aspiracao:
                    solucao_atual = viz
                    
                    memoria_tabu[i][j] = it + tamanho_lista_tabu
                    memoria_tabu[j][i] = it + tamanho_lista_tabu
                    
                    if custo_viz < melhor_custo_global:
                        melhor_custo_global = custo_viz
                        melhor_solucao_global = viz.copy()
                        
                    break
                    
        return melhor_solucao_global, melhor_custo_global


if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent
    caminho_instancia = BASE_DIR / "data" / "instances" / "nug12.dat"
    
    print(f"Carregando instância: {caminho_instancia.name}...\n")
    
    qap_solver = SolucionadorQAP(caminho_instancia)
    
    inicio = time.perf_counter()
    melhor_sol, custo_final = qap_solver.executar_tabu(max_iteracoes=800, tamanho_lista_tabu=10)
    fim = time.perf_counter()
    
    custo_otimo_gurobi = 578 
    gap = ((custo_final - custo_otimo_gurobi) / custo_otimo_gurobi) * 100
    
    print("==========================================")
    print("    RESULTADOS METAHEURÍSTICA (TABU)      ")
    print("==========================================")
    print(f"Custo Encontrado : {custo_final}")
    print(f"Alocação Final   : {melhor_sol}")
    print(f"Tempo Decorrido  : {fim - inicio:.4f} segundos")
    print(f"Gap p/ Exato     : {gap:.2f}%")
    print("==========================================")