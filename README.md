# Projeto QAP - Problema de Atribuição Quadrática

Esqueleto do projeto para resolução do QAP via modelo matemático exato com Gurobi.

## Estrutura do Projeto

```text
Projeto-QAP/
│
├── data/
│   ├── instances/        # Coloque seus arquivos de dados aqui
│   └── solutions/        # Pasta de saída para salvar os resultados
│
├── src/
│   ├── __init__.py
│   ├── reader.py         # Leitura da instância (n, fluxo, distância)
│   ├── model.py          # Modelagem matemática e chamada do Gurobi
│   └── utils.py          # Funções auxiliares (exibição e exportação)
│
├── main.py               # Fluxo principal de execução
├── requirements.txt      # Bibliotecas necessárias
└── README.md
```
