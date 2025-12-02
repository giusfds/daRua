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

## 🎯 Casos de Uso Práticos

### Caso de Uso 1: Fluxo Completo de Doação em Duas Fases

Este exemplo demonstra o sistema de duas fases (Recebimento → Distribuição):

```python
from backend.models.doador import Doador
from backend.models.doacao import Doacao
from backend.models.objeto_doavel import ObjetoDoavel
from backend.models.beneficiario import Beneficiario
from backend.models.voluntario import Voluntario
from datetime import date, timedelta

# ========== FASE 1: RECEBIMENTO ==========
print("🔵 FASE 1: Recebimento da Doação\n")

# 1. Registrar doador
doador = Doador(
    nome="Supermercado Bom Preço",
    email="contato@bompreco.com",
    telefone="(31) 3333-4444",
    cidade="Belo Horizonte",
    estado="MG"
)
doador.save()
print(f"✅ Doador cadastrado: {doador.nome}")

# 2. Criar doação (Status inicial: Recebida)
doacao = Doacao(
    doadorId=doador.idDoador,
    campanhaId=1
)
doacao.save()
print(f"✅ Doação registrada: ID {doacao.idDoacao}")
print(f"   Status: Recebida")
print(f"   Data: {doacao.dataCriacao}")

# 3. Adicionar itens doados
objetos_doados = [
    ObjetoDoavel(nome="Arroz 5kg", categoria="Alimentos", pontoColetaId=1),
    ObjetoDoavel(nome="Feijão 1kg", categoria="Alimentos", pontoColetaId=1),
    ObjetoDoavel(nome="Óleo 900ml", categoria="Alimentos", pontoColetaId=1),
    ObjetoDoavel(nome="Açúcar 1kg", categoria="Alimentos", pontoColetaId=1)
]

print("\n📦 Itens recebidos:")
for obj in objetos_doados:
    obj.save()
    doacao.adicionar_objeto(obj.idObjeto)
    print(f"   - {obj.nome}")

# ========== FASE 2: DISTRIBUIÇÃO ==========
print("\n🟢 FASE 2: Distribuição da Doação\n")

# 4. Selecionar beneficiários
beneficiarios_ids = [1, 2, 3]  # IDs dos beneficiários
print(f"👥 Beneficiários selecionados: {len(beneficiarios_ids)}")

# 5. Selecionar voluntários distribuidores
voluntarios_ids = [1, 2]  # IDs dos voluntários
print(f"🙋 Voluntários distribuidores: {len(voluntarios_ids)}")

# 6. Executar distribuição
print("\n🚚 Executando distribuição...")
sucesso = doacao.distribuir(
    beneficiarios_ids=beneficiarios_ids,
    voluntarios_ids=voluntarios_ids
)

if sucesso:
    print("✅ Distribuição concluída!")
    print(f"   Status: Distribuída")
    print(f"   Data de distribuição: {date.today()}")

    # 7. Verificar status
    status = doacao.calcular_status()
    print(f"\n📊 Status da Doação:")
    print(f"   - Status: {status}")
    print(f"   - Beneficiários: {len(doacao.listar_beneficiarios())}")
    print(f"   - Voluntários: {len(doacao.listar_voluntarios_distribuidores())}")
    print(f"   - Objetos: {len(doacao.get_objetos())}")
else:
    print("❌ Erro na distribuição")
```

**Saída Esperada:**

```
🔵 FASE 1: Recebimento da Doação

✅ Doador cadastrado: Supermercado Bom Preço
✅ Doação registrada: ID 42
   Status: Recebida
   Data: 2024-01-15

📦 Itens recebidos:
   - Arroz 5kg
   - Feijão 1kg
   - Óleo 900ml
   - Açúcar 1kg

🟢 FASE 2: Distribuição da Doação

👥 Beneficiários selecionados: 3
🙋 Voluntários distribuidores: 2

🚚 Executando distribuição...
✅ Distribuição concluída!
   Status: Distribuída
   Data de distribuição: 2024-01-15

📊 Status da Doação:
   - Status: Distribuída
   - Beneficiários: 3
   - Voluntários: 2
   - Objetos: 4
```

