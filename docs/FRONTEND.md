# 🎨 Frontend - Somos DaRua

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Tecnologias](#tecnologias)
- [Estrutura do Frontend](#estrutura-do-frontend)
- [Páginas do Sistema](#páginas-do-sistema)
- [Componentes Reutilizáveis](#componentes-reutilizáveis)
- [Sistema de Configuração](#sistema-de-configuração)
- [Estilização](#estilização)
- [State Management](#state-management)
- [Formulários](#formulários)
- [Gráficos e Visualizações](#gráficos-e-visualizações)
- [Navegação](#navegação)
- [Boas Práticas](#boas-práticas)

---

## 🎯 Visão Geral

O frontend do sistema Somos DaRua é construído com **Streamlit**, um framework Python que permite criar aplicações web interativas de forma rápida e eficiente.

### Características Principais

✅ **Interface Responsiva**: Adapta-se a diferentes tamanhos de tela
✅ **Tema Escuro**: Design moderno com paleta de cores azul/roxo
✅ **Componentes Reutilizáveis**: Código DRY e manutenível
✅ **Navegação Intuitiva**: Sidebar com menu principal
✅ **Feedback Visual**: Mensagens claras de sucesso/erro
✅ **Gráficos Interativos**: Visualizações com Plotly

---

## 💻 Tecnologias

### Core

- **Streamlit 1.31.0**: Framework web principal
- **Python 3.10+**: Linguagem de programação

### Bibliotecas de Visualização

- **Plotly 5.18.0**: Gráficos interativos
- **Pandas 2.2.0**: Manipulação de dados
- **NumPy 1.26.3**: Computação numérica

### Integração

- **MySQL Connector**: Conexão com banco de dados
- **Python Dotenv**: Gerenciamento de variáveis de ambiente

---

## 📁 Estrutura do Frontend

```
app/
├── main.py                      # 🏠 Dashboard principal
│
├── pages/                       # 📄 Páginas navegáveis
│   ├── 2_doadores.py           # 👤 CRUD Doadores
│   ├── 3_beneficiarios.py      # 🤝 CRUD Beneficiários
│   ├── 4_doacoes.py            # 📦 Sistema de Doações
│   ├── 5_campanhas.py          # 📢 CRUD Campanhas
│   ├── 6_pontos_coleta.py      # 📍 CRUD Pontos de Coleta
│   ├── 7_voluntarios.py        # 🙋 CRUD Voluntários
│   └── 8_relatorios.py         # 📊 Relatórios e Análises
│
├── components/                  # 🧩 Componentes reutilizáveis
│   └── forms.py                # Formulários padronizados
│
└── utils/                       # 🛠️ Utilitários
    ├── config.py               # ⚙️ Configurações centralizadas
    │   ├── COLORS              # Paleta de cores
    │   ├── GLOBAL_CSS          # Estilos CSS
    │   ├── setup_page()        # Config de página
    │   ├── apply_global_css()  # Aplicar estilos
    │   ├── render_sidebar()    # Renderizar menu
    │   └── render_footer()     # Renderizar rodapé
    │
    └── mock_data.py            # Dados fictícios (deprecated)
```

---

## 📄 Páginas do Sistema

### 🏠 Dashboard (main.py)

**Arquivo**: `app/main.py`

**Propósito**: Página inicial com visão geral do sistema

**Componentes**:

- 4 Cards de métricas principais
- Gráfico de pizza (doações por categoria)
- Gráfico de barras (doações mensais)
- Gráfico de linha (tendência de doadores)
- Tabela com últimas 10 doações
- Cards de destaques e alertas

**Dados**: Busca dados reais do MySQL via `backend/models/dashboard_model.py`

**Exemplo de Uso**:

```python
# Carregar métricas do banco
from models.dashboard_model import get_metricas_dashboard

metricas = get_metricas_dashboard()

# Exibir métricas
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total de Doadores", metricas['total_doadores'])
```

---

### 👤 Doadores (2_doadores.py)

**Arquivo**: `app/pages/2_doadores.py`

**Propósito**: CRUD completo de doadores

**Funcionalidades**:

- ➕ Cadastrar novo doador com dados completos
- 📋 Listar todos os doadores
- 🔍 Buscar por nome/email/telefone
- ✏️ Editar informações de doadores
- 🗑️ Excluir doadores (bloqueado se houver doações)
- 📊 Estatísticas: Total, Ativos, Cadastros do mês

**Estrutura**:

```
Tabs:
├── Cadastrar Novo
│   └── Formulário completo
├── Listar Doadores
│   ├── Filtros de busca
│   └── Tabela com ações
└── Estatísticas
    └── Cards com métricas
```

**Validações Frontend**:

- Nome obrigatório
- Email com formato válido
- Estado com 2 caracteres
- CEP com 8 dígitos

---

### 🤝 Beneficiários (3_beneficiarios.py)

**Arquivo**: `app/pages/3_beneficiarios.py`

**Propósito**: Gerenciar pessoas que recebem doações

**Funcionalidades**:

- ➕ Cadastrar beneficiário com dados pessoais
- 🔍 Filtrar por status (Ativo/Inativo/Aguardando)
- 🔍 Buscar por nome
- ✏️ Editar informações
- 🗑️ Excluir (se não tiver doações recebidas)
- 📊 Gráficos:
  - Distribuição por status
  - Faixa etária
  - Distribuição por gênero

**Campos Especiais**:

- Data de Nascimento → Idade (calculada automaticamente)
- Gênero (M/F/O/Prefiro não informar)
- Necessidades (múltipla escolha)
- Status (Ativo/Inativo/Aguardando)

---

### 📦 Doações (4_doacoes.py)

**Arquivo**: `app/pages/4_doacoes.py`

**Propósito**: Sistema completo de gestão de doações (duas fases)

**Fluxo de Doações**:

```
FASE 1: RECEBIMENTO
├── Doador entrega itens
├── Voluntário registra no ponto de coleta
└── Status: "Recebida"

FASE 2: DISTRIBUIÇÃO
├── Seleciona doação recebida
├── Marca beneficiários que receberão
├── Seleciona voluntários distribuidores
└── Status: "Distribuída"
```

**Abas da Página**:

#### Aba 1: Nova Doação

Formulário organizado em 3 seções:

1. **Identificação** (obrigatório)

   - Doador
   - Ponto de Coleta
   - Voluntário Responsável

2. **Detalhes da Doação**

   - Tipo: Alimentos/Roupas/Medicamentos/Dinheiro/Outros
   - Descrição do Item
   - Quantidade + Unidade (Kg/Litros/Unidades/R$)

3. **Informações Adicionais** (opcional)
   - Campanha vinculada
   - Data prevista de entrega
   - Observações

#### Aba 2: Distribuir Doação

1. Dropdown: Seleciona doação "Recebida"
2. Exibe: Detalhes completos da doação
3. Checkboxes: Seleciona beneficiários
4. Multiselect: Voluntários distribuidores (opcional)
5. Date input: Data de entrega
6. Botão: Confirmar distribuição

**Ao confirmar**:

- ✅ Cria registros na tabela `Recebe`
- ✅ Cria registros na tabela `Possui`
- ✅ Atualiza status para "Distribuída"
- ✅ Atualiza data de entrega

#### Aba 3: Histórico

- Filtros: Tipo, Status
- Estatísticas: Total, Recebidas, Distribuídas
- Tabela com todas as doações

---

### 📢 Campanhas (5_campanhas.py)

**Arquivo**: `app/pages/5_campanhas.py`

**Propósito**: Gerenciar campanhas de arrecadação

**Funcionalidades**:

- ➕ Criar nova campanha com metas
- 🔍 Filtrar por status (Ativa/Concluída)
- 🔍 Ordenar: Mais recentes, Nome, Progresso
- ✏️ Editar campanha
- 🗑️ Excluir (se não houver doações)
- 📊 Cards visuais:
  - Nome e descrição
  - Período (início e término)
  - Meta e arrecadado
  - Barra de progresso
  - Valor/quantidade faltante

**Cálculo Automático**:

```python
progresso = (arrecadado / meta) × 100%
faltante = meta - arrecadado
```

**Validações**:

- Nome obrigatório
- Meta maior que zero
- Data término > Data início

---

### 📍 Pontos de Coleta (6_pontos_coleta.py)

**Arquivo**: `app/pages/6_pontos_coleta.py`

**Propósito**: Gerenciar locais de recebimento de doações

**Funcionalidades**:

- ➕ Cadastrar novo ponto com endereço completo
- 🔍 Filtrar por status (Ativo/Inativo)
- 🔍 Buscar por nome/endereço
- ✏️ Editar informações
- 🗑️ Excluir (se não houver objetos cadastrados)
- 📊 Cards visuais com:
  - Status emoji (🟢 Ativo / 🔴 Inativo)
  - Nome do responsável
  - Endereço completo
  - Botões de ação

**Informações Exibidas**:

- Responsável (obrigatório)
- Endereço: Rua, Número, Complemento, Bairro, Cidade, Estado, CEP
- Status operacional

---

### 🙋 Voluntários (7_voluntarios.py)

**Arquivo**: `app/pages/7_voluntarios.py`

**Propósito**: Gerenciar colaboradores do sistema

**Funcionalidades**:

- ➕ Cadastrar novo voluntário
- 🔍 Filtrar por status e área de atuação
- 🔍 Buscar por nome/email/telefone
- ✏️ Editar informações
- 🗑️ Excluir (se não estiver associado a doações)

**Uso no Sistema**:

1. **Voluntário de Coleta**: Registra nova doação no ponto de coleta
2. **Voluntário Distribuidor**: Entrega doação aos beneficiários

**Campos**:

- Nome (obrigatório)
- Email (obrigatório)
- Telefone (obrigatório)

---

### 📊 Relatórios (8_relatorios.py)

**Arquivo**: `app/pages/8_relatorios.py`

**Propósito**: Análises detalhadas e exportação de dados

**Estrutura**:

```
┌─────────────────────────────┐
│ Filtros                     │
├─────────────────────────────┤
│ • Data Início               │
│ • Data Fim                  │
│ • Tipo de Relatório         │
└─────────────────────────────┘

┌─────────────────────────────┐
│ Métricas Principais         │
├─────────────────────────────┤
│ • Total de Doações          │
│ • Total de Doadores         │
│ • Total de Beneficiários    │
│ • Campanhas Ativas          │
└─────────────────────────────┘

┌─────────────────────────────┐
│ Análises Detalhadas         │
├─────────────────────────────┤
│ • Gráficos comparativos     │
│ • Tendências temporais      │
│ • Rankings                  │
└─────────────────────────────┘

┌─────────────────────────────┐
│ Tabelas Detalhadas          │
├─────────────────────────────┤
│ Tab 1: Doações              │
│ Tab 2: Doadores             │
│ Tab 3: Beneficiários        │
└─────────────────────────────┘

┌─────────────────────────────┐
│ Exportação (Planejado)      │
├─────────────────────────────┤
│ • PDF                       │
│ • Excel                     │
│ • Email                     │
└─────────────────────────────┘
```

**Tipos de Relatório**:

1. **Visão Geral**: Métricas principais do período
2. **Doações**: Detalhes de todas as doações
3. **Doadores**: Ranking e estatísticas
4. **Beneficiários**: Distribuição e análises
5. **Campanhas**: Performance de campanhas

---

## 🧩 Componentes Reutilizáveis

### Configuração Central (`utils/config.py`)

Este arquivo centraliza todas as configurações do frontend.

#### Paleta de Cores

```python
COLORS = {
    'primary': '#A78BFA',        # Roxo claro - botões e títulos
    'primary_dark': '#8B5CF6',   # Roxo médio - hover
    'secondary': '#60A5FA',      # Azul claro - subtítulos
    'success': '#34D399',        # Verde - sucesso
    'warning': '#FBBF24',        # Amarelo - avisos
    'background': '#0F172A',     # Azul escuro - fundo
    'white': '#1E293B',          # Cinza azulado - cards
    'text_dark': '#E2E8F0',      # Cinza claro - texto secundário
    'text_light': '#F8FAFC',     # Quase branco - texto principal
    'border': '#334155',         # Cinza médio - bordas
}
```

#### Funções Disponíveis

```python
# Configurar página
setup_page(page_title: str, page_icon: str)

# Aplicar estilos globais
apply_global_css()

# Renderizar sidebar
render_sidebar(current_page: str = "")

# Renderizar footer
render_footer()

# Criar card de métrica
create_metric_card(label: str, value: str, delta: str = None)

# Mensagens padronizadas
show_info_message(message: str, icon: str = "ℹ️")
show_success_message(message: str, icon: str = "✅")
show_warning_message(message: str, icon: str = "⚠️")
show_error_message(message: str, icon: str = "❌")
```

#### Exemplo de Uso

```python
from utils.config import (
    setup_page,
    apply_global_css,
    render_sidebar,
    show_success_message,
    COLORS
)

# Configurar página
setup_page("Minha Página", "🎯")
apply_global_css()

# Renderizar sidebar
render_sidebar("Minha Página")

# Usar cores
st.markdown(
    f"<h1 style='color: {COLORS['primary']};'>Título</h1>",
    unsafe_allow_html=True
)

# Mensagens
show_success_message("Operação realizada com sucesso!")
```

---

## 🎨 Estilização

### CSS Global

O sistema utiliza CSS customizado para criar uma interface consistente:

```css
/* Fundo da página */
.main {
  background-color: #0f172a; /* Azul escuro */
  color: #f8fafc; /* Texto claro */
}

/* Botões */
.stButton > button {
  background-color: #a78bfa; /* Roxo */
  color: #0f172a;
  border-radius: 8px;
  padding: 0.5rem 2rem;
  transition: all 0.3s ease;
}

.stButton > button:hover {
  background-color: #8b5cf6;
  box-shadow: 0 4px 6px rgba(167, 139, 250, 0.3);
}

/* Cards */
.metric-card {
  background-color: #1e293b; /* Cinza azulado */
  padding: 1.5rem;
  border-radius: 10px;
  border: 1px solid #334155;
}

/* Inputs */
.stTextInput > div > div > input {
  background-color: #1e293b;
  color: #f8fafc;
  border-radius: 8px;
  border: 1px solid #334155;
}
```

### Componentes Visuais

#### Cards Estilizados

```python
st.markdown(
    f"""
    <div style='
        background-color: {COLORS['white']};
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid {COLORS['border']};
        margin-bottom: 1rem;
    '>
        <h3 style='color: {COLORS['primary']};'>Título do Card</h3>
        <p style='color: {COLORS['text_dark']};'>Conteúdo do card</p>
    </div>
    """,
    unsafe_allow_html=True
)
```

#### Botões Personalizados

```python
# Botão padrão Streamlit (já estilizado globalmente)
if st.button("Salvar"):
    # ação

# Botão customizado
st.markdown(
    f"""
    <button style='
        background-color: {COLORS['success']};
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    '>
        Confirmar
    </button>
    """,
    unsafe_allow_html=True
)
```

---

## 💾 State Management

### Session State

Streamlit mantém estado entre reruns usando `st.session_state`:

```python
# Inicializar estado
if 'contador' not in st.session_state:
    st.session_state.contador = 0

# Ler estado
valor = st.session_state.contador

# Modificar estado
st.session_state.contador += 1

# Usar com widgets
nome = st.text_input("Nome", key="nome_input")
# Equivalente a: st.session_state.nome_input
```

### Exemplo Prático: Edição de Doador

```python
# Inicializar estado de edição
if 'editando_doador' not in st.session_state:
    st.session_state.editando_doador = None

# Botão para iniciar edição
if st.button("Editar", key=f"edit_{doador.idDoador}"):
    st.session_state.editando_doador = doador.idDoador
    st.rerun()

# Exibir formulário se estiver editando
if st.session_state.editando_doador == doador.idDoador:
    with st.form("form_editar"):
        novo_nome = st.text_input("Nome", value=doador.nome)
        novo_email = st.text_input("Email", value=doador.email)

        if st.form_submit_button("Salvar"):
            doador.nome = novo_nome
            doador.email = novo_email
            doador.update()
            st.session_state.editando_doador = None
            st.rerun()
```

---

## 📝 Formulários

### Estrutura Básica

```python
with st.form("nome_do_form", clear_on_submit=True):
    # Campos do formulário
    campo1 = st.text_input("Campo 1*")
    campo2 = st.selectbox("Campo 2", opcoes)
    campo3 = st.date_input("Campo 3")

    # Botão de submit (sempre dentro do form)
    submitted = st.form_submit_button("Enviar")

    if submitted:
        # Validações
        if not campo1:
            st.error("Campo 1 é obrigatório")
            return

        # Processar dados
        salvar_dados(campo1, campo2, campo3)
        st.success("Dados salvos!")
```

### Formulário Completo de Doador

```python
def render_form_doador(doador=None):
    """Renderiza formulário de cadastro/edição de doador"""

    # Valores iniciais (para edição)
    valores = {
        'nome': doador.nome if doador else "",
        'email': doador.email if doador else "",
        'telefone': doador.telefone if doador else "",
        'logradouro': doador.logradouro if doador else "",
        'numero': doador.numero if doador else "",
        'complemento': doador.complemento if doador else "",
        'bairro': doador.bairro if doador else "",
        'cidade': doador.cidade if doador else "",
        'estado': doador.estado if doador else "",
        'cep': doador.cep if doador else "",
    }

    with st.form("form_doador", clear_on_submit=not doador):
        st.subheader("Dados Pessoais")

        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome*", value=valores['nome'])
        with col2:
            email = st.text_input("Email", value=valores['email'])

        col1, col2 = st.columns(2)
        with col1:
            telefone = st.text_input("Telefone", value=valores['telefone'])
        with col2:
            pass

        st.subheader("Endereço")

        col1, col2, col3 = st.columns([3, 1, 2])
        with col1:
            logradouro = st.text_input("Logradouro", value=valores['logradouro'])
        with col2:
            numero = st.text_input("Número", value=valores['numero'])
        with col3:
            complemento = st.text_input("Complemento", value=valores['complemento'])

        col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
        with col1:
            bairro = st.text_input("Bairro", value=valores['bairro'])
        with col2:
            cidade = st.text_input("Cidade", value=valores['cidade'])
        with col3:
            estado = st.text_input("UF", value=valores['estado'], max_chars=2)
        with col4:
            cep = st.text_input("CEP", value=valores['cep'])

        submitted = st.form_submit_button(
            "✏️ Atualizar" if doador else "➕ Cadastrar"
        )

        if submitted:
            # Validar
            if not nome:
                st.error("Nome é obrigatório")
                return

            if email and '@' not in email:
                st.error("Email inválido")
                return

            # Salvar/Atualizar
            if doador:
                doador.nome = nome
                doador.email = email
                # ... outros campos
                if doador.update():
                    st.success("Doador atualizado!")
                    st.rerun()
            else:
                novo_doador = Doador(
                    nome=nome,
                    email=email,
                    # ... outros campos
                )
                if novo_doador.save():
                    st.success("Doador cadastrado!")
                    st.rerun()
```

---

## 📊 Gráficos e Visualizações

### Gráficos com Plotly

#### Gráfico de Pizza

```python
import plotly.express as px

# Dados
dados = {
    'Alimentos': 45,
    'Roupas': 30,
    'Medicamentos': 15,
    'Outros': 10
}

df = pd.DataFrame(
    list(dados.items()),
    columns=['Categoria', 'Quantidade']
)

# Criar gráfico
fig = px.pie(
    df,
    values='Quantidade',
    names='Categoria',
    color_discrete_sequence=[
        COLORS['primary'],
        COLORS['secondary'],
        COLORS['success'],
        COLORS['warning']
    ],
    title="Doações por Categoria"
)

# Configurações adicionais
fig.update_traces(
    textposition='inside',
    textinfo='percent+label'
)

fig.update_layout(
    height=400,
    showlegend=True
)

# Exibir
st.plotly_chart(fig, use_container_width=True)
```

#### Gráfico de Barras

```python
# Dados mensais
dados_mensais = {
    '2024-01': 120,
    '2024-02': 150,
    '2024-03': 180,
    '2024-04': 145,
    '2024-05': 200,
    '2024-06': 175
}

df = pd.DataFrame(
    list(dados_mensais.items()),
    columns=['Mês', 'Quantidade']
)

# Formatar mês
df['Mês'] = pd.to_datetime(df['Mês']).dt.strftime('%b/%y')

# Criar gráfico
fig = px.bar(
    df,
    x='Mês',
    y='Quantidade',
    color_discrete_sequence=[COLORS['primary']],
    title="Doações nos Últimos 6 Meses"
)

fig.update_layout(
    xaxis_title="",
    yaxis_title="Número de Doações",
    height=400
)

st.plotly_chart(fig, use_container_width=True)
```

#### Gráfico de Linha

```python
# Tendência temporal
fig = px.line(
    df,
    x='Mês',
    y='Quantidade',
    markers=True,
    color_discrete_sequence=[COLORS['secondary']],
    title="Tendência de Doações"
)

fig.update_layout(height=350)
st.plotly_chart(fig, use_container_width=True)
```

### Métricas do Streamlit

```python
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total de Doadores",
        value="1,234",
        delta="+23 este mês"
    )

with col2:
    st.metric(
        label="Total de Doações",
        value="5,678",
        delta="+156 este mês"
    )

with col3:
    st.metric(
        label="Campanhas Ativas",
        value="8",
        delta="+3"
    )

with col4:
    st.metric(
        label="Beneficiários",
        value="890",
        delta="+12 este mês"
    )
```

---

## 🧭 Navegação

### Sidebar com Menu

O sistema usa a sidebar do Streamlit para navegação principal:

```python
def render_sidebar(current_page: str = ""):
    """Renderiza sidebar com links de navegação"""

    with st.sidebar:
        # Título
        st.title("🤝 Somos DaRua")
        st.markdown("---")

        # Links de navegação
        st.page_link("main.py", label="🏠 Dashboard", icon="🏠")
        st.page_link("pages/2_doadores.py", label="👤 Doadores", icon="👤")
        st.page_link("pages/3_beneficiarios.py", label="🤝 Beneficiários", icon="🤝")
        st.page_link("pages/4_doacoes.py", label="📦 Doações", icon="📦")
        st.page_link("pages/5_campanhas.py", label="📢 Campanhas", icon="📢")
        st.page_link("pages/6_pontos_coleta.py", label="📍 Pontos de Coleta", icon="📍")
        st.page_link("pages/7_voluntarios.py", label="🙋 Voluntários", icon="🙋")
        st.page_link("pages/8_relatorios.py", label="📊 Relatórios", icon="📊")

        # Informações
        st.markdown("---")
        st.caption("Versão 1.0.0")
        st.caption("Sistema de Gestão de Doações")
```

### Tabs para Organização

```python
# Criar tabs
tab1, tab2, tab3 = st.tabs(["📋 Listagem", "➕ Cadastrar", "📊 Estatísticas"])

with tab1:
    st.markdown("### Lista de Registros")
    # Conteúdo da tab 1

with tab2:
    st.markdown("### Novo Registro")
    # Conteúdo da tab 2

with tab3:
    st.markdown("### Estatísticas")
    # Conteúdo da tab 3
```

### Navegação Condicional

```python
# Mostrar conteúdo baseado em estado
if st.session_state.get('modo') == 'editar':
    render_form_edicao()
elif st.session_state.get('modo') == 'visualizar':
    render_detalhes()
else:
    render_listagem()
```

---

## ✅ Boas Práticas

### 1. Organização de Código

```python
# ✅ BOM: Separar em funções
def carregar_dados():
    """Carrega dados do banco"""
    return Doador.get_all()

def exibir_tabela(dados):
    """Exibe tabela formatada"""
    df = pd.DataFrame(dados)
    st.dataframe(df)

def main():
    """Função principal da página"""
    dados = carregar_dados()
    exibir_tabela(dados)

if __name__ == "__main__":
    main()
```

### 2. Validações em Múltiplas Camadas

```python
# Frontend (Streamlit) - UX
if not nome:
    st.error("❌ Nome é obrigatório")
    return

if email and '@' not in email:
    st.error("❌ Email inválido")
    return

# Backend (Model) - Segurança
valido, erro = doador.validate()
if not valido:
    st.error(f"❌ {erro}")
    return
```

### 3. Feedback Visual Consistente

```python
# Mensagens padronizadas
from utils.config import (
    show_success_message,
    show_error_message,
    show_warning_message,
    show_info_message
)

# Sucesso
if doador.save():
    show_success_message("Doador cadastrado com sucesso!")
else:
    show_error_message("Erro ao cadastrar doador")

# Aviso
if doador.tem_doacoes():
    show_warning_message("Este doador possui doações vinculadas")

# Informação
show_info_message("Preencha todos os campos obrigatórios")
```

### 4. Tratamento de Erros

```python
try:
    doador.save()
    st.success("✅ Salvo com sucesso!")
    st.rerun()
except Exception as e:
    if "foreign key" in str(e).lower():
        st.error("❌ Não é possível excluir: existem registros relacionados")
    elif "duplicate" in str(e).lower():
        st.error("❌ Email já cadastrado")
    else:
        st.error(f"❌ Erro inesperado: {str(e)}")
```

### 5. Performance

```python
# ✅ BOM: Cachear dados pesados
@st.cache_data(ttl=300)  # 5 minutos
def carregar_dados_pesados():
    return processar_dados_complexos()

# ✅ BOM: Limitar queries
dados = Doador.get_all(limit=100)

# ❌ EVITAR: Recarregar tudo a cada interação
# dados = Doador.get_all()  # Sem cache
```

### 6. Responsividade

```python
# Adaptar layout para diferentes telas
col1, col2 = st.columns([2, 1])  # Proporções
col1, col2, col3 = st.columns(3)  # Igual largura

# Containers expansíveis
with st.container():
    st.write("Conteúdo que pode expandir")

# Expander para detalhes
with st.expander("Ver detalhes"):
    st.write("Informações adicionais")
```

### 7. Acessibilidade

```python
# Labels descritivos
nome = st.text_input(
    "Nome completo do doador*",
    help="Digite o nome completo ou razão social"
)

# Placeholders úteis
email = st.text_input(
    "Email",
    placeholder="exemplo@email.com"
)

# Mensagens claras
if not nome:
    st.error("❌ O campo Nome é obrigatório para continuar")
```

---

## 🐛 Debugging

### Exibir Dados de Debug

```python
# Modo debug condicional
if st.checkbox("🐛 Debug Mode"):
    st.json({
        'session_state': dict(st.session_state),
        'dados': dados,
        'metricas': metricas
    })

# Expander para debug
with st.expander("🐛 Debug Info"):
    st.write("Session State:", st.session_state)
    st.write("Dados:", dados)
```

### Logs

```python
import logging

logger = logging.getLogger(__name__)

# Em desenvolvimento
logger.debug(f"Dados carregados: {len(dados)} registros")

# Em produção
logger.info(f"Usuário {user_id} acessou página X")
logger.error(f"Erro ao salvar: {str(e)}")
```

---

## 📚 Recursos Adicionais

### Documentação Oficial

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Python](https://plotly.com/python/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

### Exemplos

- [Streamlit Gallery](https://streamlit.io/gallery)
- [Plotly Examples](https://plotly.com/python/)

---

[⬅️ Voltar ao Índice](./INDEX.md) | [➡️ Próximo: Testes](./TESTES.md)
