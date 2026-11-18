import sys
import time
from algoritmos.grasp import GRASP
from algoritmos.sa import SimulatedAnnealing
from config import OTIMOS_QAPLIB, PARAMS_GRASP, PARAMS_SA
from leitor import ler_instancia, listar_instancias
from relatorio import calcular_gap, formatar_bloco, salvar_comparativo, salvar_individual


def rodar_modelo(classe, params, distancias, fluxos, titulo, arquivo, chave):
    t0 = time.perf_counter()
    solucao, custo = classe(distancias, fluxos).executar(**params)
    tempo = time.perf_counter() - t0
    gap = calcular_gap(custo, chave)
    bloco = formatar_bloco(titulo, arquivo, custo, solucao, tempo, gap)
    print(bloco + "\n")
    return custo, gap, f"{tempo:.3f}s", bloco


def main(filtro="todos"):
    reg_grasp, reg_sa, tabela = [], [], []

    for caminho in listar_instancias():
        chave = caminho.stem
        n, distancias, fluxos = ler_instancia(caminho)
        otimo = OTIMOS_QAPLIB.get(chave, "N/A")
        res = {}

        if filtro in ("todos", "grasp"):
            custo, gap, dt, bloco = rodar_modelo(GRASP, PARAMS_GRASP, distancias, fluxos, "GRASP", caminho.name, chave)
            reg_grasp.append({"arquivo": caminho.name, "n": n, "bloco": bloco})
            res["grasp"] = (custo, gap, dt)

        if filtro in ("todos", "sa"):
            custo, gap, dt, bloco = rodar_modelo(SimulatedAnnealing, PARAMS_SA, distancias, fluxos, "SIM. ANNEALING", caminho.name, chave)
            reg_sa.append({"arquivo": caminho.name, "n": n, "bloco": bloco})
            res["sa"] = (custo, gap, dt)

        if filtro == "todos":
            g, s = res["grasp"], res["sa"]
            tabela.append(f"| `{caminho.name}` | {n} | {otimo} | {g[0]} | {g[1]} | {g[2]} | {s[0]} | {s[1]} | {s[2]} |")

    if reg_grasp:
        salvar_individual("resultados_grasp.md", "GRASP", PARAMS_GRASP, reg_grasp)
    if reg_sa:
        salvar_individual("resultados_sa.md", "Simulated Annealing", PARAMS_SA, reg_sa)
    if tabela:
        salvar_comparativo(tabela)


if __name__ == "__main__":
    main(sys.argv[1].lower() if len(sys.argv) > 1 else "todos")