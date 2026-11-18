from pathlib import Path
from config import PASTA_INSTANCIAS


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