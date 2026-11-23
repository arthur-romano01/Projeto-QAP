# Projeto QAP - Problema de Atribuição Quadrática

Projeto desenvolvido para a disciplina de **Pesquisa Operacional (UNIFESP)** com o objetivo de modelar e resolver o **Problema de Atribuição Quadrática (QAP - *Quadratic Assignment Problem*)** utilizando tanto métodos exatos com o **Gurobi Optimizer** (`gurobipy`) quanto métodos aproximados baseados em **Metaheurísticas**.

---

## 📁 Estrutura do Projeto

O repositório está organizado separando os métodos exatos (programação matemática) dos métodos aproximados (metaheurísticas), com compartilhamento centralizado dos dados de instâncias:

```text
Projeto-QAP/
│
├── data/
│   └── instances/
│       └── nug12.dat          # Instância clássica de benchmark da QAPLIB (n = 12)
│
├── Metaheurísticas/
│   ├── busca_tabu.py          # Busca Tabu com estrutura de vizinhança 2-opt
│   └── temperagem_sim.py      # Têmpera Simulada (Simulated Annealing)
│
├── Modelo-Matemático/
│   ├── main.py                # Modelo exato linearizado (Kaufman & Broeckx - MILP)
│   ├── qap_quadratic.py       # Modelo exato quadrático original (Koopmans-Beckmann - MIQP)
│   └── requirements.txt       # Dependências específicas do módulo
│
├── requirements.txt           # Dependências do projeto (gurobipy, numpy)
└── README.md                  # Documentação do projeto
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

Para resolver instâncias de maior porte em que métodos exatos se tornam proibitivos computacionalmente, foram implementadas metaheurísticas em Python com operações vetorizadas via `NumPy`:

### 1. Busca Tabu (`busca_tabu.py`)
* **Representação:** Permutação de tamanho $n$.
* **Estrutura de Vizinhança:** Movimentos 2-opt (troca de pares de instalações).
* **Memória Tabu:** Matriz que armazena pares proibidos por um determinado número de iterações para prevenir ciclos.
* **Critério de Aspiração:** Permite movimentos tabu caso eles produzam uma solução estritamente melhor do que a melhor já encontrada globalmente.

### 2. Têmpera Simulada / Simulated Annealing (`temperagem_sim.py`)
* **Perturbação:** Movimentos aleatórios 2-opt.
* **Critério de Aceitação:** Critério de Metropolis ($e^{-\Delta / T}$) para aceitar soluções de piora com probabilidade controlada, escapando de ótimos locais.
* **Esquema de Resfriamento:** Resfriamento geométrico progressivo ($T_{novo} = \alpha \cdot T_{atual}$).

---

## 🚀 Como Executar

### 1. Instalar dependências
Certifique-se de ter o Python 3.9+ e instale os pacotes necessários:
```bash
pip install -r requirements.txt
```

### 2. Executando os Modelos Matemáticos Exatos
A partir da raiz do repositório:
- **Modelo Linearizado (Kaufman & Broeckx):**
  ```bash
  python Modelo-Matemático/main.py
  ```
- **Modelo Quadrático (Koopmans-Beckmann):**
  ```bash
  python Modelo-Matemático/qap_quadratic.py
  ```

*(Ou entrando na pasta com `cd Modelo-Matemático` e executando `python main.py`)*

Por padrão os modelos resolvem `nug12`. Para outra instância de `data/instances/`, passe o nome e, se quiser, um limite de tempo em segundos:
```bash
python Modelo-Matemático/qap_quadratic.py chr15a --tempo-limite 600
```

### 3. Executando as Metaheurísticas
A partir da raiz do repositório:
- **Busca Tabu:**
  ```bash
  python Metaheurísticas/busca_tabu.py
  ```
- **Têmpera Simulada (Simulated Annealing):**
  ```bash
  python Metaheurísticas/temperagem_sim.py
  ```

*(Ou entrando na pasta com `cd Metaheurísticas` e executando `python busca_tabu.py`)*

> **💡 Resolução Dinâmica de Caminhos (`pathlib`):**
> Todos os scripts utilizam resolução de caminho que verifica tanto a pasta raiz quanto a pasta local (`BASE_DIR.parent / "data"` ou `BASE_DIR / "data"`). Dessa forma, qualquer script pode ser executado diretamente da raiz, de dentro da sua subpasta ou através do botão *Play* da IDE sem erros de `FileNotFoundError`.

---

## 📊 Comparativo de Resultados (`nug12.dat`)

Desempenho obtido na instância de benchmark `nug12.dat` ($n = 12$):

| Método | Tipo | Custo Encontrado | Gap p/ Ótimo | Tempo Médio |
| :--- | :--- | :---: | :---: | :---: |
| **Koopmans-Beckmann (Gurobi)** | Exato (MIQP) | **578** | **0.00%** | ~20.5 s |
| **Kaufman & Broeckx (Gurobi)** | Exato (MILP) | **578** | **0.00%** | ~109 s |
| **Busca Tabu** | Metaheurística | **578** | **0.00%** | ~4.3 s |
| **Simulated Annealing** | Metaheurística | **582** | **0.69%** | ~0.6 s |
