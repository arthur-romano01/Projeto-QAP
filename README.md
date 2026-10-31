# Projeto QAP - Problema de Atribuição Quadrática

Projeto desenvolvido para a disciplina de **Pesquisa Operacional (UNIFESP)** com o objetivo de modelar e resolver o **Problema de Atribuição Quadrática (QAP - *Quadratic Assignment Problem*)** utilizando a API Python do **Gurobi Optimizer** (`gurobipy`).

---

## 📁 Estrutura do Projeto

O projeto é estruturado de forma direta e sem dependências complexas:

```text
Projeto-QAP/
│
├── Modelo-Matemático/
│   ├── data/
│   │   └── instances/
│   │       └── nug12.dat      # Instância clássica de benchmark da QAPLIB (n = 12)
│   │
│   ├── main.py                # Script do modelo linearizado (Kaufman & Broeckx - MILP)
│   ├── qap_quadratic.py       # Script do modelo quadrático original (Koopmans-Beckmann - MIQP)
│   └── requirements.txt       # Dependências do projeto (gurobipy)
│
└── README.md                  # Documentação do projeto
```

---

## 🧮 Modelagem Matemática

O **QAP** clássico de Koopmans-Beckmann busca atribuir $n$ instalações a $n$ locais minimizando o custo total de transporte (fluxo $\times$ distância).

### Formulação Quadrática Original (Koopmans-Beckmann)

$$\min \sum_{i=0}^{n-1} \sum_{j=0}^{n-1} \sum_{k=0}^{n-1} \sum_{l=0}^{n-1} F_{ik} \cdot D_{jl} \cdot x_{ij} \cdot x_{kl}$$

Sujeito a:
* $\sum_{j=0}^{n-1} x_{ij} = 1 \quad \forall i \in \{0, \dots, n-1\}$ (cada instalação vai para um único local)
* $\sum_{i=0}^{n-1} x_{ij} = 1 \quad \forall j \in \{0, \dots, n-1\}$ (cada local recebe uma única instalação)
* $x_{ij} \in \{0, 1\} \quad \forall i, j$

Como a função objetivo é quadrática e não-convexa devido aos produtos $x_{ij} \cdot x_{kl}$, métodos exatos diretos exigem algoritmos específicos para problemas não-convexos.

---

## 📐 Linearização de Kaufman e Broeckx (1978)

A formulação implementada em [`Modelo-Matemático/main.py`](Modelo-Matemático/main.py) é a **Linearização de Kaufman e Broeckx**, uma das linearizações mais compactas existentes para o QAP. Ela transforma o problema em uma **Programação Linear Inteira Mista (MILP)**, dispensando o parâmetro de não-convexidade e permitindo o uso de algoritmos tradicionais de *Branch-and-Bound* e planos de corte.

### Ideia Central e Variáveis Auxiliares
Em vez de criar uma variável para cada par de pares $(i, j, k, l)$ — o que geraria $O(n^4)$ variáveis, como na formulação de Lawler —, Kaufman e Broeckx agregam o custo total de interação da instalação $i$ no local $j$ em uma única variável contínua $w_{ij} \ge 0$:

$$w_{ij} = x_{ij} \sum_{k=0}^{n-1} \sum_{l=0}^{n-1} F_{ik} D_{jl} x_{kl}$$

### Formulação MILP com Big-M

#### Variáveis de Decisão
* $x_{ij} \in \{0, 1\}$: $1$ se a instalação $i$ for alocada ao local $j$; $0$ caso contrário.
* $w_{ij} \ge 0$: variável contínua representando o custo de interação da instalação $i$ quando alocada no local $j$.

#### Parâmetro Big-M ($M_{ij}$)
Para cada par $(i, j)$, calcula-se um limitante superior (*upper bound*) para a interação máxima possível:
$$M_{ij} = \sum_{k=0}^{n-1} \sum_{l=0}^{n-1} F_{ik} D_{jl}$$

#### Modelo Matemático Completo

$$\min \sum_{i=0}^{n-1} \sum_{j=0}^{n-1} w_{ij}$$

Sujeito a:

1. **Atribuição de Instalações:**
   $$\sum_{j=0}^{n-1} x_{ij} = 1 \quad \forall i \in \{0, \dots, n-1\}$$

2. **Atribuição de Locais:**
   $$\sum_{i=0}^{n-1} x_{ij} = 1 \quad \forall j \in \{0, \dots, n-1\}$$

3. **Restrições de Acoplamento Big-M (Kaufman & Broeckx):**
   $$w_{ij} \ge \sum_{k=0}^{n-1} \sum_{l=0}^{n-1} F_{ik} D_{jl} x_{kl} - M_{ij}(1 - x_{ij}) \quad \forall i, j \in \{0, \dots, n-1\}$$

4. **Domínio:**
   $$x_{ij} \in \{0, 1\}, \quad w_{ij} \ge 0 \quad \forall i, j \in \{0, \dots, n-1\}$$

#### Funcionamento da Restrição Big-M
* **Se $x_{ij} = 1$:** O termo $-M_{ij}(1 - x_{ij})$ torna-se $0$, ativando a restrição $w_{ij} \ge \sum_{k,l} F_{ik} D_{jl} x_{kl}$. Pela minimização na função objetivo, $w_{ij}$ assumirá exatamente esse custo.
* **Se $x_{ij} = 0$:** O termo $-M_{ij}$ subtrai uma constante suficientemente grande, tornando o lado direito $\le 0$. Como $w_{ij} \ge 0$ e estamos minimizando, o solver define $w_{ij} = 0$.

> **Vantagens:** O modelo adiciona apenas $n^2$ variáveis contínuas e $n^2$ restrições lineares (contra $O(n^4)$ de outras linearizações clássicas).

---

## 🚀 Como Executar

### 1. Instalar dependências
Certifique-se de ter o Python 3.9+ instalado e o Gurobi configurado:
```bash
cd Modelo-Matemático
pip install -r requirements.txt
```

### 2. Executar os modelos

Os scripts utilizam resolução dinâmica de caminhos (`Path(__file__).resolve().parent`), o que permite executá-los com segurança tanto a partir da pasta `Modelo-Matemático/` quanto a partir da raiz do projeto.

**Opção A: A partir da pasta `Modelo-Matemático/`**
- Modelo Linearizado (Kaufman e Broeckx):
  ```bash
  python main.py
  ```
- Modelo Quadrático Exato (Koopmans-Beckmann):
  ```bash
  python qap_quadratic.py
  ```

**Opção B: A partir da raiz do repositório**
```bash
python Modelo-Matemático/main.py
python Modelo-Matemático/qap_quadratic.py
```

