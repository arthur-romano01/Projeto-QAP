from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
PASTA_INSTANCIAS = ROOT_DIR / "data" / "instances"
PASTA_RESULTADOS = ROOT_DIR / "results"

OTIMOS_QAPLIB = {
    "nug12": 578,
    "nug14": 1014,
    "nug15": 1150,
    "nug16a": 1610,
    "nug17": 1732,
    "nug18": 1930,
    "nug20": 2570,
    "nug22": 3596,
    "nug25": 3744,
    "nug30": 6124,
    "chr12a": 9552,
    "chr15a": 9896,
    "chr20a": 2192,
    "chr25a": 3796,
    "esc16a": 68,
    "had12": 1652,
    "had14": 2724,
    "had16": 3720,
    "had20": 6922,
    "rou12": 235528,
    "rou15": 354210,
    "rou20": 725522,
    "scr12": 31410,
    "scr15": 51140,
    "scr20": 110030,
    "tai12a": 224416,
    "tai15a": 388214,
    "tai20a": 703482,
    "tai25a": 1167256,
    "tai30a": 1818146,
}


def listar_instancias():
    return sorted(
        p for p in PASTA_INSTANCIAS.iterdir()
        if p.is_file() and p.suffix not in {".md", ".py", ".txt"}
    )


def ler_instancia(caminho):
    nums = list(map(int, Path(caminho).read_text(encoding="utf-8").split()))
    n = nums[0]
    distancias = [nums[1 + i * n : 1 + (i + 1) * n] for i in range(n)]
    fluxos = [nums[1 + n * n + i * n : 1 + n * n + (i + 1) * n] for i in range(n)]
    return n, distancias, fluxos


def calcular_gap(custo, chave_instancia):
    otimo = OTIMOS_QAPLIB.get(chave_instancia)
    if not otimo:
        return "N/A"
    return f"{((custo - otimo) / otimo) * 100:.2f}%"


def salvar_relatorio_individual(nome_arquivo, titulo, info_params, registros):
    PASTA_RESULTADOS.mkdir(parents=True, exist_ok=True)
    linhas = [
        f"# Resultados - {titulo}\n",
        f"- **Última execução:** {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        f"- **Parâmetros:** {info_params}\n",
    ]
    for reg in registros:
        linhas.append(f"### Instância `{reg['arquivo']}` (n={reg['n']})\n```text\n{reg['bloco']}\n```\n")

    (PASTA_RESULTADOS / nome_arquivo).write_text("\n".join(linhas), encoding="utf-8")


def salvar_comparativo(tabela_linhas):
    PASTA_RESULTADOS.mkdir(parents=True, exist_ok=True)
    cabecalho = [
        "# Comparativo Geral - Metaheurísticas\n",
        f"- **Atualizado em:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n",
        "| Instância | n | Ótimo | GRASP Custo | GRASP Gap | GRASP Tempo | SA Custo | SA Gap | SA Tempo |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
    ]
    (PASTA_RESULTADOS / "comparativo_geral.md").write_text(
        "\n".join(cabecalho + tabela_linhas) + "\n", encoding="utf-8"
    )