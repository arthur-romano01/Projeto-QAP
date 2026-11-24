# Projeto QAP - Problema de Atribuição Quadrática

Projeto desenvolvido para a disciplina de **Pesquisa Operacional (UNIFESP)** com o objetivo de modelar e resolver o **Problema de Atribuição Quadrática (QAP - *Quadratic Assignment Problem*)** utilizando tanto métodos exatos com o **Gurobi Optimizer** (`gurobipy`) quanto métodos aproximados baseados em **Metaheurísticas**.

---

## 📁 Estrutura do Projeto

O repositório separa os métodos exatos (programação matemática) dos métodos aproximados (metaheurísticas), com as instâncias e os resultados compartilhados:

```text
Projeto-QAP/
│
├── data/
│   └── instances/             # 10 instâncias da QAPLIB (nug12 a sko42)
│
├── Metaheurísticas/
│   ├── algoritmos/
│   │   ├── grasp.py           # GRASP: construção gulosa aleatorizada + busca local
│   │   ├── sa.py              # Simulated Annealing
│   │   ├── busca_tabu.py      # Busca Tabu
│   │   ├── delta.py           # Avaliação de trocas compilada com Numba
│   │   └── registro.py        # Descoberta automática dos modelos
│   ├── main.py                # Uma execução de cada modelo em todas as instâncias
│   ├── benchmark.py           # Benchmark semeado com orçamento igual por modelo
│   ├── config.py              # Caminhos e ótimos conhecidos da QAPLIB
│   ├── leitor.py              # Leitura das instâncias
│   └── relatorio.py           # Geração dos relatórios em Markdown
│
├── Modelo-Matemático/
│   ├── main.py                # Modelo exato linearizado (Kaufman & Broeckx - MILP)
│   ├── qap_quadratic.py       # Modelo exato quadrático (Koopmans-Beckmann - MIQP)
│   └── requirements.txt       # Dependências específicas do módulo
│
├── results/                   # Comparativo geral, resultados por modelo e benchmark
├── docs/licenca-gurobi-wls.md # Como obter a licença acadêmica do Gurobi
├── requirements.txt           # Dependências (gurobipy, numpy, numba)
└── README.md
```

---

## 🧮 Modelos Matemáticos Exatos (`Modelo-Matemático/`)

O **QAP** clássico busca atribuir $n$ instalações a $n$ locais de modo a minimizar o custo total associado ao fluxo de materiais multiplicado pela distância física entre os locais.

### 1. Formulação Quadrática Original (Koopmans-Beckmann)
Disponível em [`Modelo-Matemático/qap_quadratic.py`](Modelo-Matemático/qap_quadratic.py):

$$\min \sum_{i=0}^{n-1} \sum_{j=0}^{n-1} \sum_{k=0}^{n-1} \sum_{l=0}^{n-1} F_{ik} \cdot D_{jl} \cdot x_{ij} \cdot x_{kl}$$

Sujeito a:
* $\sum_{j=0}^{n-1} x_{ij} = 1 \quad \forall i \in \{0, \dots, n-1\}$ (cada instalação vai para um único local)
* $\sum_{i=0}^{n-1} x_{ij} = 1 \quad \forall j \in \{0, \dots, n-1\}$ (cada local recebe uma única instalação)
* $x_{ij} \in \{0, 1\} \quad \forall i, j$

> **Nota técnica:** Utiliza o parâmetro `model.Params.NonConvex = 2` no Gurobi para tratar os termos quadráticos não-convexos.

### 2. Linearização de Kaufman e Broeckx (1978)
Disponível em [`Modelo-Matemático/main.py`](Modelo-Matemático/main.py):

Transforma o QAP em uma **Programação Linear Inteira Mista (MILP)** compacta através da técnica de restrições **Big-M**:
* Introduz variáveis contínuas $w_{ij} \ge 0$ representando o custo de interação da instalação $i$ no local $j$.
* Adiciona apenas $n^2$ variáveis contínuas e $n^2$ restrições lineares (em contraste com $O(n^4)$ na formulação de Lawler).

$$\min \sum_{i=0}^{n-1} \sum_{j=0}^{n-1} w_{ij}$$

Sujeito às restrições de atribuição padrão e às restrições Big-M de acoplamento:
$$w_{ij} \ge \sum_{k=0}^{n-1} \sum_{l=0}^{n-1} F_{ik} D_{jl} x_{kl} - M_{ij}(1 - x_{ij}) \quad \forall i, j$$

onde $M_{ij} = \sum_{k=0}^{n-1} \sum_{l=0}^{n-1} F_{ik} D_{jl}$.

---

## ⚡ Metaheurísticas (`Metaheurísticas/`)

Para instâncias maiores, em que os métodos exatos se tornam proibitivos, foram implementadas três metaheurísticas sobre a mesma representação: uma permutação de tamanho $n$ com vizinhança de trocas 2-opt (troca de pares de instalações).

### 1. GRASP (`algoritmos/grasp.py`)
* **Construção:** Gulosa aleatorizada. A cada passo calcula o custo incremental de todos os pares (instalação, local) livres e sorteia um da Lista Restrita de Candidatos (RCL), formada pelos pares com custo até $c_{min} + \alpha (c_{max} - c_{min})$.
* **Busca Local:** Primeira melhora na vizinhança 2-opt até atingir um ótimo local.
* **Multi-start:** Repete construção + busca local e guarda a melhor solução.

