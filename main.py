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

# Carregando dados
caminho = "data/instances/nug12.dat"
n, flow, dist = read_instance(caminho)

# ==========================================
# 2. MODELO MATEMÁTICO NO GUROBI
# ==========================================
model = gp.Model("QAP")

# Obrigatório no Gurobi para aceitar a função quadrática do QAP
model.Params.NonConvex = 2

x = model.addVars(n, n, vtype=GRB.BINARY, name="x")

# - Cada instalação deve ir para exatamente 1 local
for i in range(n):
    model.addConstr(gp.quicksum(x[i, j] for j in range(n)) == 1)

# - Cada local deve receber exatamente 1 instalação
for j in range(n):
    model.addConstr(gp.quicksum(x[i, j] for i in range(n)) == 1)

obj = gp.quicksum(flow[i][k] * dist[j][l] * x[i, j] * x[k, l] for i in range(n) for k in range(n) for j in range(n) for l in range(n))
model.setObjective(obj, GRB.MINIMIZE)

model.optimize()


# ==========================================
# 3. RESULTADOS
# ==========================================
if model.SolCount > 0:
    print(f"Custo Total Mínimo: {model.ObjVal:.0f}")
