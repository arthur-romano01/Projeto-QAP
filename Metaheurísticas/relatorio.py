from datetime import datetime
from config import OTIMOS_QAPLIB, PASTA_RESULTADOS


def calcular_gap(custo, chave):
    otimo = OTIMOS_QAPLIB.get(chave)
    return f"{((custo - otimo) / otimo) * 100:.2f}%" if otimo else "N/A"


def formatar_bloco(titulo, arquivo, custo, solucao, tempo, gap):
    return (
        f"{'=' * 42}\n"
        f" RESULTADOS METAHEURÍSTICA ({titulo})\n"
        f"{'=' * 42}\n"
        f"Instância        : {arquivo}\n"
        f"Custo Encontrado : {custo}\n"
        f"Alocação Final   : {solucao}\n"
        f"Tempo Decorrido  : {tempo:.4f} segundos\n"
        f"Gap p/ Exato     : {gap}\n"
        f"{'=' * 42}"
    )


def salvar_individual(nome_arquivo, titulo, params, registros):
    PASTA_RESULTADOS.mkdir(parents=True, exist_ok=True)
    linhas = [
        f"# Resultados - {titulo}\n",
        f"- **Última execução:** {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        f"- **Parâmetros:** `{params}`\n",
    ]
    for reg in registros:
        linhas.append(f"### Instância `{reg['arquivo']}` (n={reg['n']})\n```text\n{reg['bloco']}\n```\n")

    (PASTA_RESULTADOS / nome_arquivo).write_text("\n".join(linhas), encoding="utf-8")


def _linha_tabela(celulas):
    return "| " + " | ".join(str(celula) for celula in celulas) + " |"


def salvar_comparativo(rotulos, linhas_tabela):
    PASTA_RESULTADOS.mkdir(parents=True, exist_ok=True)
    colunas = ["Instância", "n", "Ótimo"]
    for rotulo in rotulos:
        colunas += [f"{rotulo} Custo", f"{rotulo} Gap", f"{rotulo} Tempo"]

    cabecalho = [
        "# Comparativo Geral - Metaheurísticas\n",
        f"- **Atualizado em:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n",
        _linha_tabela(colunas),
        _linha_tabela([":---"] + [":---:"] * (len(colunas) - 1)),
    ]
    linhas = cabecalho + [_linha_tabela(celulas) for celulas in linhas_tabela]
    (PASTA_RESULTADOS / "comparativo_geral.md").write_text("\n".join(linhas) + "\n", encoding="utf-8")