---

### Caso de Uso 2: Gestão Completa de Campanha

Criar campanha, adicionar necessidades, receber doações e gerar relatório:

```python
from backend.models.campanha_doacao import CampanhaDoacao
from backend.models.necessidade import Necessidade
from backend.models.doacao import Doacao
from datetime import date, timedelta

# 1. Criar campanha
print("📢 Criando Campanha de Inverno\n")

campanha = CampanhaDoacao(
    nome="Campanha do Agasalho 2024",
    dataInicio=date.today(),
    dataTermino=date.today() + timedelta(days=60),
    descricao="Arrecadação de roupas e cobertores para o inverno"
)
campanha.save()
print(f"✅ Campanha criada: ID {campanha.idCampanha}")

# 2. Definir necessidades
necessidades = [
    "Cobertores novos ou em bom estado",
    "Agasalhos tamanho adulto",
    "Meias térmicas",
    "Toucas e luvas",
    "Roupas de cama"
]

print(f"\n📝 Necessidades da campanha:")
for desc in necessidades:
    nec = Necessidade(descricao=desc)
    nec.save()
    # Vincular à campanha (tabela N:N Promove)
    print(f"   - {desc}")

# 3. Simular recebimento de doações ao longo dos dias
print(f"\n📦 Doações recebidas:\n")

doacoes_campanha = []
for i in range(5):
    doacao = Doacao(
        doadorId=i + 1,  # Diferentes doadores
        campanhaId=campanha.idCampanha
    )
    doacao.save()
    doacoes_campanha.append(doacao)
    print(f"   Dia {i+1}: Doação #{doacao.idDoacao}")

# 4. Gerar relatório da campanha
print(f"\n📊 Relatório da Campanha\n")
print(f"{'='*50}")
print(f"Campanha: {campanha.nome}")
print(f"Período: {campanha.dataInicio} até {campanha.dataTermino}")
print(f"Dias restantes: {(campanha.dataTermino - date.today()).days}")
print(f"\n📈 Estatísticas:")
print(f"   Total de doações: {len(doacoes_campanha)}")
print(f"   Necessidades definidas: {len(necessidades)}")

# Calcular quantos foram distribuídos
distribuidas = sum(1 for d in doacoes_campanha if d.calcular_status() == "Distribuída")
recebidas = len(doacoes_campanha) - distribuidas

print(f"   Doações recebidas: {recebidas}")
print(f"   Doações distribuídas: {distribuidas}")
print(f"   Taxa de distribuição: {(distribuidas/len(doacoes_campanha)*100):.1f}%")
print(f"{'='*50}")
```

**Saída Esperada:**

```
📢 Criando Campanha de Inverno

✅ Campanha criada: ID 15

📝 Necessidades da campanha:
   - Cobertores novos ou em bom estado
   - Agasalhos tamanho adulto
   - Meias térmicas
   - Toucas e luvas
   - Roupas de cama

📦 Doações recebidas:

   Dia 1: Doação #128
   Dia 2: Doação #129
   Dia 3: Doação #130
   Dia 4: Doação #131
   Dia 5: Doação #132

📊 Relatório da Campanha

==================================================
Campanha: Campanha do Agasalho 2024
Período: 2024-01-15 até 2024-03-15
Dias restantes: 59

📈 Estatísticas:
   Total de doações: 5
   Necessidades definidas: 5
   Doações recebidas: 3
   Doações distribuídas: 2
   Taxa de distribuição: 40.0%
==================================================
```

---

### Caso de Uso 3: Sistema de Busca e Filtros

Implementar buscas avançadas por múltiplos critérios:

