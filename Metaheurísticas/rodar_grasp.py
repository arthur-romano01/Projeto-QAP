import glob
import os
import time
from datetime import datetime
from grasp import GRASP


OTIMOS_QAPLIB = {
    "nug12": 578,
    "nug15": 1150,
    "nug20": 2570,
    "nug25": 3744,
    "nug30": 6124,
    "chr25a": 3796,
    "tai20a": 703482,
    "tai30a": 1818146,
}


def ler_instancia(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        nums = list(map(int, f.read().split()))

    n = nums[0]
    distancias = [nums[1 + i * n : 1 + (i + 1) * n] for i in range(n)]
    fluxos = [nums[1 + n * n + i * n : 1 + n * n + (i + 1) * n] for i in range(n)]
    return n, distancias, fluxos


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pasta_instancias = os.path.join(base_dir, "..", "data", "instances")
    pasta_resultados = os.path.join(base_dir, "resultados")
    os.makedirs(pasta_resultados, exist_ok=True)

    arquivo_saida = os.path.join(pasta_resultados, "resultados_grasp.md")
    max_iteracoes = 150
    alfa = 0.35

    arquivos = sorted(
        f for f in glob.glob(os.path.join(pasta_instancias, "*"))
        if os.path.isfile(f) and not f.endswith((".md", ".py", ".txt"))
    )

    if not arquivos:
        print(f"Nenhuma instância encontrada em: {os.path.abspath(pasta_instancias)}")
    else:
        linhas_relatorio = [
            "# Resultados - GRASP\n",
            f"- **Última execução:** {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            f"- **Parâmetros:** `max_iteracoes={max_iteracoes}`, `alfa={alfa}`\n",
        ]

        for caminho in arquivos:
            arquivo_nome = os.path.basename(caminho)
            instancia_chave = os.path.splitext(arquivo_nome)[0]

            print(f"Carregando instância: {arquivo_nome}...\n")

            n, distancias, fluxos = ler_instancia(caminho)
            modelo = GRASP(distancias, fluxos)

            inicio = time.perf_counter()
            solucao, custo = modelo.executar(max_iteracoes=max_iteracoes, alfa=alfa)
            tempo_decorrido = time.perf_counter() - inicio

            otimo = OTIMOS_QAPLIB.get(instancia_chave)
            gap_str = f"{((custo - otimo) / otimo) * 100:.2f}%" if otimo else "N/A"

            bloco = (
                f"{'=' * 40}\n"
                f" RESULTADOS METAHEURÍSTICA (GRASP)\n"
                f"{'=' * 40}\n"
                f"Instância        : {arquivo_nome}\n"
                f"Custo Encontrado : {custo}\n"
                f"Alocação Final   : {solucao}\n"
                f"Tempo Decorrido  : {tempo_decorrido:.4f} segundos\n"
                f"Gap p/ Exato     : {gap_str}\n"
                f"{'=' * 40}"
            )

            print(bloco + "\n")
            linhas_relatorio.append(f"### Instância `{arquivo_nome}` (n={n})\n```text\n{bloco}\n```\n")

        with open(arquivo_saida, "w", encoding="utf-8") as f:
            f.write("\n".join(linhas_relatorio))

        print(f"Resultados salvos em: {arquivo_saida}")