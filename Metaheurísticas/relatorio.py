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


def salvar_comparativo(linhas_tabela):
    PASTA_RESULTADOS.mkdir(parents=True, exist_ok=True)
    cabecalho = [
        "# Comparativo Geral - Metaheurísticas\n",
        f"- **Atualizado em:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n",
        "| Instância | n | Ótimo | GRASP Custo | GRASP Gap | GRASP Tempo | SA Custo | SA Gap | SA Tempo |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
    ]
    (PASTA_RESULTADOS / "comparativo_geral.md").write_text(
        "\n".join(cabecalho + linhas_tabela) + "\n", encoding="utf-8"
    )