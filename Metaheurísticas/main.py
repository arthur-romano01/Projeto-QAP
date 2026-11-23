import sys
import time
from algoritmos.registro import carregar_modelos
from benchmark import aquecer_compilacao
from config import OTIMOS_QAPLIB
from leitor import ler_instancia, listar_instancias
from relatorio import calcular_gap, formatar_bloco, salvar_comparativo, salvar_individual


def rodar_modelo(modelo, distancias, fluxos, arquivo, chave):
    t0 = time.perf_counter()
    solucao, custo = modelo.classe(distancias, fluxos).executar(**modelo.params)
    tempo = time.perf_counter() - t0
    gap = calcular_gap(custo, chave)
    bloco = formatar_bloco(modelo.nome.upper(), arquivo, custo, solucao, tempo, gap)
    print(bloco + "\n")
    return custo, gap, f"{tempo:.3f}s", bloco


def main(filtro="todos"):
    modelos = carregar_modelos()
    if filtro != "todos" and filtro not in modelos:
        sys.exit(f"Modelo desconhecido: {filtro}. Opções: todos, {', '.join(modelos)}")

    selecionados = [modelos[chave] for chave in sorted(modelos)] if filtro == "todos" else [modelos[filtro]]
    aquecer_compilacao()
    registros = {modelo.chave: [] for modelo in selecionados}
    tabela = []

    for caminho in listar_instancias():
        chave = caminho.stem
        n, distancias, fluxos = ler_instancia(caminho)
        celulas = [f"`{caminho.name}`", n, OTIMOS_QAPLIB.get(chave, "N/A")]

        for modelo in selecionados:
            custo, gap, dt, bloco = rodar_modelo(modelo, distancias, fluxos, caminho.name, chave)
            registros[modelo.chave].append({"arquivo": caminho.name, "n": n, "bloco": bloco})
            celulas += [custo, gap, dt]

        tabela.append(celulas)

    for modelo in selecionados:
        salvar_individual(f"resultados_{modelo.chave}.md", modelo.nome, modelo.params, registros[modelo.chave])

    if filtro == "todos":
        salvar_comparativo([modelo.rotulo for modelo in selecionados], tabela)


if __name__ == "__main__":
    main(sys.argv[1].lower() if len(sys.argv) > 1 else "todos")
