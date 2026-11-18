# Licença acadêmica do Gurobi (WLS)

Guia rápido para rodar os modelos exatos do Projeto-QAP no seu computador.

> **A licença é pessoal.** Cada pessoa precisa gerar a sua. Nunca envie o seu `gurobi.lic` para ninguém e nunca faça commit dele: o arquivo contém as suas credenciais, e as regras da Gurobi proíbem compartilhar as chaves de API. Guarde-o fora da pasta do repositório.

## Por que preciso disso?

O `gurobipy` instalado pelo `pip` vem com uma licença restrita, limitada a 2000 variáveis, 2000 restrições lineares e apenas 200 variáveis quando há termos quadráticos. Com as 10 instâncias do projeto, fica assim:

| Modelo | Variáveis | Limite na licença restrita | Instâncias que cabem |
| --- | --- | --- | --- |
| Quadrático (Koopmans-Beckmann) | n² | n <= 14 | só `nug12` |
| Linearizado (Kaufman-Broeckx) | 2n² | n <= 31 | todas, menos `ste36a` (n = 36) e `sko42` (n = 42) |

A licença WLS (*Web License Service*) remove esses limites. Ela é validada on-line nos servidores da Gurobi, então não fica presa a um único computador.

## Regras da licença

- Gratuita para estudantes, docentes e funcionários de instituições de ensino superior reconhecidas, apenas para pesquisa, ensino ou trabalhos de disciplina.
- **Gerar e renovar exige estar na rede da universidade.**
- Depois de criada, funciona em qualquer computador com internet, inclusive em casa.
- Precisa de internet durante toda a otimização.
- Vale 90 dias e pode ser renovada enquanto você tiver vínculo acadêmico.
- Permite 2 sessões simultâneas.
- Exige Gurobi 10 ou mais recente (o `requirements.txt` do projeto já instala uma versão compatível).

## Passo a passo

1. **Crie a sua conta** em <https://portal.gurobi.com/iam/register/>, registrando-se como usuário **Academic**.

2. **Gere a licença na rede da universidade.** Conectado à rede da Unifesp, abra <https://portal.gurobi.com/iam/licenses/request/?type=academic> e clique em **GENERATE NOW** no bloco **WLS Academic**. Se os blocos acadêmicos não aparecerem, confira se o seletor da página está em **ACADEMIC**, e não em COMMERCIAL.

3. **Baixe o `gurobi.lic`.** No Web License Manager, em <https://license.gurobi.com/>, abra a aba **API Keys** e clique em **CREATE API KEY**. Baixe o arquivo na hora: esse é o único momento em que a chave fica disponível para download. O conteúdo tem este formato:

   ```
   WLSACCESSID=SEU_ACCESS_ID
   WLSSECRET=SEU_SECRET
   LICENSEID=SEU_LICENSE_ID
   ```

4. **Coloque o arquivo na sua pasta pessoal**, com o nome exato `gurobi.lic`:

   | Sistema | Pasta pessoal (recomendada) | Alternativa para todo o computador |
   | --- | --- | --- |
   | Windows | `C:\Users\SEU_USUARIO` | `C:\gurobi` |
   | Linux | `/home/SEU_USUARIO` | `/opt/gurobi` |
   | macOS | `/Users/SEU_USUARIO` | `/Library/gurobi` |

   No Linux e no macOS, proteja o arquivo para que só a sua conta consiga lê-lo:

   ```bash
   chmod 600 ~/gurobi.lic
   ```

   Se precisar guardar o arquivo em outro lugar, defina a variável de ambiente `GRB_LICENSE_FILE` com o caminho completo **do arquivo**, e não da pasta (por exemplo, `/caminho/para/gurobi.lic`).

5. **Instale as dependências** a partir da raiz do repositório:

   ```bash
   pip install -r requirements.txt
   ```

6. **Teste a licença.** Este comando monta um modelo acima do limite da licença restrita. Só criar um `gp.Model()` não serve como teste, porque isso também funciona na licença restrita.

   ```bash
   python -c "import gurobipy as gp; m=gp.Model(); m.addVars(2001); m.optimize(); print('LICENCA OK')"
   ```

   - **Deu certo:** aparece `LICENCA OK` no final.
   - **Deu errado:** aparece um erro como `Model too large for size-limited license`. Veja a seção abaixo.

## Problemas comuns

**`Academic Domain Error`**
A Gurobi não reconheceu o seu endereço de rede como acadêmico. Conecte-se à rede do campus e tente de novo.

**`[USER_NOT_ACADEMIC] User account type is not academic`**
A sua conta está registrada como comercial. No [portal da Gurobi](https://portal.gurobi.com/), abra **Review your profile information**, clique em **EDIT** e mude a resposta de "Are you an Academic or Commercial user?" para **Academic**. Se nada mudar, limpe o cache do navegador.

**`Model too large` ou menção a licença restrita (`restricted license`)**
O Gurobi não está encontrando o seu arquivo. Confira a pasta e o nome: downloads repetidos ou o próprio sistema podem gerar nomes como `gurobi.lic.txt` ou `gurobi(1).lic`.

**`ERROR 10009: License has expired`**
Passaram-se os 90 dias. Conectado à rede da universidade, renove a licença no [Web License Manager](https://license.gurobi.com/). A renovação pode levar de 15 a 30 minutos para valer.

## Fontes

Informações conferidas em 18/11/2026 na documentação da Gurobi. As telas do portal exigem login e podem mudar, e este passo a passo não foi testado de ponta a ponta.

- [Limites da licença restrita](https://support.gurobi.com/hc/en-us/articles/360051597492-How-do-I-resolve-a-Model-too-large-for-size-limited-Gurobi-license-error)
- [Regras da licença acadêmica WLS](https://support.gurobi.com/hc/en-us/articles/34672988479633)
- [Como obter a licença acadêmica](https://support.gurobi.com/hc/en-us/articles/360040541251-How-do-I-obtain-a-free-academic-license)
- [Configuração da licença WLS](https://support.gurobi.com/hc/en-us/articles/13232844297489-How-do-I-set-up-a-Web-License-Service-WLS-license)
- [Onde colocar o `gurobi.lic`](https://support.gurobi.com/hc/en-us/articles/360013417211-Where-do-I-place-the-Gurobi-license-file-gurobi-lic)
- [`Academic Domain Error`](https://support.gurobi.com/hc/en-us/articles/360058679471)
- [Licença sem acesso à rede do campus](https://support.gurobi.com/hc/en-us/articles/43876824710673)
- [Erro `User account type is not academic`](https://support.gurobi.com/hc/en-us/articles/14140596056593)
- [Erro de licença expirada](https://support.gurobi.com/hc/en-us/articles/20183190511889)
- [Download da chave de API na criação](https://support.gurobi.com/hc/en-us/articles/4409582394769-Google-Colab-Installation-and-Licensing)
