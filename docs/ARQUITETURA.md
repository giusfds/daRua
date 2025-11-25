# 🏗️ Arquitetura do Sistema - Somos DaRua

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Arquitetura em Camadas](#arquitetura-em-camadas)
- [Estrutura de Diretórios](#estrutura-de-diretórios)
- [Fluxo de Dados](#fluxo-de-dados)
- [Padrões de Projeto](#padrões-de-projeto)
- [Componentes do Sistema](#componentes-do-sistema)
- [Diagrama de Componentes](#diagrama-de-componentes)

---

## 🎯 Visão Geral

O sistema Somos DaRua segue uma **arquitetura em camadas** (layered architecture) que separa responsabilidades e facilita a manutenção e evolução do código.

### Princípios Arquiteturais

1. **Separação de Responsabilidades**: Cada camada tem uma função específica
2. **Baixo Acoplamento**: Componentes independentes e reutilizáveis
3. **Alta Coesão**: Funcionalidades relacionadas agrupadas
4. **DRY (Don't Repeat Yourself)**: Código reutilizável em componentes
5. **Single Responsibility**: Cada classe/módulo tem uma única responsabilidade

---

## 🏢 Arquitetura em Camadas

```
┌─────────────────────────────────────────────────────────┐
│                 CAMADA DE APRESENTAÇÃO                   │
│                    (Frontend - Streamlit)                │
│  ┌─────────────────────────────────────────────────┐    │
│  │  main.py (Dashboard)                            │    │
│  │  pages/ (Páginas específicas)                   │    │
│  │  components/ (Componentes reutilizáveis)        │    │
│  └─────────────────────────────────────────────────┘    │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────┐
│                 CAMADA DE NEGÓCIO                        │
│                 (Business Logic - Models)                │
│  ┌─────────────────────────────────────────────────┐    │
│  │  models/ (Entidades do domínio)                 │    │
│  │  - Doador, Beneficiario, Doacao, etc.          │    │
│  │  - Validações de negócio                        │    │
│  │  - Operações CRUD                               │    │
│  └─────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────┐    │
│  │  services/ (Regras complexas)                   │    │
│  │  - Lógica de negócio avançada                   │    │
│  │  - Orquestração de múltiplos models             │    │
│  └─────────────────────────────────────────────────┘    │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────┐
│              CAMADA DE PERSISTÊNCIA                      │
│                  (Data Access Layer)                     │
│  ┌─────────────────────────────────────────────────┐    │
│  │  database/connection.py                         │    │
│  │  - Gerenciamento de conexões                    │    │
│  │  - Pool de conexões                             │    │
│  │  - Transações                                   │    │
│  └─────────────────────────────────────────────────┘    │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────┐
│                    BANCO DE DADOS                        │
│                      (MySQL 8.0)                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │  Tabelas, Índices, Constraints                  │    │
│  │  Stored Procedures, Triggers                    │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 Estrutura de Diretórios Detalhada

```
somos-darua/
│
├── 📱 app/                          # CAMADA DE APRESENTAÇÃO
│   ├── main.py                      # Dashboard principal
│   │   ├── Renderização de métricas
│   │   ├── Gráficos interativos
│   │   └── Navegação principal
│   │
│   ├── pages/                       # Páginas do sistema
│   │   ├── 2_doadores.py           # CRUD de doadores
│   │   ├── 3_beneficiarios.py      # CRUD de beneficiários
│   │   ├── 4_doacoes.py            # Gestão de doações
│   │   ├── 5_campanhas.py          # Gestão de campanhas
│   │   ├── 6_pontos_coleta.py      # Pontos de coleta
│   │   ├── 7_voluntarios.py        # Gestão de voluntários
│   │   └── 8_relatorios.py         # Relatórios e análises
│   │
│   ├── components/                  # Componentes reutilizáveis
│   │   └── forms.py                # Formulários padronizados
│   │
│   └── utils/                       # Utilitários do frontend
│       ├── config.py               # Configurações globais
│       │   ├── Estilos CSS
│       │   ├── Cores e temas
│       │   ├── Funções auxiliares
│       │   └── Sidebar comum
│       └── mock_data.py            # Dados mockados (desenvolvimento)
│
├── 🔧 backend/                      # CAMADA DE NEGÓCIO E DADOS
│   ├── models/                      # Modelos de domínio
│   │   ├── base_model.py           # Classe base (herança)
│   │   ├── doador.py               # Model Doador
│   │   │   ├── __init__()
│   │   │   ├── validate()
│   │   │   ├── save()
│   │   │   ├── update()
│   │   │   ├── delete()
│   │   │   ├── get_by_id()
│   │   │   ├── get_all()
│   │   │   └── search()
│   │   │
│   │   ├── beneficiario.py         # Model Beneficiário
│   │   ├── doacao.py               # Model Doação
│   │   ├── campanha_doacao.py      # Model Campanha
│   │   ├── ponto_coleta.py         # Model Ponto de Coleta
│   │   ├── voluntario.py           # Model Voluntário
│   │   ├── objeto_doavel.py        # Model Objeto Doável
│   │   └── necessidade.py          # Model Necessidade
│   │
│   ├── services/                    # Regras de negócio complexas
│   │   ├── doacao_service.py       # Lógica de doações
│   │   │   ├── Criar doação com múltiplos itens
│   │   │   ├── Vincular beneficiários
│   │   │   └── Atualizar status
│   │   │
│   │   └── relatorio_service.py    # Geração de relatórios
│   │       ├── Relatórios de período
│   │       ├── Análises estatísticas
│   │       └── Exportação de dados
│   │
│   └── database/                    # Camada de persistência
│       ├── __init__.py
│       ├── connection.py            # Gerenciador de conexões
│       │   ├── DatabaseConnection (Context Manager)
│       │   ├── connect()
│       │   ├── disconnect()
│       │   ├── execute_query()
│       │   ├── fetch_all()
│       │   ├── fetch_one()
│       │   └── get_last_insert_id()
│       │
│       └── setup.py                 # Setup do banco
│           ├── Criar database
│           ├── Criar tabelas
│           └── Popular dados iniciais
│
├── 🗄️ database/                     # SCHEMAS E MIGRATIONS
│   ├── schema/                      # DDL - Definição de estrutura
│   │   └── create_database.sql     # Script de criação completo
│   │       ├── DROP DATABASE
│   │       ├── CREATE DATABASE
│   │       ├── CREATE TABLES
│   │       ├── FOREIGN KEYS
│   │       ├── INDEXES
│   │       └── CONSTRAINTS
│   │
│   ├── seeds/                       # Dados iniciais
│   │   └── sample_data.sql         # Dados de exemplo
│   │
│   └── migrations/                  # Alterações de schema
│       └── [versões futuras]
│
├── 🎨 assets/                       # Recursos estáticos
│   ├── images/                      # Imagens do sistema
│   └── icons/                       # Ícones
│
├── 📖 docs/                         # Documentação
│   ├── INDEX.md                     # Índice principal
│   ├── ARQUITETURA.md              # Este arquivo
│   ├── DATABASE.md                  # Documentação do BD
│   ├── DESENVOLVIMENTO.md           # Guia de dev
│   └── API.md                       # Docs de models
│
├── 📄 Arquivos de Configuração
│   ├── .env                         # Variáveis de ambiente (não versionado)
│   ├── .env.example                 # Exemplo de .env
│   ├── .gitignore                   # Arquivos ignorados
│   ├── requirements.txt             # Dependências Python
│   ├── run.sh                       # Script de execução (Linux/Mac)
│   ├── run.bat                      # Script de execução (Windows)
│   ├── README.md                    # Documentação principal
│   └── LICENSE                      # Licença do projeto
│
└── 🧪 tests/                        # Testes (futuro)
    ├── unit/                        # Testes unitários
    ├── integration/                 # Testes de integração
    └── e2e/                         # Testes end-to-end
```

---

## 🔄 Fluxo de Dados

### Exemplo: Cadastro de Doador

```
┌─────────────┐
│   Usuário   │
└──────┬──────┘
       │ 1. Preenche formulário
       ↓
┌─────────────────────────────┐
│  pages/2_doadores.py        │
│  (Camada de Apresentação)   │
│  - Valida campos obrigatórios
│  - Formata dados            │
└──────┬──────────────────────┘
       │ 2. Chama Model
       ↓
┌─────────────────────────────┐
│  models/doador.py           │
│  (Camada de Negócio)        │
│  - Cria instância Doador    │
│  - Executa validações       │
│  - Chama save()             │
└──────┬──────────────────────┘
       │ 3. Executa query SQL
       ↓
┌─────────────────────────────┐
│  database/connection.py     │
│  (Camada de Persistência)   │
│  - Abre conexão             │
│  - Executa INSERT           │
│  - Retorna ID gerado        │
│  - Fecha conexão            │
└──────┬──────────────────────┘
       │ 4. Persiste dados
       ↓
┌─────────────────────────────┐
│  MySQL Database             │
│  - Tabela Doador            │
└─────────────────────────────┘
       │
       │ 5. Retorna sucesso
       ↓
┌─────────────────────────────┐
│  Usuário recebe confirmação │
└─────────────────────────────┘
```

### Exemplo: Consulta com Joins

```
┌─────────────┐
│   Usuário   │
└──────┬──────┘
       │ 1. Acessa relatório
       ↓
┌─────────────────────────────┐
│  pages/8_relatorios.py      │
│  - Seleciona filtros        │
└──────┬──────────────────────┘
       │ 2. Chama Service
       ↓
┌─────────────────────────────┐
│  services/relatorio_service.py
│  - Monta query complexa     │
│  - Aplica filtros           │
└──────┬──────────────────────┘
       │ 3. Executa consulta
       ↓
┌─────────────────────────────┐
│  database/connection.py     │
│  - Executa SELECT com JOINs │
│  - Retorna resultados       │
└──────┬──────────────────────┘
       │ 4. Busca dados
       ↓
┌─────────────────────────────┐
│  MySQL Database             │
│  - Múltiplas tabelas        │
└──────┬──────────────────────┘
       │ 5. Retorna dataset
       ↓
┌─────────────────────────────┐
│  Service processa dados     │
│  - Agrupa                   │
│  - Calcula métricas         │
└──────┬──────────────────────┘
       │ 6. Renderiza
       ↓
┌─────────────────────────────┐
│  Página exibe gráficos      │
│  e tabelas (Plotly/Pandas)  │
└─────────────────────────────┘
```

---

## 🎨 Padrões de Projeto

### 1. **MVC (Model-View-Controller)** Adaptado

- **Model** (`backend/models/`): Lógica de negócio e dados
- **View** (`app/pages/`): Interface com usuário
- **Controller**: Implícito nas páginas Streamlit

### 2. **Repository Pattern** (Parcial)

Os Models funcionam como repositories, encapsulando acesso a dados:

```python
class Doador:
    @staticmethod
    def get_all() -> List['Doador']:
        """Busca todos os doadores"""
        # Acesso ao banco abstraído

    @staticmethod
    def get_by_id(id: int) -> Optional['Doador']:
        """Busca doador por ID"""
```

### 3. **Context Manager** (for database connections)

```python
with DatabaseConnection() as db:
    result = db.execute_query(query, params)
    # Conexão fechada automaticamente
```

**Benefícios:**

- Conexões sempre fechadas
- Tratamento automático de exceções
- Código mais limpo

### 4. **Singleton Pattern** (Database Config)

Configurações do banco são centralizadas:

```python
class DatabaseConnection:
    def __init__(self):
        self.config = {
            'host': os.getenv('DB_HOST'),
            # ...
        }
```

### 5. **Factory Pattern** (Forms)

Componentes reutilizáveis para criação de formulários:

```python
def criar_form_doador(valores_iniciais=None):
    """Factory para formulário de doador"""
    # Cria formulário padronizado
```

### 6. **Strategy Pattern** (Validações)

Validações específicas por tipo de entidade:

```python
class Doador:
    def validate(self) -> tuple[bool, str]:
        """Estratégia de validação para Doador"""

class Beneficiario:
    def validate(self) -> tuple[bool, str]:
        """Estratégia de validação para Beneficiário"""
```

---

## 🧩 Componentes do Sistema

### 1. Frontend (Streamlit)

**Responsabilidades:**

- Renderização da interface
- Captura de entrada do usuário
- Exibição de feedback
- Navegação entre páginas

**Tecnologias:**

- Streamlit (framework web)
- Plotly (gráficos)
- Pandas (manipulação de dados)

### 2. Models (Business Logic)

**Responsabilidades:**

- Representar entidades do domínio
- Validações de negócio
- Operações CRUD
- Encapsular regras de negócio

**Padrão:**

```python
class EntidadeBase:
    def __init__(self, **kwargs)
    def validate(self) -> tuple[bool, str]
    def save(self) -> bool
    def update(self) -> bool
    def delete(self) -> bool

    @staticmethod
    def get_all() -> List

    @staticmethod
    def get_by_id(id: int) -> Optional
```

### 3. Services (Business Rules)

**Responsabilidades:**

- Orquestrar múltiplos models
- Lógica de negócio complexa
- Transações que envolvem várias entidades

**Exemplo:**

```python
class DoacaoService:
    @staticmethod
    def criar_doacao_completa(doacao_data, objetos, beneficiarios):
        """
        Cria doação vinculando múltiplos objetos e beneficiários
        """
        # 1. Criar doação
        # 2. Adicionar objetos
        # 3. Vincular beneficiários
        # 4. Registrar histórico
```

### 4. Database Layer

**Responsabilidades:**

- Gerenciar conexões
- Executar queries
- Transações
- Pool de conexões

**Padrão Context Manager:**

```python
with DatabaseConnection() as db:
    db.execute_query(sql, params)
```

### 5. Utilities

**Responsabilidades:**

- Funções auxiliares
- Configurações globais
- Helpers de formatação
- Estilos CSS

---

## 📊 Diagrama de Componentes

```
┌──────────────────────────────────────────────────────────────┐
│                        STREAMLIT APP                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │ Dashboard  │  │  Páginas   │  │ Components │            │
│  │  main.py   │  │   CRUD     │  │   forms    │            │
│  └─────┬──────┘  └──────┬─────┘  └──────┬─────┘            │
│        │                │               │                   │
│        └────────────────┴───────────────┘                   │
│                         │                                    │
└─────────────────────────┼────────────────────────────────────┘
                          │
                          ↓
┌──────────────────────────────────────────────────────────────┐
│                     BACKEND LAYER                            │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────┐       ┌──────────────────────┐      │
│  │      MODELS        │       │      SERVICES        │      │
│  ├────────────────────┤       ├──────────────────────┤      │
│  │ • Doador          │       │ • DoacaoService      │      │
│  │ • Beneficiario    │◄──────┤ • RelatorioService   │      │
│  │ • Doacao          │       │ • NotificacaoService │      │
│  │ • Campanha        │       └──────────────────────┘      │
│  │ • PontoColeta     │                                      │
│  │ • Voluntario      │                                      │
│  └─────────┬──────────┘                                     │
│            │                                                 │
└────────────┼─────────────────────────────────────────────────┘
             │
             ↓
┌──────────────────────────────────────────────────────────────┐
│                   DATABASE LAYER                             │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────────────────┐         │
│  │       DatabaseConnection                       │         │
│  ├────────────────────────────────────────────────┤         │
│  │ • connect()                                    │         │
│  │ • disconnect()                                 │         │
│  │ • execute_query(sql, params)                   │         │
│  │ • fetch_all(sql, params)                       │         │
│  │ • fetch_one(sql, params)                       │         │
│  │ • Context Manager (__enter__, __exit__)        │         │
│  └─────────────────────┬──────────────────────────┘         │
│                        │                                     │
└────────────────────────┼─────────────────────────────────────┘
                         │
                         ↓
┌──────────────────────────────────────────────────────────────┐
│                      MySQL 8.0                               │
├──────────────────────────────────────────────────────────────┤
│  Database: somos_darua                                       │
│  ┌────────────────────────────────────────────────┐         │
│  │  Tables:                                       │         │
│  │  • Doador                                      │         │
│  │  • Beneficiario                                │         │
│  │  • Doacao                                      │         │
│  │  • CampanhaDoacao                              │         │
│  │  • PontoColeta                                 │         │
│  │  • Voluntario                                  │         │
│  │  • ObjetoDoavel                                │         │
│  │  • Necessidade                                 │         │
│  │  • Contem (N:N)                                │         │
│  │  • Recebe (N:N)                                │         │
│  └────────────────────────────────────────────────┘         │
└──────────────────────────────────────────────────────────────┘
```

---

## 🔐 Segurança e Boas Práticas

### 1. Variáveis de Ambiente

```python
# ✅ CORRETO
from dotenv import load_dotenv
load_dotenv()
db_password = os.getenv('DB_PASSWORD')

# ❌ ERRADO
db_password = "senha123"  # Nunca hardcode credenciais
```

### 2. SQL Injection Prevention

```python
# ✅ CORRETO - Usa prepared statements
query = "SELECT * FROM Doador WHERE idDoador = %s"
db.execute_query(query, (id,))

# ❌ ERRADO - Vulnerável a SQL injection
query = f"SELECT * FROM Doador WHERE idDoador = {id}"
```

### 3. Tratamento de Erros

```python
# ✅ CORRETO
try:
    doador.save()
except DatabaseError as e:
    st.error(f"Erro ao salvar: {e}")
    logger.error(f"Database error: {e}")
```

### 4. Validações em Múltiplas Camadas

```
Frontend (Streamlit) → Validação de UI (campos obrigatórios)
         ↓
Model (Python)       → Validação de negócio
         ↓
Database (MySQL)     → Constraints e triggers
```

---

## 📈 Escalabilidade

### Preparação para Crescimento

1. **Pool de Conexões**: Implementar pool para múltiplos usuários
2. **Cache**: Redis para consultas frequentes
3. **API REST**: Separar backend em API independente
4. **Microserviços**: Dividir em serviços menores quando necessário

### Otimizações Futuras

- [ ] Implementar cache de queries
- [ ] Adicionar índices otimizados
- [ ] Lazy loading de dados
- [ ] Paginação em listas grandes
- [ ] Compressão de dados
- [ ] CDN para assets estáticos

---

## 🧪 Testabilidade

A arquitetura facilita testes em cada camada:

```python
# Teste de Model (unitário)
def test_doador_validation():
    doador = Doador(nome="")
    valido, erro = doador.validate()
    assert not valido

# Teste de Service (integração)
def test_criar_doacao_completa():
    service = DoacaoService()
    resultado = service.criar_doacao_completa(...)
    assert resultado.sucesso

# Teste de Database (integração)
def test_database_connection():
    with DatabaseConnection() as db:
        assert db.connection.is_connected()
```

---

## 📚 Referências

- [Streamlit Documentation](https://docs.streamlit.io/)
- [MySQL Best Practices](https://dev.mysql.com/doc/)
- [Python Design Patterns](https://refactoring.guru/design-patterns/python)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

---

[⬅️ Voltar ao Índice](./INDEX.md) | [➡️ Próximo: Banco de Dados](./DATABASE.md)
