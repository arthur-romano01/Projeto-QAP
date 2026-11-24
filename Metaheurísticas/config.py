from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
PASTA_INSTANCIAS = ROOT_DIR / "data" / "instances"
PASTA_RESULTADOS = ROOT_DIR / "results"

OTIMOS_QAPLIB = {
    "nug12": 578,
    "chr15a": 9896,
    "had18": 5358,
    "els19": 17212548,
    "rou20": 725522,
    "bur26a": 5426670,
    "nug30": 6124,
    "kra30a": 88900,
    "ste36a": 9526,
    "sko42": 15812,
}