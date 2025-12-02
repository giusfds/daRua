# 🤝 Sistema Somos DaRua - Gestão de Doações

> **Sistema completo de gestão de doações para organizações sociais que atendem pessoas em situação de vulnerabilidade**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-red.svg)](https://streamlit.io/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-Academic-green.svg)]()
[![Code Style](https://img.shields.io/badge/code%20style-PEP8-black)](https://www.python.org/dev/peps/pep-0008/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## 📑 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades Principais](#-funcionalidades-principais)
- [Arquitetura do Sistema](#-arquitetura-do-sistema)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Estrutura do Banco de Dados](#-estrutura-do-banco-de-dados)
- [Guia de Instalação](#-guia-de-instalação)
- [Como Usar](#-como-usar)
- [Páginas do Sistema](#-páginas-do-sistema)
- [Fluxos de Trabalho](#-fluxos-de-trabalho)
- [Estrutura de Diretórios](#-estrutura-de-diretórios)
- [Desenvolvimento](#-desenvolvimento)
- [Como Contribuir](#-como-contribuir)
- [Equipe](#-equipe)

---

## 🎯 Sobre o Projeto

O **Somos DaRua** é um sistema web desenvolvido para facilitar a gestão de doações em organizações sociais. O projeto foi criado como parte de um trabalho acadêmico de extensão universitária e simula um ambiente real de gerenciamento de doações.

### 🌟 Problema Resolvido

Organizações sociais frequentemente enfrentam dificuldades para:

- Rastrear o histórico de doações
- Associar itens específicos às necessidades de beneficiários
- Coordenar a logística de entrega
- Gerenciar campanhas de arrecadação
- Controlar prazos e distribuição

### 💡 Solução Proposta

Um sistema centralizado que permite:

- ✅ Cadastro completo de doadores, beneficiários e voluntários
- ✅ Registro detalhado de doações (tipo, quantidade, origem)
- ✅ Sistema de duas fases (recebimento → distribuição)
- ✅ Gerenciamento de campanhas com metas
- ✅ Relatórios e estatísticas em tempo real
- ✅ Controle de pontos de coleta

---

## 🚀 Funcionalidades Principais

### 1. Gestão de Doadores

- Cadastro completo com dados de contato e endereço
- Busca e filtros avançados
- Histórico de doações por doador
- Edição e exclusão segura

### 2. Sistema de Doações (Duas Fases)

#### **Fase 1: Recebimento**

```
Doador entrega → Ponto de Coleta → Voluntário registra → Status: "Recebida"
```

- Registro de tipo, item, quantidade e unidade
- Vinculação opcional com campanhas
- Observações e previsão de entrega

#### **Fase 2: Distribuição**

```
Doação "Recebida" → Seleciona beneficiários → Voluntários entregam → Status: "Distribuída"
```

- Associação com múltiplos beneficiários
- Seleção de voluntários distribuidores
- Atualização automática de status

### 3. Campanhas de Doação

- Criação com nome, descrição e período
- Definição de metas (R$, Kg, Unidades, etc.)
- Acompanhamento de progresso em tempo real
- Barra de progresso visual

### 4. Dashboard e Relatórios

- Métricas principais atualizadas em tempo real
- Gráficos interativos (doações por categoria, evolução mensal, ranking)
- Últimas doações registradas
- Relatórios detalhados com filtros

### 5. Gestão de Beneficiários

- Cadastro com idade, gênero e necessidades
- Filtros por status (Ativo, Inativo, Aguardando)
- Histórico de doações recebidas
- Gráficos de distribuição demográfica

### 6. Pontos de Coleta e Voluntários

- Cadastro de locais estratégicos
- Gestão de voluntários e suas atribuições
- Controle de responsáveis

---

## 🏗️ Arquitetura do Sistema

O sistema utiliza uma **arquitetura em 3 camadas**:

```
┌─────────────────────────────────────────┐
│         FRONTEND (Streamlit)            │
│  ┌──────────┐ ┌──────────┐ ┌─────────┐ │
│  │Dashboard │ │Cadastros │ │Relatórios│ │
│  └──────────┘ └──────────┘ └─────────┘ │
└─────────────────┬───────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────┐
│       BACKEND (Models Python)           │
│  ┌──────────┐ ┌──────────┐ ┌─────────┐ │
│  │Validações│ │ Lógica   │ │  CRUD   │ │
│  └──────────┘ └──────────┘ └─────────┘ │
└─────────────────┬───────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────┐
│         DATABASE (MySQL)                │
│  ┌──────────┐ ┌──────────┐ ┌─────────┐ │
│  │  Tabelas │ │   FKs    │ │ Índices │ │
│  └──────────┘ └──────────┘ └─────────┘ │
└─────────────────────────────────────────┘
```

### Camadas Explicadas

#### 🎨 **Frontend (Streamlit)**

- Interface web interativa
- Páginas navegáveis via sidebar
- Gráficos com Plotly
- Formulários de cadastro
- **Localização:** `/app`

#### 🧠 **Backend (Models Python)**

- Classes Python para cada entidade
- Validações de negócio
- Operações CRUD
- Métodos auxiliares
- **Localização:** `/backend/models`

#### 💾 **Database (MySQL)**

- Persistência de dados
- Relacionamentos N:N
- Integridade referencial
- **Localização:** `/database/schema`

---

## 💻 Tecnologias Utilizadas

### Core

- **Python 3.8+** - Linguagem principal
- **Streamlit 1.28+** - Framework web
- **MySQL 8.0+** - Banco de dados relacional

### Bibliotecas Python

```python
streamlit          # Interface web
pandas             # Manipulação de dados
plotly             # Gráficos interativos
mysql-connector    # Conexão com MySQL
python-dotenv      # Variáveis de ambiente
```

### Ferramentas de Desenvolvimento

- **Git** - Controle de versão
- **Figma** - Prototipação da UI
- **MySQL Workbench** - Gerenciamento do banco

---

## 🗄️ Estrutura do Banco de Dados

### Diagrama ER Simplificado

```
┌─────────┐       ┌─────────┐       ┌──────────────┐
│ Doador  │──────>│ Doacao  │<──────│ Beneficiario │
└─────────┘       └─────────┘       └──────────────┘
                       │
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ↓              ↓              ↓
  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │Voluntario│  │Campanha  │  │  Ponto   │
  └──────────┘  └──────────┘  │ Coleta   │
                               └──────────┘
```

### 📊 Tabelas Principais (8)

| Tabela             | Descrição                 | Campos Principais                       |
| ------------------ | ------------------------- | --------------------------------------- |
| **Doador**         | Pessoas/empresas que doam | Nome, Email, Telefone, Endereço         |
| **Beneficiario**   | Quem recebe doações       | Nome, Idade, Gênero, Descrição          |
| **Doacao**         | Registro de doações       | TipoDoacao, Quantidade, Unidade, Status |
| **CampanhaDoacao** | Campanhas organizadas     | Nome, Meta, Arrecadado, Período         |
| **PontoColeta**    | Locais de coleta          | Responsável, Endereço                   |
| **Voluntario**     | Colaboradores             | Nome, Email, Telefone                   |
| **ObjetoDoavel**   | Itens doáveis             | Nome, Categoria                         |
| **Necessidade**    | Necessidades prioritárias | Descrição                               |

### 🔗 Tabelas de Relacionamento N:N (5)

| Tabela      | Relacionamento                | Descrição                    |
| ----------- | ----------------------------- | ---------------------------- |
| **Recebe**  | Beneficiario ↔ Doacao         | Quem recebeu cada doação     |
| **Possui**  | Doacao ↔ Voluntario           | Voluntários que distribuíram |
| **Contem**  | Doacao ↔ ObjetoDoavel         | Itens em cada doação         |
| **Promove** | CampanhaDoacao ↔ Necessidade  | Necessidades de campanhas    |
| **Associa** | ObjetoDoavel ↔ CampanhaDoacao | Objetos vinculados           |

### 🔑 Campos Importantes na Tabela Doacao

```sql
idDoacao                        INT PRIMARY KEY AUTO_INCREMENT
Doador_idDoador                 INT NOT NULL  -- Quem doou
PontoColeta_idPontoColeta       INT NOT NULL  -- Onde foi recebida
VoluntarioColeta_idVoluntario   INT NOT NULL  -- Quem registrou
CampanhaDoacao_idCampanhaDoacao INT NULL      -- Campanha (opcional)
DataCriacao                     DATE          -- Quando foi registrada
DataEntrega                     DATE          -- Quando será/foi entregue
TipoDoacao                      VARCHAR(50)   -- Alimentos, Roupas, etc
DescricaoItem                   VARCHAR(255)  -- Descrição detalhada
Quantidade                      DECIMAL(10,2) -- Quantidade
Unidade                         VARCHAR(20)   -- Kg, Litros, Unidades, R$
Status                          VARCHAR(50)   -- Recebida/Distribuída
Observacoes                     TEXT          -- Observações
```

> **⚠️ IMPORTANTE:** Beneficiário NÃO é campo direto na tabela Doacao!  
> O relacionamento é N:N através da tabela **Recebe**.

---

## 📥 Guia de Instalação

### Pré-requisitos

```bash
✅ Python 3.8 ou superior
✅ MySQL 8.0 ou superior
✅ pip (gerenciador de pacotes Python)
✅ Git (opcional, para clonar o repositório)
```

### Passo 1: Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/somos-darua.git
cd somos-darua
```

### Passo 2: Criar Ambiente Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Passo 3: Instalar Dependências

```bash
pip install -r requirements.txt
```

**Conteúdo do `requirements.txt`:**

```
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.17.0
mysql-connector-python>=8.1.0
python-dotenv>=1.0.0
```

### Passo 4: Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
# .env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha_mysql
DB_NAME=somos_darua
DB_PORT=3306
```

### Passo 5: Criar o Banco de Dados

#### Opção A: Script Automático

```bash
python3 backend/database/setup.py
```

#### Opção B: Manual via MySQL

```bash
mysql -u root -p < database/schema/create_database.sql
```

### Passo 6: Executar Migrations

Execute **na ordem**:

```bash
mysql -u root -p somos_darua < database/migrations/add_doacoes_detalhes.sql
mysql -u root -p somos_darua < database/migrations/add_fks_doacoes.sql
mysql -u root -p somos_darua < database/migrations/add_meta_campanhas.sql
```

### Passo 7: Testar Conexão

```bash
python3 backend/database/connection.py
```

**Saída esperada:**

```
✓ Conectado ao MySQL versão 8.0.xx
✓ Banco atual: somos_darua
✓ Versão MySQL: 8.0.xx
✅ CONEXÃO OK!
```

### Passo 8: Iniciar a Aplicação

```bash
streamlit run app/main.py
```

A aplicação estará disponível em: **http://localhost:8501**

---

## 🎮 Como Usar

### Fluxo Completo: Da Doação até a Distribuição

#### 1️⃣ **Preparação Inicial (Cadastros)**

```
a) Cadastrar Doador
   └─> Página: 👤 Doadores
   └─> Preencher: Nome, Email, Telefone, Endereço
   └─> Clicar: "Cadastrar Novo Doador"

b) Cadastrar Beneficiário
   └─> Página: 🤝 Beneficiários
   └─> Preencher: Nome, Data Nascimento, Gênero, Necessidades
   └─> Clicar: "Cadastrar Novo Beneficiário"

c) Cadastrar Ponto de Coleta
   └─> Página: 📍 Pontos de Coleta
   └─> Preencher: Responsável, Endereço Completo
   └─> Clicar: "Cadastrar Novo Ponto"

d) Cadastrar Voluntário
   └─> Página: 🙋 Voluntários
   └─> Preencher: Nome, Email, Telefone
   └─> Clicar: "Cadastrar Voluntário"

e) Criar Campanha (Opcional)
   └─> Página: 📢 Campanhas
   └─> Preencher: Nome, Descrição, Período, Meta
   └─> Clicar: "Criar Campanha"
```

#### 2️⃣ **Registrar Nova Doação (Fase 1: Recebimento)**

```
1. Ir para: 📦 Doações → Aba "Nova Doação"

2. Preencher identificação:
   ├─ Selecionar: Doador (quem doou)
   ├─ Selecionar: Ponto de Coleta (onde foi recebida)
   └─ Selecionar: Voluntário Responsável (quem registrou)

3. Preencher detalhes da doação:
   ├─ Tipo: Alimentos / Roupas / Medicamentos / Dinheiro / Outros
   ├─ Descrição do Item: "Arroz integral", "Cesta básica", etc
   ├─ Quantidade: 5, 10, 100...
   └─ Unidade: Kg / Litros / Unidades / Caixas / R$

4. Opcional:
   ├─ Vincular a uma Campanha
   ├─ Data Prevista de Entrega
   └─ Observações

5. Clicar: "Registrar Doação"

✅ Status inicial: "Recebida"
```

#### 3️⃣ **Distribuir Doação (Fase 2: Distribuição)**

```
1. Ir para: 📦 Doações → Aba "Distribuir Doação"

2. Selecionar doação:
   └─ Lista mostra apenas doações com status "Recebida"

3. Marcar beneficiários:
   └─ Selecionar um ou mais que receberão a doação

4. Selecionar voluntários distribuidores (opcional):
   └─ Quem fará a entrega

5. Definir data de entrega:
   └─ Quando será entregue

6. Clicar: "Confirmar Distribuição"

✅ Status atualizado automaticamente para: "Distribuída"
✅ Beneficiários associados na tabela Recebe
✅ Voluntários associados na tabela Possui
```

#### 4️⃣ **Acompanhar no Dashboard**

```
1. Ir para: 🏠 Dashboard

2. Ver em tempo real:
   ├─ Total de Doadores
   ├─ Total de Beneficiários
   ├─ Total de Doações
   └─ Campanhas Ativas

3. Analisar gráficos:
   ├─ Doações por Categoria (Pizza)
   ├─ Evolução Mensal (Barras)
   └─ Tendência de Doadores (Linha)

4. Ver últimas 10 doações registradas
```

#### 5️⃣ **Gerar Relatórios**

```
1. Ir para: 📊 Relatórios

2. Definir filtros:
   ├─ Data Início
   ├─ Data Fim
   └─ Tipo de Relatório

3. Visualizar:
   ├─ Estatísticas detalhadas
   ├─ Gráficos comparativos
   └─ Tabelas de dados

4. Exportar (em desenvolvimento):
   └─ PDF / Excel / Email
```

---

## 📄 Páginas do Sistema

### 🏠 Dashboard (main.py)

**Objetivo:** Visão geral do sistema

**Elementos:**

- 4 Cards de métricas principais
- Gráfico de Pizza: Doações por categoria
- Gráfico de Barras: Doações mensais
- Gráfico de Linha: Tendência de doadores
- Tabela: Últimas 10 doações
- Cards de destaques e alertas

**Dados:** Busca em tempo real do MySQL via `dashboard_model.py`

---

### 👤 Doadores (2_doadores.py)

**Objetivo:** CRUD completo de doadores

**Funcionalidades:**

- ➕ Cadastrar novo doador
- 🔍 Buscar por nome/email/telefone
- ✏️ Editar informações
- 🗑️ Excluir (bloqueado se houver doações)
- 📊 Estatísticas: Total, Ativos, Cadastros do mês

**Campos:**

- Nome\* (obrigatório)
- Email, Telefone
- Endereço completo (Rua, Número, Bairro, Cidade, Estado, CEP)

**Validações:**

- Email válido (@)
- Estado com 2 caracteres
- CEP formato 00000-000

---

### 🤝 Beneficiários (3_beneficiarios.py)

**Objetivo:** CRUD completo de beneficiários

**Funcionalidades:**

- ➕ Cadastrar novo beneficiário
- 🔍 Filtrar por status (Ativo/Inativo/Aguardando)
- 🔍 Buscar por nome
- ✏️ Editar informações
- 🗑️ Excluir (bloqueado se houver doações recebidas)
- 📊 Gráficos:
  - Distribuição por status
  - Faixa etária (0-17, 18-29, 30-49, 50-64, 65+)

**Campos:**

- Nome\* (obrigatório)
- Data de Nascimento → Idade (calculada automaticamente)
- Gênero (M/F/O/Prefiro não informar)
- Descrição da situação
- Necessidades (Alimentação, Vestuário, Abrigo, Saúde, Educação)
- Status (Ativo/Inativo/Aguardando)

---

### 📦 Doações (4_doacoes.py)

**Objetivo:** Sistema completo de gestão de doações

**Abas:**

#### **Aba 1: Nova Doação (Recebimento)**

Formulário com 3 seções:

1. **Identificação (Obrigatório)**

   - Doador \*
   - Ponto de Coleta \*
   - Voluntário Responsável \*

2. **Detalhes da Doação**

   - Tipo de Doação \*
   - Descrição do Item \*
   - Quantidade \*
   - Unidade \*

3. **Informações Adicionais (Opcional)**
   - Campanha
   - Data Prevista de Entrega
   - Observações

#### **Aba 2: Distribuir Doação**

1. Seleção (Dropdown com doações "Recebidas")
2. Detalhes da Doação (Exibe informações completas)
3. Beneficiários (Checkboxes para selecionar múltiplos)
4. Voluntários Distribuidores (Opcional)
5. Data de Entrega

**Ao confirmar:**

- ✅ Cria registros na tabela Recebe
- ✅ Cria registros na tabela Possui
- ✅ Atualiza status para "Distribuída"
- ✅ Atualiza data de entrega

#### **Aba 3: Histórico**

- Filtros: Tipo, Status
- Estatísticas: Total, Recebidas, Distribuídas
- Tabela: Todas as doações com detalhes

---

### 📢 Campanhas (5_campanhas.py)

**Objetivo:** Gerenciar campanhas de arrecadação

**Funcionalidades:**

- ➕ Criar nova campanha
- 🔍 Filtrar por status (Ativa/Concluída)
- 🔍 Ordenar por: Mais recentes, Nome, Progresso
- ✏️ Editar campanha
- 🗑️ Excluir (bloqueado se houver doações vinculadas)
- 📊 Cards com barra de progresso e valor faltante

**Campos:**

- Nome* e Descrição*
- Data Início* e Data Término*
- Meta\* (valor numérico)
- Tipo de Meta\* (R$, Kg, Unidades, Litros, Caixas)
- Arrecadado

**Cálculo automático:**

```
Progresso = (Arrecadado / Meta) × 100%
```

---

### 📍 Pontos de Coleta (6_pontos_coleta.py)

**Objetivo:** CRUD de locais de coleta

**Funcionalidades:**

- ➕ Cadastrar novo ponto
- 🔍 Filtrar por status (Ativo/Inativo)
- 🔍 Buscar por nome/endereço
- ✏️ Editar informações
- 🗑️ Excluir (bloqueado se houver objetos cadastrados)
- 📊 Cards visuais com status emoji (🟢/🔴)

**Campos:**

- Responsável\* (obrigatório)
- Endereço completo\*

---

### 🙋 Voluntários (7_voluntarios.py)

**Objetivo:** CRUD de voluntários

**Funcionalidades:**

- ➕ Cadastrar novo voluntário
- 🔍 Filtrar por status e área de atuação
- 🔍 Buscar por nome/email/telefone
- ✏️ Editar informações
- 🗑️ Excluir (bloqueado se associado a doações)

**Campos:**

- Nome*, Email*, Telefone\* (obrigatórios)

**Uso no sistema:**

1. Ao registrar nova doação (voluntário que recebeu)
2. Ao distribuir doação (voluntários que entregarão)

---

### 📊 Relatórios (8_relatorios.py)

**Objetivo:** Análises detalhadas e exportação

**Filtros:**

- Data Início e Fim
- Tipo de Relatório (Visão Geral, Doações, Doadores, Beneficiários, Campanhas)

**Seções:**

1. Visão Geral (Métricas com delta)
2. Análises Detalhadas (Gráficos)
3. Tabelas Detalhadas (3 abas)
4. Exportação (Planejado: PDF/Excel/Email)

---

## 🔄 Fluxos de Trabalho

### Fluxo 1: Ciclo Completo de uma Doação

```
1. Cadastrar Doador
2. Cadastrar Beneficiário
3. Cadastrar Ponto de Coleta
4. Cadastrar Voluntário
5. Registrar Nova Doação (Status: Recebida)
6. Distribuir Doação
7. Selecionar Beneficiários
8. Selecionar Voluntários
9. Status atualizado automaticamente: Distribuída
10. Visualizar no Dashboard
```

### Fluxo 2: Gerenciamento de Campanha

```
1. Criar Campanha
2. Definir Meta
3. Vincular Doações à Campanha
4. Atualizar Arrecadado
5. Acompanhar Progresso
6. Encerrar quando atingir meta ou prazo
```

---

## 📁 Estrutura de Diretórios

```
somos-darua/
│
├── app/                          # Frontend Streamlit
│   ├── main.py                   # 🏠 Dashboard
│   ├── pages/                    # Páginas navegáveis
│   │   ├── 2_doadores.py         # 👤 CRUD Doadores
│   │   ├── 3_beneficiarios.py    # 🤝 CRUD Beneficiários
│   │   ├── 4_doacoes.py          # 📦 Sistema de Doações
│   │   ├── 5_campanhas.py        # 📢 CRUD Campanhas
│   │   ├── 6_pontos_coleta.py    # 📍 CRUD Pontos de Coleta
│   │   ├── 7_voluntarios.py      # 🙋 CRUD Voluntários
│   │   └── 8_relatorios.py       # 📊 Relatórios
│   │
│   └── utils/                    # Utilitários
│       ├── config.py             # ⚙️ Configurações centralizadas
│       └── mock_data.py          # 🎭 Dados fictícios (desativado)
│
├── backend/                      # Backend Python
│   ├── models/                   # 🧠 Lógica de negócio
│   │   ├── doador.py
│   │   ├── beneficiario.py
│   │   ├── doacao.py             # (Modelo mais complexo)
│   │   ├── campanha_doacao.py
│   │   ├── ponto_coleta.py
│   │   ├── voluntario.py
│   │   ├── objeto_doavel.py
│   │   ├── necessidade.py
│   │   └── dashboard_model.py    # 📊 Queries agregadas
│   │
│   └── database/                 # 💾 Camada de dados
│       ├── connection.py         # Conexão MySQL
│       └── setup.py              # Script de criação
│
├── database/                     # 🗄️ Estrutura do banco
│   ├── schema/
│   │   └── create_database.sql   # Script completo
│   ├── migrations/               # Atualizações incrementais
│   │   ├── add_doacoes_detalhes.sql
│   │   ├── add_fks_doacoes.sql
│   │   └── add_meta_campanhas.sql
│   └── seeds/                    # Dados de teste (vazio)
│
├── assents/                      # Recursos estáticos
│   ├── icons/
│   └── images/
│
├── .env                          # ⚙️ Variáveis de ambiente
├── requirements.txt              # 📦 Dependências
├── README.md                     # 📖 Este arquivo
└── Extencionista__BD.pdf         # 📄 Relatório do projeto
```

---

## 🛠️ Desenvolvimento

### Padrão de Código

#### 1. Validações Duplas

```python
# Frontend (Streamlit)
if not nome:
    st.error("Nome é obrigatório")

# Backend (Model)
def validate(self):
    if not self.nome:
        return False, "Nome é obrigatório"
    return True, ""
```

#### 2. Context Manager para Database

```python
# Sempre usar 'with' para garantir fechamento
with DatabaseConnection() as db:
    result = db.fetch_one(query, params)
```

#### 3. Tratamento de Erros

```python
try:
    if objeto.save():
        show_success_message("✅ Salvo com sucesso!")
except Exception as e:
    if "foreign key" in str(e).lower():
        show_error_message("❌ Não pode excluir: possui vínculos")
    else:
        show_error_message(f"❌ Erro: {str(e)}")
```

#### 4. Nomenclatura

- **Variáveis:** snake_case (`total_doadores`)
- **Classes:** PascalCase (`DashboardModel`)
- **Funções:** snake_case (`get_metricas_dashboard`)
- **Constantes:** UPPER_SNAKE_CASE (`COLORS`)

### Boas Práticas Implementadas

- ✅ Separação de responsabilidades (Frontend/Backend/Database)
- ✅ Configuração centralizada
- ✅ Validações em camadas
- ✅ Relacionamentos N:N
- ✅ Status calculado automaticamente
- ✅ Context managers
- ✅ Transações para integridade

---

## 🐛 Troubleshooting

### Problema: "Connection refused" ao conectar MySQL

**Solução:**

```bash
# Verificar se MySQL está rodando
sudo systemctl status mysql

# Iniciar MySQL
sudo systemctl start mysql
```

### Problema: "Module not found"

**Solução:**

```bash
# Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstalar dependências
pip install -r requirements.txt
```

### Problema: "Table doesn't exist"

**Solução:**

```bash
# Recriar banco
python3 backend/database/setup.py

# Rodar migrations na ordem
mysql -u root -p somos_darua < database/migrations/add_doacoes_detalhes.sql
mysql -u root -p somos_darua < database/migrations/add_fks_doacoes.sql
mysql -u root -p somos_darua < database/migrations/add_meta_campanhas.sql
```

### Problema: Dashboard mostra dados vazios

**Solução:**

- Verificar se migrations foram executadas
- Cadastrar dados de teste manualmente nas páginas

---

## 📚 Conceitos Aprendidos

### 1. Arquitetura em Camadas

Separação clara: Frontend → Backend → Database

### 2. ORM Manual

Classes Python espelham tabelas MySQL

### 3. Relacionamentos N:N

Uso de tabelas intermediárias (Recebe, Possui, etc)

### 4. Transações

Garantem integridade em operações complexas

### 5. Context Managers

Garantem fechamento de recursos (`with`)

### 6. Status Calculado

Evita inconsistências no banco

### 7. Validações Duplas

Frontend (UX) + Backend (Segurança)

---

## 🚧 Melhorias Futuras

### Fase 1: Funcionalidades Essenciais

- [ ] Sistema de autenticação (login/logout)
- [ ] Gestão de permissões (admin/voluntário)
- [ ] Exportação de relatórios (PDF/Excel)
- [ ] Notificações por email
- [ ] Upload de fotos das doações

### Fase 2: Melhorias de UX

- [ ] Dashboard personalizável
- [ ] Filtros avançados
- [ ] Busca global
- [ ] Histórico de alterações
- [ ] Modo claro/escuro

### Fase 3: Integrações

- [ ] API REST para mobile
- [ ] Integração com WhatsApp
- [ ] Google Maps (pontos de coleta)
- [ ] QR Code para rastreamento
- [ ] Certificados de doação

### Fase 4: Analytics

- [ ] Previsão de demanda (IA)
- [ ] Sugestão de campanhas
- [ ] Relatórios comparativos
- [ ] Dashboards interativos

---

## 👥 Equipe

### Desenvolvimento

- **Giuseppe Cordeiro** - Desenvolvedor
- **Pedro Henrique** - Desenvolvedor
- **Pedro Tinoco** - Desenvolvedor e Documentação
- **Savio Faria** - Desenvolvedor

### Instituição

- **Curso** - Ciência da Computação
- **Disciplina** - Projeto Extensionista
- **Ano** - 2024/2025

---

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos como parte de um projeto extensionista.

**Uso Acadêmico** - Permitido para:

- ✅ Estudo e aprendizado
- ✅ Adaptação para projetos similares
- ✅ Referência em trabalhos acadêmicos

**Uso Comercial** - Requer autorização prévia dos autores.

---

## 🙏 Agradecimentos

Agradecimentos especiais a:

- 👨‍🏫 Professor Orientador pela orientação
- 🏢 Organizações sociais que inspiraram o projeto
- 📚 Comunidade open-source pelas ferramentas
- 🤝 Colegas de turma pelo suporte

---

## 🤝 Como Contribuir

Adoramos contribuições! Quer ajudar a melhorar o Somos DaRua? Veja como:

### 📋 Formas de Contribuir

- 🐛 **Reportar bugs**: Encontrou um erro? [Abra uma issue](https://github.com/giusfds/DaRua/issues/new)
- 💡 **Sugerir melhorias**: Tem uma ideia? Compartilhe conosco!
- 📝 **Melhorar documentação**: Sempre há espaço para melhorias
- 💻 **Desenvolver código**: Implemente funcionalidades ou corrija bugs
- 🧪 **Escrever testes**: Aumente a cobertura de testes

### 🚀 Início Rápido

```bash
# 1. Fork o repositório
# 2. Clone seu fork
git clone https://github.com/SEU-USUARIO/DaRua.git

# 3. Crie uma branch
git checkout -b feature/minha-contribuicao

# 4. Faça suas mudanças e commit
git commit -m "feat: adiciona nova funcionalidade"

# 5. Push e abra um Pull Request
git push origin feature/minha-contribuicao
```

### 📚 Guias

Para informações detalhadas sobre o processo de contribuição:

- **[CONTRIBUTING.md](CONTRIBUTING.md)**: Guia completo de contribuição
- **[docs/DESENVOLVIMENTO.md](docs/DESENVOLVIMENTO.md)**: Setup do ambiente de desenvolvimento
- **[docs/TESTES.md](docs/TESTES.md)**: Como escrever e executar testes

### 📜 Padrões de Código

Seguimos os padrões da comunidade Python:

- **PEP 8**: Estilo de código Python
- **Type hints**: Use anotações de tipo
- **Docstrings**: Documente funções e classes
- **Conventional Commits**: Formato padronizado de commits

Exemplo de commit:

```bash
feat(doadores): adiciona filtro por cidade
fix(validacao): corrige validação de email
docs: atualiza guia de instalação
```

### 🔍 Processo de Revisão

1. ✅ Código segue os padrões do projeto
2. ✅ Testes foram incluídos e passam
3. ✅ Documentação atualizada
4. ✅ PR pequeno e focado (< 400 linhas)
5. ✅ Descrição clara do que foi mudado

**Tempo médio de revisão**: 1-3 dias úteis

### 💬 Precisa de Ajuda?

- 📖 Leia a [documentação completa](docs/)
- 💬 Abra uma [Discussion](https://github.com/giusfds/DaRua/discussions)
- 🐛 Veja [issues marcadas como "good first issue"](https://github.com/giusfds/DaRua/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)

**Obrigado por contribuir! Juntos, construímos algo incrível! 🙏**

---

## 📖 Referências

### Documentação Oficial

- [Streamlit Docs](https://docs.streamlit.io/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Python Official](https://docs.python.org/3/)
- [Pandas](https://pandas.pydata.org/docs/)
- [Plotly](https://plotly.com/python/)

### Tutoriais e Recursos

- [Real Python - MySQL](https://realpython.com/python-mysql/)
- [Streamlit Gallery](https://streamlit.io/gallery)
- [W3Schools SQL](https://www.w3schools.com/sql/)

---

<div align="center">

### ⭐ Se este projeto foi útil, considere dar uma estrela!

**Desenvolvido com ❤️ por estudantes de Ciência da Computação**

---

**[Voltar ao topo ⬆️](#-sistema-somos-darua---gestão-de-doações)**

</div>
