from pathlib import Path
import gurobipy as gp
from gurobipy import GRB

# ==========================================
# 1. DADOS DA INSTÂNCIA
# ==========================================
def read_instance(caminho):
    with open(caminho) as file:
        dados = file.read().split()
        valores = [int(x) for x in dados]
    n = valores[0]

    dist = [valores[1+i*n: 1 + (i+1)*n] for i in range(n)]
    flow = [valores[1+n**2 + i*n: 1 + n**2 + (i+1)*n] for i in range(n)]

    return n, flow, dist   

# Carregando dados (caminho robusto relativo ao arquivo)
BASE_DIR = Path(__file__).resolve().parent
caminho = BASE_DIR / "data" / "instances" / "nug12.dat"
n, flow, dist = read_instance(caminho)

# ==========================================
# 2. MODELO MATEMÁTICO NO GUROBI
#    (Linearização de Kaufman e Broeckx)
# ==========================================
model = gp.Model("QAP_Kaufman_Broeckx")

# Variáveis de decisão:
# x[i, j] = 1 se a instalação i é alocada ao local j, 0 caso contrário
x = model.addVars(n, n, vtype=GRB.BINARY, name="x")

# w[i, j] >= 0 representa o custo de interação da instalação i no local j:
# w[i, j] = x[i, j] * sum_{k, l} (flow[i][k] * dist[j][l] * x[k, l])
w = model.addVars(n, n, lb=0.0, vtype=GRB.CONTINUOUS, name="w")

# Restrições de atribuição:
# 1. Cada instalação deve ir para exatamente 1 local
for i in range(n):
    model.addConstr(gp.quicksum(x[i, j] for j in range(n)) == 1, name=f"inst_{i}")

# 2. Cada local deve receber exatamente 1 instalação
for j in range(n):
    model.addConstr(gp.quicksum(x[i, j] for i in range(n)) == 1, name=f"loc_{j}")

# 3. Restrições de linearização de Kaufman e Broeckx (Big-M):
# Para cada par (i, j), calculamos o limitante superior M[i, j]
for i in range(n):
    for j in range(n):
        M_ij = sum(flow[i][k] * dist[j][l] for k in range(n) for l in range(n))
        custo_interacao = gp.quicksum(
            flow[i][k] * dist[j][l] * x[k, l] for k in range(n) for l in range(n)
        )
        model.addConstr(
            w[i, j] >= custo_interacao - M_ij * (1 - x[i, j]),
            name=f"kb_{i}_{j}"
        )

# Função Objetivo Linearizada: minimizar a soma de w[i, j]
obj = gp.quicksum(w[i, j] for i in range(n) for j in range(n))
model.setObjective(obj, GRB.MINIMIZE)

model.optimize()


# ==========================================
# 3. RESULTADOS
# ==========================================
if model.SolCount > 0:
    print(f"Custo Total Mínimo: {model.ObjVal:.0f}")
