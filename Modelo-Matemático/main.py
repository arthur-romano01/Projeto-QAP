import argparse
from pathlib import Path
import gurobipy as gp
from gurobipy import GRB


def read_instance(caminho):
    with open(caminho) as file:
        dados = file.read().split()
        valores = [int(x) for x in dados]
    n = valores[0]
    dist = [valores[1 + i * n : 1 + (i + 1) * n] for i in range(n)]
    flow = [valores[1 + n**2 + i * n : 1 + n**2 + (i + 1) * n] for i in range(n)]
    return n, flow, dist


parser = argparse.ArgumentParser()
parser.add_argument("instancia", nargs="?", default="nug12")
parser.add_argument("--tempo-limite", type=float)
args = parser.parse_args()

BASE_DIR = Path(__file__).resolve().parent
caminho = BASE_DIR.parent / "data" / "instances" / f"{args.instancia}.dat"
if not caminho.exists():
    caminho = BASE_DIR / "data" / "instances" / f"{args.instancia}.dat"
n, flow, dist = read_instance(caminho)

# Modelo MILP: Linearização de Kaufman e Broeckx
model = gp.Model("QAP_Kaufman_Broeckx")
if args.tempo_limite is not None:
    model.Params.TimeLimit = args.tempo_limite

x = model.addVars(n, n, vtype=GRB.BINARY, name="x")
w = model.addVars(n, n, lb=0.0, vtype=GRB.CONTINUOUS, name="w")

# Restrições de atribuição
for i in range(n):
    model.addConstr(gp.quicksum(x[i, j] for j in range(n)) == 1, name=f"inst_{i}")

for j in range(n):
    model.addConstr(gp.quicksum(x[i, j] for i in range(n)) == 1, name=f"loc_{j}")

# Restrições de linearização (Big-M)
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

# Função objetivo
obj = gp.quicksum(w[i, j] for i in range(n) for j in range(n))
model.setObjective(obj, GRB.MINIMIZE)

model.optimize()

if model.SolCount > 0:
    print(f"Custo Total Mínimo: {model.ObjVal:.0f}")
    print(f"Limitante Inferior: {model.ObjBound:.0f} (gap {100 * model.MIPGap:.2f}%)")
