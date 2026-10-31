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

    dist = [valores[1 + i * n : 1 + (i + 1) * n] for i in range(n)]
    flow = [valores[1 + n**2 + i * n : 1 + n**2 + (i + 1) * n] for i in range(n)]

    return n, flow, dist


# Carregando dados (caminho robusto relativo ao arquivo)
BASE_DIR = Path(__file__).resolve().parent
caminho = BASE_DIR / "data" / "instances" / "nug12.dat"
n, flow, dist = read_instance(caminho)

# ==========================================
# 2. MODELO MATEMÁTICO NO GUROBI
#    (Formulação Quadrática de Koopmans-Beckmann)
# ==========================================
model = gp.Model("QAP_Quadratic")

# Obrigatório no Gurobi para aceitar a função quadrática não-convexa do QAP
model.Params.NonConvex = 2

# x[i, j] = 1 se a instalação i é alocada ao local j, 0 caso contrário
x = model.addVars(n, n, vtype=GRB.BINARY, name="x")

# - Cada instalação deve ir para exatamente 1 local
for i in range(n):
    model.addConstr(gp.quicksum(x[i, j] for j in range(n)) == 1, name=f"inst_{i}")

# - Cada local deve receber exatamente 1 instalação
for j in range(n):
    model.addConstr(gp.quicksum(x[i, j] for i in range(n)) == 1, name=f"loc_{j}")

# Função Objetivo Quadrática:
# min sum_{i,j,k,l} flow[i][k] * dist[j][l] * x[i,j] * x[k,l]
obj = gp.quicksum(
    flow[i][k] * dist[j][l] * x[i, j] * x[k, l]
    for i in range(n)
    for k in range(n)
    for j in range(n)
    for l in range(n)
)
model.setObjective(obj, GRB.MINIMIZE)

model.optimize()

# ==========================================
# 3. RESULTADOS
# ==========================================
if model.SolCount > 0:
    print(f"Custo Total Mínimo: {model.ObjVal:.0f}")

