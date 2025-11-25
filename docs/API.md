# 🔌 API/Models - Somos DaRua

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Estrutura de Models](#estrutura-de-models)
- [Models Disponíveis](#models-disponíveis)
  - [Doador](#1-doador)
  - [Beneficiario](#2-beneficiario)
  - [Doacao](#3-doacao)
  - [CampanhaDoacao](#4-campanhado acao)
  - [PontoColeta](#5-pontocoleta)
  - [ObjetoDoavel](#6-objetodoavel)
  - [Voluntario](#7-voluntario)
  - [Necessidade](#8-necessidade)
- [Operações CRUD](#operações-crud)
- [Validações](#validações)
- [Exemplos de Uso](#exemplos-de-uso)

---

## 🎯 Visão Geral

Os **Models** representam as entidades do domínio e encapsulam toda a lógica de acesso a dados e regras de negócio. Cada model corresponde a uma tabela no banco de dados.

### Características dos Models

✅ **CRUD Completo**: Create, Read, Update, Delete
✅ **Validações**: Validação de dados antes de persistir
✅ **Type Hints**: Tipagem completa para melhor IDE support
✅ **Context Manager**: Gerenciamento automático de conexões
✅ **Métodos Estáticos**: Busca e listagem de dados
✅ **Conversão**: Métodos para dict/json

---

## 🏗️ Estrutura de Models

### Padrão Base

Todos os models seguem a mesma estrutura:

```python
class Model:
    # 1. Constructor
    def __init__(self, campo1, campo2, ..., id=None)

    # 2. Representation
    def __repr__(self) -> str

    # 3. Validation
    def validate(self) -> Tuple[bool, str]

    # 4. CRUD Operations
    def save(self) -> bool
    def update(self) -> bool
    def delete(self) -> bool

    # 5. Static Methods (Queries)
    @staticmethod
    def get_by_id(id: int) -> Optional['Model']

    @staticmethod
    def get_all() -> List['Model']

    @staticmethod
    def search(...) -> List['Model']

    # 6. Utility
    def to_dict(self) -> Dict
```

---

## 📚 Models Disponíveis

### 1. 👤 Doador

Representa pessoas ou empresas que fazem doações.

#### Localização

```
backend/models/doador.py
```

#### Atributos

| Atributo      | Tipo | Obrigatório | Descrição                  |
| ------------- | ---- | ----------- | -------------------------- |
| `idDoador`    | int  | Não (auto)  | ID único                   |
| `nome`        | str  | Sim         | Nome completo/razão social |
| `telefone`    | str  | Não         | Telefone de contato        |
| `email`       | str  | Não         | Email                      |
| `logradouro`  | str  | Não         | Rua/Avenida                |
| `numero`      | str  | Não         | Número                     |
| `complemento` | str  | Não         | Complemento                |
| `bairro`      | str  | Não         | Bairro                     |
| `cidade`      | str  | Não         | Cidade                     |
| `estado`      | str  | Não         | UF (2 caracteres)          |
| `cep`         | str  | Não         | CEP (8 dígitos)            |

#### Métodos

```python
# Constructor
doador = Doador(
    nome="João Silva",
    email="joao@email.com",
    telefone="(31) 99999-9999",
    cidade="Belo Horizonte",
    estado="MG"
)

# Validation
valido, erro = doador.validate()

# Create
doador.save()  # Returns: bool

# Read
doador = Doador.get_by_id(1)
todos = Doador.get_all()
buscados = Doador.search_by_name("João")

# Update
doador.nome = "João Silva Santos"
doador.update()

# Delete
doador.delete()

# Utility
dict_data = doador.to_dict()
```

#### Validações

- ✅ Nome obrigatório e não vazio
- ✅ Email deve conter '@' (se fornecido)
- ✅ Estado deve ter exatamente 2 caracteres (se fornecido)
- ✅ CEP deve ter 8 dígitos (se fornecido)

#### Exemplo Completo

```python
from backend.models.doador import Doador

# Criar novo doador
doador = Doador(
    nome="Maria Santos",
    email="maria@email.com",
    telefone="(11) 98765-4321",
    logradouro="Rua das Flores",
    numero="123",
    bairro="Centro",
    cidade="São Paulo",
    estado="SP",
    cep="01234-567"
)

# Validar
valido, erro = doador.validate()
if not valido:
    print(f"Erro: {erro}")
else:
    # Salvar
    if doador.save():
        print(f"Doador salvo com ID: {doador.idDoador}")

        # Buscar
        encontrado = Doador.get_by_id(doador.idDoador)
        print(f"Encontrado: {encontrado.nome}")

        # Atualizar
        encontrado.email = "novo_email@email.com"
        encontrado.update()

        # Listar todos
        todos = Doador.get_all()
        print(f"Total de doadores: {len(todos)}")

        # Buscar por nome
        resultados = Doador.search_by_name("Maria")
        print(f"Encontrados: {len(resultados)}")
```

---

### 2. 🤝 Beneficiario

Representa pessoas que recebem doações.

#### Localização

```
backend/models/beneficiario.py
```

#### Atributos

| Atributo         | Tipo | Obrigatório | Descrição     |
| ---------------- | ---- | ----------- | ------------- |
| `idBeneficiario` | int  | Não (auto)  | ID único      |
| `nome`           | str  | Sim         | Nome completo |
| `idade`          | int  | Não         | Idade em anos |
| `genero`         | str  | Não         | M, F, O ou N  |
| `descricao`      | str  | Não         | Observações   |

#### Métodos

```python
# Constructor
beneficiario = Beneficiario(
    nome="José Silva",
    idade=45,
    genero="M",
    descricao="Mora em situação de rua"
)

# CRUD
beneficiario.save()
beneficiario.update()
beneficiario.delete()

# Queries
Beneficiario.get_by_id(1)
Beneficiario.get_all()
Beneficiario.search_by_name("José")
```

#### Validações

- ✅ Nome obrigatório e não vazio
- ✅ Idade não pode ser negativa (se fornecida)
- ✅ Gênero deve ser M, F, O ou N (se fornecido)

#### Exemplo

```python
from backend.models.beneficiario import Beneficiario

# Criar beneficiário
beneficiario = Beneficiario(
    nome="Ana Costa",
    idade=32,
    genero="F",
    descricao="Mãe de 2 filhos"
)

if beneficiario.save():
    print(f"✅ Beneficiário cadastrado: ID {beneficiario.idBeneficiario}")
```

---

### 3. 📦 Doacao

Representa uma doação realizada por um doador.

#### Localização

```
backend/models/doacao.py
```

#### Atributos

| Atributo      | Tipo | Obrigatório | Descrição        |
| ------------- | ---- | ----------- | ---------------- |
| `idDoacao`    | int  | Não (auto)  | ID único         |
| `dataCriacao` | date | Sim (auto)  | Data de registro |
| `dataEntrega` | date | Não         | Data de entrega  |
| `doadorId`    | int  | Sim         | FK para Doador   |
| `campanhaId`  | int  | Não         | FK para Campanha |

#### Métodos

```python
# Constructor
doacao = Doacao(
    doadorId=1,
    campanhaId=5,
    dataEntrega="2024-12-25"
)

# CRUD
doacao.save()
doacao.update()
doacao.delete()

# Queries
Doacao.get_by_id(1)
Doacao.get_all()
Doacao.get_by_doador(doador_id=1)
Doacao.get_by_periodo(data_inicio, data_fim)

# Relacionamentos
doacao.adicionar_objeto(objeto_id)
doacao.adicionar_beneficiario(beneficiario_id)
doacao.get_objetos()
doacao.get_beneficiarios()
```

#### Exemplo

```python
from backend.models.doacao import Doacao
from datetime import date

# Criar doação
doacao = Doacao(
    doadorId=1,
    campanhaId=2
)

if doacao.save():
    print(f"✅ Doação criada: ID {doacao.idDoacao}")

    # Adicionar objetos à doação
    doacao.adicionar_objeto(objeto_id=10)
    doacao.adicionar_objeto(objeto_id=11)

    # Adicionar beneficiários
    doacao.adicionar_beneficiario(beneficiario_id=5)

    # Marcar como entregue
    doacao.dataEntrega = date.today()
    doacao.update()
```

---

### 4. 📢 CampanhaDoacao

Representa campanhas de arrecadação.

#### Localização

```
backend/models/campanha_doacao.py
```

#### Atributos

| Atributo      | Tipo | Obrigatório | Descrição        |
| ------------- | ---- | ----------- | ---------------- |
| `idCampanha`  | int  | Não (auto)  | ID único         |
| `nome`        | str  | Sim         | Nome da campanha |
| `dataInicio`  | date | Não         | Data de início   |
| `dataTermino` | date | Não         | Data de término  |
| `descricao`   | str  | Não         | Descrição        |

#### Validações

- ✅ Nome obrigatório
- ✅ DataTermino >= DataInicio (se ambas fornecidas)

#### Exemplo

```python
from backend.models.campanha_doacao import CampanhaDoacao
from datetime import date, timedelta

# Criar campanha
campanha = CampanhaDoacao(
    nome="Campanha de Natal 2024",
    dataInicio=date.today(),
    dataTermino=date.today() + timedelta(days=30),
    descricao="Arrecadação de alimentos e roupas"
)

if campanha.save():
    print(f"✅ Campanha criada: ID {campanha.idCampanha}")

    # Buscar campanhas ativas
    ativas = CampanhaDoacao.get_campanhas_ativas()
    print(f"Campanhas ativas: {len(ativas)}")
```

---

### 5. 📍 PontoColeta

Representa locais de recebimento de doações.

#### Localização

```
backend/models/ponto_coleta.py
```

#### Atributos

| Atributo        | Tipo | Obrigatório | Descrição           |
| --------------- | ---- | ----------- | ------------------- |
| `idPontoColeta` | int  | Não (auto)  | ID único            |
| `responsavel`   | str  | Sim         | Nome do responsável |
| `logradouro`    | str  | Não         | Rua/Avenida         |
| `numero`        | str  | Não         | Número              |
| `complemento`   | str  | Não         | Complemento         |
| `bairro`        | str  | Não         | Bairro              |
| `cidade`        | str  | Não         | Cidade              |
| `estado`        | str  | Não         | UF                  |
| `cep`           | str  | Não         | CEP                 |

#### Exemplo

```python
from backend.models.ponto_coleta import PontoColeta

# Criar ponto de coleta
ponto = PontoColeta(
    responsavel="Carlos Silva",
    logradouro="Av. Principal",
    numero="500",
    bairro="Centro",
    cidade="Belo Horizonte",
    estado="MG",
    cep="30140-000"
)

if ponto.save():
    print(f"✅ Ponto criado: ID {ponto.idPontoColeta}")

    # Listar pontos por cidade
    pontos_bh = PontoColeta.get_by_cidade("Belo Horizonte")
    print(f"Pontos em BH: {len(pontos_bh)}")
```

---

### 6. 📦 ObjetoDoavel

Representa itens que podem ser doados.

#### Localização

```
backend/models/objeto_doavel.py
```

#### Atributos

| Atributo        | Tipo | Obrigatório | Descrição                         |
| --------------- | ---- | ----------- | --------------------------------- |
| `idObjeto`      | int  | Não (auto)  | ID único                          |
| `nome`          | str  | Sim         | Nome do item                      |
| `descricao`     | str  | Não         | Descrição                         |
| `categoria`     | str  | Não         | Categoria (ex: Alimentos, Roupas) |
| `pontoColetaId` | int  | Não         | FK para PontoColeta               |

#### Categorias Comuns

- 🍎 Alimentos
- 👕 Roupas
- 👟 Calçados
- 🛋️ Móveis
- 💻 Eletrônicos
- 📚 Livros
- 🧸 Brinquedos
- 🧴 Higiene

#### Exemplo

```python
from backend.models.objeto_doavel import ObjetoDoavel

# Criar objeto
objeto = ObjetoDoavel(
    nome="Cesta Básica",
    descricao="Cesta com 15 itens",
    categoria="Alimentos",
    pontoColetaId=1
)

if objeto.save():
    print(f"✅ Objeto criado: ID {objeto.idObjeto}")

    # Buscar por categoria
    alimentos = ObjetoDoavel.get_by_categoria("Alimentos")
    print(f"Total de alimentos: {len(alimentos)}")
```

---

### 7. 🙋 Voluntario

Representa pessoas que auxiliam nas ações.

#### Localização

```
backend/models/voluntario.py
```

#### Atributos

| Atributo       | Tipo | Obrigatório | Descrição     |
| -------------- | ---- | ----------- | ------------- |
| `idVoluntario` | int  | Não (auto)  | ID único      |
| `nome`         | str  | Sim         | Nome completo |
| `email`        | str  | Não         | Email         |
| `telefone`     | str  | Não         | Telefone      |

#### Exemplo

```python
from backend.models.voluntario import Voluntario

# Criar voluntário
voluntario = Voluntario(
    nome="Pedro Santos",
    email="pedro@email.com",
    telefone="(31) 98888-7777"
)

if voluntario.save():
    print(f"✅ Voluntário cadastrado: ID {voluntario.idVoluntario}")
```

---

### 8. 📝 Necessidade

Representa necessidades promovidas pelas campanhas.

#### Localização

```
backend/models/necessidade.py
```

#### Atributos

| Atributo        | Tipo | Obrigatório | Descrição                |
| --------------- | ---- | ----------- | ------------------------ |
| `idNecessidade` | int  | Não (auto)  | ID único                 |
| `descricao`     | str  | Sim         | Descrição da necessidade |

#### Exemplo

```python
from backend.models.necessidade import Necessidade

# Criar necessidade
necessidade = Necessidade(
    descricao="Arrecadação de cobertores para o inverno"
)

if necessidade.save():
    print(f"✅ Necessidade criada: ID {necessidade.idNecessidade}")
```

---

## 🔄 Operações CRUD

### Padrão Geral

Todos os models seguem o mesmo padrão CRUD:

```python
# CREATE
entidade = Model(campo1="valor1", campo2="valor2")
entidade.save()  # Returns bool

# READ
entidade = Model.get_by_id(1)  # Returns Optional[Model]
todas = Model.get_all()         # Returns List[Model]

# UPDATE
entidade.campo1 = "novo_valor"
entidade.update()  # Returns bool

# DELETE
entidade.delete()  # Returns bool
```

### Exemplo Completo de CRUD

```python
from backend.models.doador import Doador

# ========== CREATE ==========
print("1. Criando doador...")
doador = Doador(
    nome="João Silva",
    email="joao@email.com",
    cidade="São Paulo",
    estado="SP"
)

if doador.save():
    print(f"✅ Criado com ID: {doador.idDoador}")
else:
    print("❌ Erro ao criar")

# ========== READ ==========
print("\n2. Buscando doador...")
encontrado = Doador.get_by_id(doador.idDoador)
if encontrado:
    print(f"✅ Encontrado: {encontrado.nome}")

print("\n3. Listando todos...")
todos = Doador.get_all()
print(f"✅ Total: {len(todos)} doadores")

print("\n4. Buscando por nome...")
resultados = Doador.search_by_name("João")
print(f"✅ Encontrados: {len(resultados)} resultados")

# ========== UPDATE ==========
print("\n5. Atualizando doador...")
encontrado.email = "joao.novo@email.com"
encontrado.telefone = "(11) 98765-4321"
if encontrado.update():
    print("✅ Atualizado com sucesso")

# ========== DELETE ==========
print("\n6. Deletando doador...")
if encontrado.delete():
    print("✅ Deletado com sucesso")

# Verificar se foi deletado
verificar = Doador.get_by_id(doador.idDoador)
if verificar is None:
    print("✅ Confirmado: doador não existe mais")
```

---

## ✅ Validações

### Tipos de Validação

Cada model implementa validações específicas:

```python
def validate(self) -> Tuple[bool, str]:
    """
    Valida dados da entidade.

    Returns:
        Tuple[bool, str]: (valido, mensagem_erro)
    """
    # Validação de campos obrigatórios
    if not self.campo_obrigatorio:
        return False, "Campo obrigatório não preenchido"

    # Validação de formato
    if self.email and '@' not in self.email:
        return False, "Email inválido"

    # Validação de intervalo
    if self.idade and self.idade < 0:
        return False, "Idade não pode ser negativa"

    # Validação de lista
    if self.genero and self.genero not in ['M', 'F', 'O']:
        return False, "Gênero inválido"

    return True, ""
```

### Quando Validar

```python
# ✅ Validação automática no save()
doador.save()  # Chama validate() internamente

# ✅ Validação manual antes de processar
valido, erro = doador.validate()
if not valido:
    print(f"Erro: {erro}")
    return

# ✅ Validação no frontend (Streamlit)
if not nome:
    st.error("Nome é obrigatório")
    return
```

---

## 💡 Exemplos de Uso

### Exemplo 1: Cadastro Completo de Doação

```python
from backend.models.doador import Doador
from backend.models.doacao import Doacao
from backend.models.objeto_doavel import ObjetoDoavel
from backend.models.beneficiario import Beneficiario

# 1. Criar/buscar doador
doador = Doador.get_by_id(1)
if not doador:
    doador = Doador(nome="João Silva", email="joao@email.com")
    doador.save()

# 2. Criar doação
doacao = Doacao(
    doadorId=doador.idDoador,
    campanhaId=1
)

if doacao.save():
    print(f"✅ Doação criada: ID {doacao.idDoacao}")

    # 3. Adicionar objetos
    objeto1 = ObjetoDoavel(nome="Cesta Básica", categoria="Alimentos")
    objeto2 = ObjetoDoavel(nome="Coberto r", categoria="Roupas")

    objeto1.save()
    objeto2.save()

    doacao.adicionar_objeto(objeto1.idObjeto)
    doacao.adicionar_objeto(objeto2.idObjeto)

    # 4. Vincular beneficiários
    beneficiario = Beneficiario.get_by_id(1)
    doacao.adicionar_beneficiario(beneficiario.idBeneficiario)

    print("✅ Doação completa registrada!")
```

### Exemplo 2: Relatório de Doadores

```python
from backend.models.doador import Doador
from backend.models.doacao import Doacao

# Buscar todos os doadores
doadores = Doador.get_all()

# Contar doações de cada um
relatorio = []
for doador in doadores:
    doacoes = Doacao.get_by_doador(doador.idDoador)
    relatorio.append({
        'nome': doador.nome,
        'email': doador.email,
        'total_doacoes': len(doacoes)
    })

# Ordenar por total de doações
relatorio.sort(key=lambda x: x['total_doacoes'], reverse=True)

# Exibir top 10
print("Top 10 Doadores:")
for i, item in enumerate(relatorio[:10], 1):
    print(f"{i}. {item['nome']}: {item['total_doacoes']} doações")
```

### Exemplo 3: Campanhas Ativas

```python
from backend.models.campanha_doacao import CampanhaDoacao
from backend.models.doacao import Doacao
from datetime import date

# Buscar campanhas ativas
campanhas = CampanhaDoacao.get_campanhas_ativas()

print(f"Campanhas ativas: {len(campanhas)}\n")

for campanha in campanhas:
    # Contar doações da campanha
    doacoes = Doacao.get_by_campanha(campanha.idCampanha)

    # Calcular dias restantes
    dias_restantes = (campanha.dataTermino - date.today()).days

    print(f"📢 {campanha.nome}")
    print(f"   Doações: {len(doacoes)}")
    print(f"   Dias restantes: {dias_restantes}")
    print()
```

---

## 🔍 Queries Avançadas

### Joins e Relacionamentos

```python
# Buscar doações com informações do doador
def get_doacoes_com_doador():
    query = """
        SELECT
            d.idDoacao,
            d.DataCriacao,
            do.Nome as NomeDoador,
            do.Email as EmailDoador
        FROM Doacao d
        INNER JOIN Doador do ON d.Doador_idDoador = do.idDoador
        ORDER BY d.DataCriacao DESC
    """

    with DatabaseConnection() as db:
        return db.fetch_all(query)

# Buscar objetos de uma doação
def get_objetos_doacao(doacao_id):
    query = """
        SELECT o.*
        FROM ObjetoDoavel o
        INNER JOIN Contem c ON o.idObjetoDoavel = c.ObjetoDoavel_idObjetoDoavel
        WHERE c.Doacao_idDoacao = %s
    """

    with DatabaseConnection() as db:
        return db.fetch_all(query, (doacao_id,))
```

---

## 📚 Referências

- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [MySQL Connector Python](https://dev.mysql.com/doc/connector-python/en/)
- [Context Managers](https://docs.python.org/3/library/contextlib.html)

---

[⬅️ Voltar ao Índice](./INDEX.md) | [➡️ Próximo: Frontend](./FRONTEND.md)
