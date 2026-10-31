# Projeto QAP - Problema de Atribuição Quadrática

Projeto desenvolvido para a disciplina de **Pesquisa Operacional (UNIFESP)** com o objetivo de modelar e resolver o **Problema de Atribuição Quadrática (QAP - *Quadratic Assignment Problem*)** utilizando a API Python do **Gurobi Optimizer** (`gurobipy`).

---

## 📁 Estrutura do Projeto

O projeto é estruturado de forma direta e sem dependências complexas:

```text
Projeto-QAP/
│
├── data/
│   ├── instances/
│   │   └── nug12.dat      # Instância clássica de benchmark da QAPLIB (n = 12)
│   └── solutions/         # Pasta destinada a saídas/relatórios
│
├── main.py                # Script principal: leitura de dados, modelo e execução do solver
├── requirements.txt       # Dependências do projeto (gurobipy)
└── README.md              # Documentação do projeto
```

---

## 🧮 Modelo Matemático (Formulação de Koopmans-Beckmann)

O modelo atual implementado no arquivo [`main.py`] é a formulação **quadrática exata**:

### Conjuntos e Parâmetros
* $n$: Quantidade de instalações e locais disponíveis.
* $i, k \in \{0, \dots, n-1\}$: Índices das instalações.
* $j, l \in \{0, \dots, n-1\}$: Índices dos locais.
* $F_{ik}$: Fluxo de materiais/itens da instalação $i$ para a instalação $k$.
* $D_{jl}$: Distância física entre o local $j$ e o local $l$.

### Variáveis de Decisão
$$x_{ij} = \begin{cases} 1, & \text{se a instalação } i \text{ for alocada no local } j \\ 0, & \text{caso contrário} \end{cases}$$

### Função Objetivo
Minimizar o custo total de transporte (fluxo $\times$ distância entre todos os pares):
$$\min \sum_{i=0}^{n-1} \sum_{j=0}^{n-1} \sum_{k=0}^{n-1} \sum_{l=0}^{n-1} F_{ik} \cdot D_{jl} \cdot x_{ij} \cdot x_{kl}$$

### Restrições
1. **Cada instalação deve ser alocada a exatamente um local:**
   $$\sum_{j=0}^{n-1} x_{ij} = 1 \quad \forall i \in \{0, \dots, n-1\}$$

2. **Cada local deve receber exatamente uma instalação:**
   $$\sum_{i=0}^{n-1} x_{ij} = 1 \quad \forall j \in \{0, \dots, n-1\}$$

3. **Natureza binária das variáveis:**
   $$x_{ij} \in \{0, 1\} \quad \forall i, j$$

> **Nota técnica:** A função objetivo possui termos quadráticos não-convexos ($x_{ij} \cdot x_{kl}$). Para resolvê-la diretamente de forma exata, é ativado o parâmetro `model.Params.NonConvex = 2`, que instrui o Gurobi a aplicar Branch-and-Bound.

---

## 🚀 Como Executar

### 1. Instalar dependências
Certifique-se de ter o Python 3.9+ instalado e uma licença válida do Gurobi (ex: acadêmica):
```bash
pip install -r requirements.txt
```

### 2. Executar o modelo
```bash
python main.py
```

---