### 2. Simulated Annealing (`algoritmos/sa.py`)
* **Perturbação:** Movimentos aleatórios 2-opt.
* **Critério de Aceitação:** Critério de Metropolis ($e^{-\Delta / T}$) para aceitar soluções de piora com probabilidade controlada, escapando de ótimos locais.
* **Esquema de Resfriamento:** Resfriamento geométrico progressivo ($T_{novo} = \alpha \cdot T_{atual}$).

### 3. Busca Tabu (`algoritmos/busca_tabu.py`)
* **Movimento:** Melhor troca não tabu da vizinhança 2-opt a cada iteração.
* **Memória Tabu:** Matriz que proíbe pares recém-trocados por um número fixo de iterações para prevenir ciclos.
* **Critério de Aspiração:** Permite movimentos tabu que produzam uma solução estritamente melhor que a melhor global.

### Avaliação de trocas com Numba (`algoritmos/delta.py`)
Nenhuma metaheurística recalcula o custo $O(n^2)$ a cada vizinho. A variação de custo $\Delta$ de uma troca é calculada em $O(n)$, e a Busca Tabu mantém a matriz com os $\Delta$ de todas as trocas, atualizada de forma incremental após cada movimento (Taillard). Essas rotinas são compiladas com `@njit` do Numba, com cache em disco.

### Benchmark (`benchmark.py`)
Para comparar os modelos de forma justa, cada um recebe o mesmo orçamento de avaliações de troca (por padrão, 800 varreduras da vizinhança, ou $800 \cdot n(n-1)/2$ avaliações) e é executado com 30 sementes por instância, em paralelo.

---

## 🚀 Como Executar

### 1. Instalar dependências
Com Python 3.10+ (testado no 3.14):
```bash
pip install -r requirements.txt
```

### 2. Modelos exatos
A partir da raiz do repositório. Por padrão resolvem `nug12`; passe outra instância de `data/instances/` e, se quiser, um limite de tempo em segundos:
```bash
python Modelo-Matemático/main.py                              # Kaufman & Broeckx (MILP)
python Modelo-Matemático/qap_quadratic.py chr15a --tempo-limite 600   # Koopmans-Beckmann (MIQP)
```
Instâncias acima de $n = 14$ (quadrático) ou $n = 31$ (linearizado) exigem a licença acadêmica: veja [`docs/licenca-gurobi-wls.md`](docs/licenca-gurobi-wls.md).

### 3. Metaheurísticas
Uma execução de cada modelo em todas as instâncias. Gera `results/comparativo_geral.md` e `results/resultados_<modelo>.md`:
```bash
python Metaheurísticas/main.py          # todos os modelos
python Metaheurísticas/main.py tabu     # só um: grasp, sa ou tabu
```

Benchmark semeado com orçamento igual. Gera `results/benchmark/execucoes.csv` e `results/benchmark/resumo.md`:
```bash
python Metaheurísticas/benchmark.py
python Metaheurísticas/benchmark.py --execucoes 10 --modelos grasp tabu --instancias nug12 chr15a
```
Opções: `--execucoes` (30), `--varreduras` (800), `--semente` (0), `--processos` (metade dos núcleos), `--modelos`, `--instancias`, `--saida`.

---

## 📊 Comparativo de Resultados

### Modelos exatos (Gurobi, limite de 600 s)

| Instância | Ótimo | Koopmans-Beckmann (MIQP) | Kaufman & Broeckx (MILP) |
| :--- | :---: | :---: | :---: |
| `nug12` | 578 | 578, ótimo provado em 17 s | 578, ótimo provado em 88 s |
| `chr15a` | 9896 | 9896, ótimo provado em 8 s | 9896, ótimo provado em 12 s |
| `had18` | 5358 | 5358 (0.00%), sem prova: limitante 1664 | 5400 (0.78%), sem prova: limitante 678 |

Em `had18` nenhum dos dois modelos prova a otimalidade em 600 s (gap do MIP de 69% e 87%).

### Metaheurísticas (`benchmark.py`, 30 sementes, 800 varreduras)

Gap médio para o ótimo da QAPLIB e, entre parênteses, quantas das 30 execuções atingiram o ótimo. Detalhes em [`results/benchmark/resumo.md`](results/benchmark/resumo.md).

| Instância | n | GRASP | SA | Busca Tabu |
| :--- | :---: | :---: | :---: | :---: |
| `nug12` | 12 | **0.05%** (29/30) | 1.23% (8/30) | 0.66% (21/30) |
| `chr15a` | 15 | **6.53%** (0/30) | 16.18% (1/30) | 11.89% (2/30) |
| `had18` | 18 | **0.00%** (29/30) | 0.12% (13/30) | 0.32% (15/30) |
| `els19` | 19 | **3.50%** (1/30) | 8.69% (1/30) | 22.45% (1/30) |
| `rou20` | 20 | 1.00% (0/30) | 1.63% (0/30) | **0.37%** (1/30) |
| `bur26a` | 26 | **0.10%** (2/30) | 0.12% (2/30) | 0.23% (0/30) |
| `kra30a` | 30 | 2.78% (0/30) | **2.37%** (2/30) | 4.93% (0/30) |
| `nug30` | 30 | 1.21% (0/30) | 0.80% (0/30) | **0.54%** (0/30) |
| `ste36a` | 36 | 3.91% (0/30) | **1.83%** (0/30) | 6.61% (0/30) |
| `sko42` | 42 | 1.32% (0/30) | **0.56%** (1/30) | 1.11% (0/30) |

Com o delta compilado, cada execução leva menos de 1 s mesmo em `sko42`. Uma execução única de cada modelo, sem semente, está em [`results/comparativo_geral.md`](results/comparativo_geral.md).