```python
from backend.models.doador import Doador
from backend.models.doacao import Doacao
from backend.models.beneficiario import Beneficiario
from backend.database.connection import DatabaseConnection
from datetime import date, timedelta

class BuscaAvancada:
    """Classe utilitária para buscas complexas"""

    @staticmethod
    def buscar_doadores_por_regiao(cidade: str = None, estado: str = None):
        """Busca doadores por localização"""
        query = "SELECT * FROM Doador WHERE 1=1"
        params = []

        if cidade:
            query += " AND Cidade LIKE %s"
            params.append(f"%{cidade}%")

        if estado:
            query += " AND Estado = %s"
            params.append(estado)

        query += " ORDER BY Nome"

        with DatabaseConnection() as db:
            results = db.fetch_all(query, tuple(params))
            return [Doador(**row) for row in results] if results else []

    @staticmethod
    def buscar_doacoes_por_periodo_e_status(
        data_inicio: date,
        data_fim: date,
        status: str = None
    ):
        """Busca doações por período e opcionalmente por status"""
        query = """
            SELECT
                d.idDoacao,
                d.DataCriacao,
                d.DataEntrega,
                do.Nome as NomeDoador,
                c.Nome as NomeCampanha,
                CASE
                    WHEN d.DataEntrega IS NOT NULL THEN 'Distribuída'
                    ELSE 'Recebida'
                END as Status
            FROM Doacao d
            INNER JOIN Doador do ON d.Doador_idDoador = do.idDoador
            LEFT JOIN CampanhaDoacao c ON d.CampanhaDoacao_idCampanha = c.idCampanha
            WHERE d.DataCriacao BETWEEN %s AND %s
        """
        params = [data_inicio, data_fim]

        if status:
            if status == "Distribuída":
                query += " AND d.DataEntrega IS NOT NULL"
            elif status == "Recebida":
                query += " AND d.DataEntrega IS NULL"

        query += " ORDER BY d.DataCriacao DESC"

        with DatabaseConnection() as db:
            return db.fetch_all(query, tuple(params))

    @staticmethod
    def buscar_beneficiarios_por_perfil(
        genero: str = None,
        idade_min: int = None,
        idade_max: int = None
    ):
        """Busca beneficiários por perfil demográfico"""
        query = "SELECT * FROM Beneficiario WHERE 1=1"
        params = []

        if genero:
            query += " AND Genero = %s"
            params.append(genero)

        if idade_min is not None:
            query += " AND Idade >= %s"
            params.append(idade_min)

        if idade_max is not None:
            query += " AND Idade <= %s"
            params.append(idade_max)

        query += " ORDER BY Nome"

        with DatabaseConnection() as db:
            results = db.fetch_all(query, tuple(params))
            return [Beneficiario(**row) for row in results] if results else []


# ========== EXEMPLO DE USO ==========

# 1. Buscar doadores de São Paulo
print("🔍 Buscando doadores de São Paulo\n")
doadores_sp = BuscaAvancada.buscar_doadores_por_regiao(estado="SP")
print(f"Encontrados: {len(doadores_sp)} doadores")
for doador in doadores_sp[:5]:
    print(f"   - {doador.nome} ({doador.cidade})")

# 2. Buscar doações do último mês
print("\n🔍 Buscando doações do último mês\n")
hoje = date.today()
mes_atras = hoje - timedelta(days=30)

doacoes = BuscaAvancada.buscar_doacoes_por_periodo_e_status(
    data_inicio=mes_atras,
    data_fim=hoje,
    status="Distribuída"
)
print(f"Encontradas: {len(doacoes)} doações distribuídas")
for doacao in doacoes[:5]:
    print(f"   - {doacao['NomeDoador']} em {doacao['DataCriacao']}")

# 3. Buscar beneficiários mulheres entre 30-50 anos
print("\n🔍 Buscando beneficiárias mulheres (30-50 anos)\n")
beneficiarias = BuscaAvancada.buscar_beneficiarios_por_perfil(
    genero="F",
    idade_min=30,
    idade_max=50
)
print(f"Encontradas: {len(beneficiarias)} beneficiárias")
for benef in beneficiarias[:5]:
    print(f"   - {benef.nome}, {benef.idade} anos")
```

