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

# Modelo MIQP: Formulação Quadrática de Koopmans-Beckmann
model = gp.Model("QAP_Quadratic")
if args.tempo_limite is not None:
    model.Params.TimeLimit = args.tempo_limite
model.Params.NonConvex = 2

x = model.addVars(n, n, vtype=GRB.BINARY, name="x")

# Restrições de atribuição
for i in range(n):
    model.addConstr(gp.quicksum(x[i, j] for j in range(n)) == 1, name=f"inst_{i}")

for j in range(n):
    model.addConstr(gp.quicksum(x[i, j] for i in range(n)) == 1, name=f"loc_{j}")

# Função objetivo quadrática
obj = gp.quicksum(
    flow[i][k] * dist[j][l] * x[i, j] * x[k, l]
    for i in range(n)
    for k in range(n)
    for j in range(n)
    for l in range(n)
)
model.setObjective(obj, GRB.MINIMIZE)

model.optimize()

if model.SolCount > 0:
    print(f"Custo Total Mínimo: {model.ObjVal:.0f}")
    print(f"Limitante Inferior: {model.ObjBound:.0f} (gap {100 * model.MIPGap:.2f}%)")
