from dataclasses import dataclass, field
from importlib import import_module
from pathlib import Path
from pkgutil import iter_modules


@dataclass(frozen=True)
class Modelo:
    chave: str
    nome: str
    rotulo: str
    classe: type
    params: dict = field(default_factory=dict)


def carregar_modelos():
    modelos = {}
    for modulo in iter_modules([str(Path(__file__).parent)]):
        modelo = getattr(import_module(f"algoritmos.{modulo.name}"), "MODELO", None)
        if modelo is None:
            continue
        if modelo.chave in modelos:
            raise ValueError(f"Chave de modelo duplicada: {modelo.chave}")
        modelos[modelo.chave] = modelo
    return modelos