---

### Caso de Uso 4: Dashboard com Métricas

Coletar e exibir estatísticas do sistema:

```python
from backend.models.doador import Doador
from backend.models.doacao import Doacao
from backend.models.beneficiario import Beneficiario
from backend.models.voluntario import Voluntario
from backend.database.connection import DatabaseConnection
from datetime import date, timedelta

class Dashboard:
    """Classe para métricas e estatísticas"""

    @staticmethod
    def obter_metricas_gerais():
        """Retorna métricas gerais do sistema"""
        return {
            'total_doadores': len(Doador.get_all()),
            'total_beneficiarios': len(Beneficiario.get_all()),
            'total_voluntarios': len(Voluntario.get_all()),
            'total_doacoes': len(Doacao.get_all())
        }

    @staticmethod
    def obter_doacoes_por_status():
        """Conta doações por status"""
        todas = Doacao.get_all()
        recebidas = sum(1 for d in todas if d.calcular_status() == "Recebida")
        distribuidas = len(todas) - recebidas

        return {
            'recebidas': recebidas,
            'distribuidas': distribuidas,
            'taxa_distribuicao': (distribuidas / len(todas) * 100) if todas else 0
        }

    @staticmethod
    def obter_top_doadores(limite=10):
        """Retorna doadores com mais doações"""
        query = """
            SELECT
                do.idDoador,
                do.Nome,
                COUNT(d.idDoacao) as TotalDoacoes
            FROM Doador do
            LEFT JOIN Doacao d ON do.idDoador = d.Doador_idDoador
            GROUP BY do.idDoador, do.Nome
            ORDER BY TotalDoacoes DESC
            LIMIT %s
        """

        with DatabaseConnection() as db:
            return db.fetch_all(query, (limite,))

    @staticmethod
    def obter_doacoes_por_mes():
        """Retorna quantidade de doações por mês (últimos 6 meses)"""
        query = """
            SELECT
                DATE_FORMAT(DataCriacao, '%Y-%m') as Mes,
                COUNT(*) as Total
            FROM Doacao
            WHERE DataCriacao >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
            GROUP BY Mes
            ORDER BY Mes
        """

        with DatabaseConnection() as db:
            return db.fetch_all(query)


# ========== EXEMPLO DE USO ==========

print("📊 DASHBOARD - Sistema Somos DaRua\n")
print("=" * 60)

# 1. Métricas Gerais
metricas = Dashboard.obter_metricas_gerais()
print("\n📈 MÉTRICAS GERAIS\n")
print(f"   👤 Doadores cadastrados: {metricas['total_doadores']}")
print(f"   🤝 Beneficiários: {metricas['total_beneficiarios']}")
print(f"   🙋 Voluntários: {metricas['total_voluntarios']}")
print(f"   📦 Doações registradas: {metricas['total_doacoes']}")

# 2. Status das Doações
status = Dashboard.obter_doacoes_por_status()
print("\n🔄 STATUS DAS DOAÇÕES\n")
print(f"   🔵 Recebidas: {status['recebidas']}")
print(f"   🟢 Distribuídas: {status['distribuidas']}")
print(f"   📊 Taxa de distribuição: {status['taxa_distribuicao']:.1f}%")

# 3. Top Doadores
print("\n⭐ TOP 10 DOADORES\n")
top = Dashboard.obter_top_doadores()
for i, doador in enumerate(top, 1):
    print(f"   {i}. {doador['Nome']}: {doador['TotalDoacoes']} doações")

# 4. Doações por Mês
print("\n📅 DOAÇÕES POR MÊS (Últimos 6 meses)\n")
por_mes = Dashboard.obter_doacoes_por_mes()
for item in por_mes:
    # Criar gráfico simples em texto
    barra = "█" * item['Total']
    print(f"   {item['Mes']}: {barra} ({item['Total']})")

print("\n" + "=" * 60)
```

