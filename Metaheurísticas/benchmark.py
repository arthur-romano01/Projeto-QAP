import argparse
import csv
import os
import random
import time
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from pathlib import Path
from statistics import mean, stdev

from algoritmos.registro import carregar_modelos
from config import OTIMOS_QAPLIB, PASTA_RESULTADOS
from leitor import ler_instancia, listar_instancias

COLUNAS = ["modelo", "instancia", "n", "semente", "orcamento", "avaliacoes", "custo", "otimo", "gap_pct", "tempo_s"]


def aquecer_compilacao():
    distancias = [[0, 1, 2, 3], [1, 0, 1, 2], [2, 1, 0, 1], [3, 2, 1, 0]]
    fluxos = [[0, 3, 1, 2], [3, 0, 2, 1], [1, 2, 0, 3], [2, 1, 3, 0]]
    for modelo in carregar_modelos().values():
        modelo.classe(distancias, fluxos).executar(**modelo.params, orcamento=12)


def executar_tarefa(tarefa):
    chave_modelo, caminho, semente, varreduras = tarefa
    modelo = carregar_modelos()[chave_modelo]
    n, distancias, fluxos = ler_instancia(caminho)
    orcamento = varreduras * n * (n - 1) // 2

    random.seed(semente)
    algoritmo = modelo.classe(distancias, fluxos)
    inicio = time.perf_counter()
    _, custo = algoritmo.executar(**modelo.params, orcamento=orcamento)
    tempo = time.perf_counter() - inicio

    instancia = Path(caminho).stem
    otimo = OTIMOS_QAPLIB[instancia]
    return {
        "modelo": chave_modelo,
        "instancia": instancia,
        "n": n,
        "semente": semente,
        "orcamento": orcamento,
        "avaliacoes": algoritmo.avaliacoes,
        "custo": int(custo),
        "otimo": otimo,
        "gap_pct": round(100 * (int(custo) - otimo) / otimo, 4),
        "tempo_s": round(tempo, 4),
    }


def salvar_execucoes(caminho, execucoes):
    with caminho.open("w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=COLUNAS)
        escritor.writeheader()
        escritor.writerows(execucoes)


def linha_resumo(rotulo, linhas):
    gaps = [linha["gap_pct"] for linha in linhas]
    desvio = stdev(gaps) if len(gaps) > 1 else 0.0
    acertos = sum(linha["custo"] == linha["otimo"] for linha in linhas)
    tempo = mean(linha["tempo_s"] for linha in linhas)
    return (
        f"| {rotulo} | {mean(gaps):.2f} | {desvio:.2f} | {min(gaps):.2f} | {max(gaps):.2f} "
        f"| {acertos}/{len(linhas)} | {tempo:.3f} |"
    )


def salvar_resumo(caminho, execucoes, args, modelos, duracao):
    por_instancia = defaultdict(lambda: defaultdict(list))
    for linha in execucoes:
        por_instancia[(linha["n"], linha["instancia"])][linha["modelo"]].append(linha)

    linhas = [
        "# Benchmark semeado - Metaheurísticas\n",
        f"- **Gerado em:** {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        f"- **Execuções por modelo e instância:** {args.execucoes}",
        f"- **Sementes:** {args.semente} a {args.semente + args.execucoes - 1}",
        f"- **Orçamento:** {args.varreduras} varreduras da vizinhança, ou {args.varreduras} · n(n-1)/2 avaliações de troca",
        f"- **Duração total:** {duracao:.0f} s com {args.processos} processos",
    ]
    linhas += [f"- **Parâmetros de {modelo.nome}:** `{modelo.params}`" for modelo in modelos]

    cabecalho = "| Modelo | Gap médio (%) | Desvio | Melhor | Pior | Ótimo atingido | Tempo médio (s) |"
    separador = "| :--- | :---: | :---: | :---: | :---: | :---: | :---: |"
    for (n, instancia), por_modelo in sorted(por_instancia.items()):
        linhas += [f"\n## `{instancia}` (n={n})\n", cabecalho, separador]
        linhas += [linha_resumo(modelo.rotulo, por_modelo[modelo.chave]) for modelo in modelos]

    caminho.write_text("\n".join(linhas) + "\n", encoding="utf-8")


def ler_argumentos(modelos):
    parser = argparse.ArgumentParser(description="Benchmark semeado com orçamento igual para todas as metaheurísticas.")
    parser.add_argument("--execucoes", type=int, default=30)
    parser.add_argument("--varreduras", type=int, default=800)
    parser.add_argument("--semente", type=int, default=0)
    parser.add_argument("--processos", type=int, default=max(1, (os.cpu_count() or 2) // 2))
    parser.add_argument("--modelos", nargs="+", choices=sorted(modelos), default=sorted(modelos))
    parser.add_argument("--instancias", nargs="+")
    parser.add_argument("--saida", type=Path, default=PASTA_RESULTADOS / "benchmark")
    return parser.parse_args()


def main():
    modelos = carregar_modelos()
    args = ler_argumentos(modelos)

    caminhos = listar_instancias()
    if args.instancias:
        caminhos = [caminho for caminho in caminhos if caminho.stem in args.instancias]

    sementes = range(args.semente, args.semente + args.execucoes)
    tarefas = [
        (chave, str(caminho), semente, args.varreduras)
        for chave in args.modelos
        for caminho in caminhos
        for semente in sementes
    ]

    inicio = time.perf_counter()
    with ProcessPoolExecutor(max_workers=args.processos, initializer=aquecer_compilacao) as executor:
        execucoes = list(executor.map(executar_tarefa, tarefas))
    duracao = time.perf_counter() - inicio

    execucoes.sort(key=lambda linha: (linha["n"], linha["instancia"], linha["modelo"], linha["semente"]))
    args.saida.mkdir(parents=True, exist_ok=True)
    salvar_execucoes(args.saida / "execucoes.csv", execucoes)
    salvar_resumo(args.saida / "resumo.md", execucoes, args, [modelos[chave] for chave in args.modelos], duracao)
    print(f"{len(execucoes)} execuções em {duracao:.0f} s. Resultados em {args.saida}")


if __name__ == "__main__":
    main()