**Saída Esperada:**

```
📊 DASHBOARD - Sistema Somos DaRua

============================================================

📈 MÉTRICAS GERAIS

   👤 Doadores cadastrados: 245
   🤝 Beneficiários: 312
   🙋 Voluntários: 48
   📦 Doações registradas: 589

🔄 STATUS DAS DOAÇÕES

   🔵 Recebidas: 127
   🟢 Distribuídas: 462
   📊 Taxa de distribuição: 78.4%

⭐ TOP 10 DOADORES

   1. Supermercado Central: 45 doações
   2. Igreja Nossa Senhora: 38 doações
   3. Padaria Pão Quente: 32 doações
   4. Empresa Tech Solutions: 28 doações
   5. Farmácia Popular: 25 doações
   6. Loja de Roupas Fashion: 22 doações
   7. João Silva: 18 doações
   8. Maria Santos: 15 doações
   9. Restaurante Sabor: 14 doações
   10. Pedro Costa: 12 doações

📅 DOAÇÕES POR MÊS (Últimos 6 meses)

   2023-08: ██████████████████████████ (78)
   2023-09: ████████████████████████████████ (95)
   2023-10: ████████████████████████████████████ (105)
   2023-11: ██████████████████████████████ (92)
   2023-12: ████████████████████████████████████████ (121)
   2024-01: ███████████████████████████████████████ (98)

============================================================
```

---

### Caso de Uso 5: Validação e Tratamento de Erros

Boas práticas para lidar com erros e validações:

```python
from backend.models.doador import Doador
from backend.models.doacao import Doacao
import streamlit as st

def cadastrar_doador_com_validacao(dados: dict) -> bool:
    """
    Cadastra doador com validação completa e tratamento de erros

    Args:
        dados: Dicionário com dados do doador

    Returns:
        bool: True se sucesso, False se erro
    """
    try:
        # 1. Validações de entrada (frontend)
        if not dados.get('nome'):
            st.error("❌ Nome é obrigatório")
            return False

        if dados.get('nome') and len(dados['nome']) < 3:
            st.error("❌ Nome deve ter pelo menos 3 caracteres")
            return False

        if dados.get('email') and '@' not in dados['email']:
            st.error("❌ Email inválido")
            return False

        if dados.get('estado') and len(dados['estado']) != 2:
            st.error("❌ Estado deve ter 2 caracteres (ex: MG)")
            return False

        if dados.get('cep'):
            cep_limpo = dados['cep'].replace('-', '').replace('.', '')
            if len(cep_limpo) != 8 or not cep_limpo.isdigit():
                st.error("❌ CEP deve ter 8 dígitos")
                return False

        # 2. Criar objeto doador
        doador = Doador(
            nome=dados['nome'].strip(),
            email=dados.get('email', '').strip() or None,
            telefone=dados.get('telefone', '').strip() or None,
            logradouro=dados.get('logradouro', '').strip() or None,
            numero=dados.get('numero', '').strip() or None,
            complemento=dados.get('complemento', '').strip() or None,
            bairro=dados.get('bairro', '').strip() or None,
            cidade=dados.get('cidade', '').strip() or None,
            estado=dados.get('estado', '').strip().upper() or None,
            cep=dados.get('cep', '').strip() or None
        )

        # 3. Validação do model
        valido, erro = doador.validate()
        if not valido:
            st.error(f"❌ {erro}")
            return False

        # 4. Verificar duplicidade (email)
        if doador.email:
            existentes = Doador.get_all()
            for existente in existentes:
                if existente.email == doador.email:
                    st.warning(f"⚠️ Já existe um doador com email {doador.email}")
                    return False

        # 5. Salvar
        if doador.save():
            st.success(f"✅ Doador {doador.nome} cadastrado com sucesso!")
            st.info(f"ID: {doador.idDoador}")
            return True
        else:
            st.error("❌ Erro ao salvar no banco de dados")
            return False

    except Exception as e:
        st.error(f"❌ Erro inesperado: {str(e)}")
        print(f"ERRO: {e}")  # Log para debug
        return False


# ========== EXEMPLO DE USO NO STREAMLIT ==========

def pagina_cadastro_doador():
    """Página de cadastro com validação completa"""
    st.title("👤 Cadastro de Doador")

    with st.form("form_doador"):
        st.subheader("Dados Pessoais")
        nome = st.text_input("Nome Completo*")
        email = st.text_input("Email")
        telefone = st.text_input("Telefone")

        st.subheader("Endereço")
        col1, col2 = st.columns([3, 1])
        with col1:
            logradouro = st.text_input("Logradouro")
        with col2:
            numero = st.text_input("Número")

        complemento = st.text_input("Complemento")

        col1, col2, col3 = st.columns(3)
        with col1:
            bairro = st.text_input("Bairro")
        with col2:
            cidade = st.text_input("Cidade")
        with col3:
            estado = st.text_input("Estado (UF)")

        cep = st.text_input("CEP")

        submitted = st.form_submit_button("💾 Salvar")

        if submitted:
            # Montar dicionário de dados
            dados = {
                'nome': nome,
                'email': email,
                'telefone': telefone,
                'logradouro': logradouro,
                'numero': numero,
                'complemento': complemento,
                'bairro': bairro,
                'cidade': cidade,
                'estado': estado,
                'cep': cep
            }

            # Cadastrar com validação
            if cadastrar_doador_com_validacao(dados):
                # Limpar campos após sucesso
                st.rerun()


# ========== EXEMPLO: Tratamento de Erros em Operações CRUD ==========

def atualizar_doador_seguro(doador_id: int, novos_dados: dict):
    """Atualiza doador com tratamento de erros"""
    try:
        # 1. Buscar doador existente
        doador = Doador.get_by_id(doador_id)
        if not doador:
            return False, "Doador não encontrado"

        # 2. Atualizar campos
        for campo, valor in novos_dados.items():
            if hasattr(doador, campo) and valor is not None:
                setattr(doador, campo, valor)

        # 3. Validar
        valido, erro = doador.validate()
        if not valido:
            return False, erro

        # 4. Atualizar
        if doador.update():
            return True, "Atualizado com sucesso"
        else:
            return False, "Erro ao atualizar"

    except Exception as e:
        return False, f"Erro: {str(e)}"


# Uso:
sucesso, msg = atualizar_doador_seguro(
    doador_id=1,
    novos_dados={'email': 'novo@email.com', 'telefone': '(11) 99999-9999'}
)

if sucesso:
    print(f"✅ {msg}")
else:
    print(f"❌ {msg}")
```

---

## 📚 Referências

- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [MySQL Connector Python](https://dev.mysql.com/doc/connector-python/en/)
- [Context Managers](https://docs.python.org/3/library/contextlib.html)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)

---

## 💡 Dicas Finais

### Performance

- Use `get_by_id()` quando souber o ID específico
- Prefira queries com filtros a buscar tudo e filtrar em Python
- Use índices nas colunas mais consultadas

### Segurança

- Sempre valide dados de entrada
- Use prepared statements (já implementado nos models)
- Nunca confie em dados do usuário sem validação

### Manutenibilidade

- Siga o padrão existente ao criar novos models
- Documente métodos complexos
- Use type hints consistentemente
- Escreva testes para novos métodos

---

[⬅️ Voltar ao Índice](./INDEX.md) | [➡️ Próximo: Frontend](./FRONTEND.md)
