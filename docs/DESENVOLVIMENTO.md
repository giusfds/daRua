# 💻 Guia de Desenvolvimento - Somos DaRua

## 📋 Índice

- [Começando](#começando)
- [Estrutura de Código](#estrutura-de-código)
- [Padrões de Código](#padrões-de-código)
- [Boas Práticas](#boas-práticas)
- [Convenções de Nomenclatura](#convenções-de-nomenclatura)
- [Trabalhando com Models](#trabalhando-com-models)
- [Criando Páginas](#criando-páginas)
- [Estilização](#estilização)
- [Debugging](#debugging)
- [Git Workflow](#git-workflow)

---

## 🚀 Começando

### Configurando o Ambiente de Desenvolvimento

```bash
# 1. Clone o repositório
git clone https://github.com/giusfds/DaRua.git
cd DaRua

# 2. Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# Edite .env com suas configurações

# 5. Configure o banco de dados
mysql -u root -p < database/schema/create_database.sql

# 6. Execute o sistema
cd app
streamlit run main.py
```

### Estrutura de Branches

```
main                 # Produção estável
├── develop          # Desenvolvimento (integração)
├── feature/nova-funcionalidade
├── bugfix/correcao-bug
└── hotfix/correcao-urgente
```

---

## 📁 Estrutura de Código

### Organização dos Arquivos

```python
# ✅ BOM: Arquivo focado em uma responsabilidade
# app/pages/2_doadores.py
"""
Página de gestão de doadores.
Responsável por:
- Listar doadores
- Cadastrar doadores
- Editar doadores
- Excluir doadores
"""

# ✅ BOM: Model com responsabilidade clara
# backend/models/doador.py
"""
Model Doador - representa um doador no sistema
"""
class Doador:
    # CRUD operations
    pass
```

### Imports Organizados

```python
# 1. Imports da biblioteca padrão
import os
import sys
from typing import Optional, List, Dict
from datetime import datetime

# 2. Imports de terceiros
import streamlit as st
import pandas as pd
import plotly.express as px

# 3. Imports locais
from utils.config import setup_page, COLORS
from backend.models.doador import Doador
```

---

## 📝 Padrões de Código

### 1. Nomenclatura

#### Variáveis e Funções (snake_case)

```python
# ✅ BOM
total_doacoes = 100
nome_doador = "João Silva"

def calcular_total_doacoes(doador_id):
    pass

def buscar_doadores_por_nome(nome):
    pass
```

#### Classes (PascalCase)

```python
# ✅ BOM
class Doador:
    pass

class DoacaoService:
    pass

class DatabaseConnection:
    pass
```

#### Constantes (UPPER_SNAKE_CASE)

```python
# ✅ BOM
MAX_TENTATIVAS = 3
DB_TIMEOUT = 30
DEFAULT_PAGE_SIZE = 50

COLORS = {
    'primary': '#A78BFA',
    'secondary': '#60A5FA'
}
```

#### Arquivos (snake_case)

```python
# ✅ BOM
doador.py
doacao_service.py
database_connection.py

# ❌ EVITAR
Doador.py
DoacaoService.py
```

---

### 2. Docstrings

#### Módulos

```python
"""
Módulo de Conexão com MySQL

Este módulo fornece a classe DatabaseConnection que gerencia
conexões com o banco de dados MySQL usando context manager.

Exemplo:
    with DatabaseConnection() as db:
        result = db.fetch_all("SELECT * FROM Doador")
"""
```

#### Classes

```python
class Doador:
    """
    Representa um doador no sistema.

    Um doador é uma pessoa física ou jurídica que realiza doações
    para beneficiários através do sistema.

    Attributes:
        idDoador (int): Identificador único do doador
        nome (str): Nome completo ou razão social
        telefone (str): Telefone de contato
        email (str): Email para comunicação

    Example:
        >>> doador = Doador(nome="João Silva", email="joao@email.com")
        >>> doador.save()
        True
    """
```

#### Funções

```python
def buscar_doadores_ativos(limite: int = 10) -> List[Doador]:
    """
    Busca doadores que fizeram doações nos últimos 6 meses.

    Args:
        limite (int): Número máximo de resultados. Default: 10

    Returns:
        List[Doador]: Lista de doadores ativos ordenados por
                      número de doações (decrescente)

    Raises:
        DatabaseError: Se houver erro na conexão com o banco

    Example:
        >>> doadores = buscar_doadores_ativos(limite=5)
        >>> len(doadores)
        5
    """
```

---

### 3. Type Hints

```python
# ✅ BOM: Use type hints sempre que possível
from typing import Optional, List, Dict, Tuple

def buscar_doador(id: int) -> Optional[Doador]:
    """Busca doador por ID"""
    pass

def listar_doacoes(
    doador_id: Optional[int] = None,
    limite: int = 50
) -> List[Dict[str, any]]:
    """Lista doações com filtros opcionais"""
    pass

def validar_email(email: str) -> Tuple[bool, str]:
    """
    Valida formato de email.

    Returns:
        Tuple[bool, str]: (valido, mensagem_erro)
    """
    pass
```

---

### 4. Validações

```python
class Doador:
    def validate(self) -> Tuple[bool, str]:
        """
        Valida dados do doador.

        Returns:
            Tuple[bool, str]: (valido, mensagem_erro)
        """
        # Validação de campo obrigatório
        if not self.nome or not self.nome.strip():
            return False, "Nome é obrigatório"

        # Validação de formato
        if self.email and '@' not in self.email:
            return False, "Email inválido"

        # Validação de tamanho
        if self.estado and len(self.estado) != 2:
            return False, "Estado deve ter 2 caracteres (UF)"

        # Validação customizada
        if self.cep:
            cep_limpo = self.cep.replace('-', '').replace('.', '')
            if not cep_limpo.isdigit() or len(cep_limpo) != 8:
                return False, "CEP inválido"

        return True, ""
```

---

### 5. Tratamento de Erros

```python
# ✅ BOM: Específico e informativo
try:
    doador.save()
    st.success("✅ Doador cadastrado com sucesso!")

except DatabaseError as e:
    st.error(f"❌ Erro ao salvar no banco: {e}")
    logger.error(f"Database error in save_doador: {e}", exc_info=True)

except ValidationError as e:
    st.warning(f"⚠️ Dados inválidos: {e}")

except Exception as e:
    st.error("❌ Erro inesperado. Tente novamente.")
    logger.critical(f"Unexpected error: {e}", exc_info=True)

# ❌ EVITAR: Genérico demais
try:
    doador.save()
except:
    print("Erro")
```

---

### 6. Logs

```python
import logging

# Configurar logger
logger = logging.getLogger(__name__)

# Níveis de log
logger.debug("Variável X = 10")              # Desenvolvimento
logger.info("Doador 123 cadastrado")         # Informação
logger.warning("Email duplicado detectado")  # Aviso
logger.error("Falha ao conectar ao banco")   # Erro
logger.critical("Sistema fora do ar")        # Crítico

# Log com contexto
logger.info(
    "Doador cadastrado",
    extra={
        'doador_id': doador.idDoador,
        'usuario': session_user,
        'ip': request_ip
    }
)
```

---

## 🎨 Trabalhando com Models

### Padrão de Model

```python
"""
Model [Nome da Entidade]
Breve descrição da entidade
"""
from typing import Optional, List, Dict, Tuple
from backend.database.connection import DatabaseConnection


class MinhaEntidade:
    """Representa [entidade] no sistema"""

    def __init__(self, campo1: str, campo2: Optional[str] = None,
                 id: Optional[int] = None):
        """
        Inicializa uma instância.

        Args:
            campo1 (str): Descrição do campo1
            campo2 (Optional[str]): Descrição do campo2
            id (Optional[int]): ID da entidade (após salvar)
        """
        self.id = id
        self.campo1 = campo1
        self.campo2 = campo2

    def __repr__(self) -> str:
        """Representação string do objeto"""
        return f"MinhaEntidade(id={self.id}, campo1={self.campo1})"

    def validate(self) -> Tuple[bool, str]:
        """
        Valida dados da entidade.

        Returns:
            Tuple[bool, str]: (valido, mensagem_erro)
        """
        if not self.campo1:
            return False, "Campo1 é obrigatório"
        return True, ""

    def save(self) -> bool:
        """
        Salva nova entidade no banco.

        Returns:
            bool: True se salvou com sucesso
        """
        valido, erro = self.validate()
        if not valido:
            print(f"✗ Validação falhou: {erro}")
            return False

        query = """
            INSERT INTO MinhaTabela (campo1, campo2)
            VALUES (%s, %s)
        """
        params = (self.campo1, self.campo2)

        with DatabaseConnection() as db:
            if db.execute_query(query, params):
                self.id = db.get_last_insert_id()
                return True
        return False

    def update(self) -> bool:
        """Atualiza entidade existente"""
        if not self.id:
            print("✗ Entidade não possui ID")
            return False

        valido, erro = self.validate()
        if not valido:
            print(f"✗ Validação falhou: {erro}")
            return False

        query = """
            UPDATE MinhaTabela
            SET campo1 = %s, campo2 = %s
            WHERE id = %s
        """
        params = (self.campo1, self.campo2, self.id)

        with DatabaseConnection() as db:
            return db.execute_query(query, params)

    def delete(self) -> bool:
        """Remove entidade"""
        if not self.id:
            print("✗ Entidade não possui ID")
            return False

        query = "DELETE FROM MinhaTabela WHERE id = %s"

        with DatabaseConnection() as db:
            return db.execute_query(query, (self.id,))

    @staticmethod
    def get_all() -> List['MinhaEntidade']:
        """
        Busca todas as entidades.

        Returns:
            List[MinhaEntidade]: Lista de entidades
        """
        query = "SELECT * FROM MinhaTabela ORDER BY campo1"

        with DatabaseConnection() as db:
            results = db.fetch_all(query)
            return [
                MinhaEntidade(
                    id=row['id'],
                    campo1=row['campo1'],
                    campo2=row['campo2']
                )
                for row in results
            ]

    @staticmethod
    def get_by_id(id: int) -> Optional['MinhaEntidade']:
        """
        Busca entidade por ID.

        Args:
            id (int): ID da entidade

        Returns:
            Optional[MinhaEntidade]: Entidade ou None
        """
        query = "SELECT * FROM MinhaTabela WHERE id = %s"

        with DatabaseConnection() as db:
            row = db.fetch_one(query, (id,))
            if row:
                return MinhaEntidade(
                    id=row['id'],
                    campo1=row['campo1'],
                    campo2=row['campo2']
                )
        return None
```

---

## 📱 Criando Páginas Streamlit

### Estrutura Padrão de Página

```python
"""
Página [Nome da Página]
Descrição do que essa página faz
"""
import streamlit as st
from utils.config import (
    setup_page,
    apply_global_css,
    render_sidebar,
    COLORS
)
from backend.models.minha_entidade import MinhaEntidade


# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================
setup_page("Minha Página - Somos DaRua", "🎯")
apply_global_css()

# ============================================================================
# SIDEBAR
# ============================================================================
render_sidebar("Minha Página")

# ============================================================================
# HEADER
# ============================================================================
st.title("🎯 Minha Página")
st.markdown("### Subtítulo da página")
st.markdown("---")

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def carregar_dados():
    """Carrega dados do banco"""
    return MinhaEntidade.get_all()


def exibir_formulario():
    """Exibe formulário de cadastro/edição"""
    with st.form("form_entidade"):
        campo1 = st.text_input("Campo 1*", key="campo1")
        campo2 = st.text_input("Campo 2", key="campo2")

        submitted = st.form_submit_button("💾 Salvar")

        if submitted:
            if not campo1:
                st.error("❌ Campo 1 é obrigatório")
                return

            entidade = MinhaEntidade(campo1=campo1, campo2=campo2)

            if entidade.save():
                st.success("✅ Salvo com sucesso!")
                st.rerun()
            else:
                st.error("❌ Erro ao salvar")


def exibir_tabela(dados):
    """Exibe tabela com os dados"""
    if not dados:
        st.info("ℹ️ Nenhum registro encontrado")
        return

    # Converter para DataFrame
    df = pd.DataFrame([
        {
            'ID': item.id,
            'Campo 1': item.campo1,
            'Campo 2': item.campo2 or '-'
        }
        for item in dados
    ])

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

# ============================================================================
# CONTEÚDO PRINCIPAL
# ============================================================================

# Tabs para organizar conteúdo
tab1, tab2 = st.tabs(["📋 Listagem", "➕ Cadastrar"])

with tab1:
    st.markdown("### Lista de Registros")
    dados = carregar_dados()
    exibir_tabela(dados)

with tab2:
    st.markdown("### Novo Registro")
    exibir_formulario()

# ============================================================================
# FOOTER (OPCIONAL)
# ============================================================================
st.markdown("---")
st.markdown(
    f"<div style='text-align: center; color: {COLORS['text_dark']};'>"
    "Somos DaRua © 2024"
    "</div>",
    unsafe_allow_html=True
)
```

---

## 🎨 Estilização

### Usando o Sistema de Cores

```python
from utils.config import COLORS

# Botões customizados
st.markdown(
    f"""
    <style>
    .custom-button {{
        background-color: {COLORS['primary']};
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Cards customizados
st.markdown(
    f"""
    <div style='
        background-color: {COLORS['white']};
        padding: 20px;
        border-radius: 10px;
        border: 1px solid {COLORS['border']};
    '>
        <h3 style='color: {COLORS['primary']};'>Título</h3>
        <p style='color: {COLORS['text_light']};'>Conteúdo</p>
    </div>
    """,
    unsafe_allow_html=True
)
```

### Componentes Streamlit Comuns

```python
# Inputs
nome = st.text_input("Nome", value="", max_chars=100)
email = st.text_input("Email", type="default")
senha = st.text_input("Senha", type="password")
idade = st.number_input("Idade", min_value=0, max_value=120)
descricao = st.text_area("Descrição", height=100)

# Seletores
opcao = st.selectbox("Selecione", ["Opção 1", "Opção 2"])
multi = st.multiselect("Múltiplas", ["A", "B", "C"])
radio = st.radio("Escolha", ["Sim", "Não"])
checkbox = st.checkbox("Aceito os termos")

# Datas
data = st.date_input("Data")
hora = st.time_input("Hora")

# Arquivo
arquivo = st.file_uploader("Arquivo", type=['csv', 'xlsx'])

# Botões
if st.button("Clique"):
    st.write("Clicou!")

# Mensagens
st.success("✅ Sucesso!")
st.error("❌ Erro!")
st.warning("⚠️ Atenção!")
st.info("ℹ️ Informação")

# Containers
col1, col2 = st.columns(2)
with col1:
    st.write("Coluna 1")
with col2:
    st.write("Coluna 2")

# Expansível
with st.expander("Ver mais"):
    st.write("Conteúdo oculto")

# Tabs
tab1, tab2 = st.tabs(["Tab 1", "Tab 2"])
```

---

## 🐛 Debugging

### Streamlit Debug

```python
# Visualizar variáveis
st.write("Valor:", variavel)
st.json(dict_data)

# Debug condicional
if st.checkbox("Debug Mode"):
    st.write("Debug info:", debug_data)

# Session state
st.write("Session State:", st.session_state)
```

### Python Debug

```python
# Print statements
print(f"DEBUG: variavel = {variavel}")

# Breakpoints (com debugger)
import pdb; pdb.set_trace()

# Logging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug("Valor da variável: %s", variavel)
```

---

## 📊 Boas Práticas

### ✅ DOs

1. **Use type hints**
2. **Escreva docstrings**
3. **Valide dados em múltiplas camadas**
4. **Use context managers para banco de dados**
5. **Trate exceções específicas**
6. **Comente código complexo**
7. **Mantenha funções pequenas (max 50 linhas)**
8. **Use constantes para valores repetidos**
9. **Teste seu código**
10. **Faça commits frequentes e descritivos**

### ❌ DON'Ts

1. **Não hardcode credenciais**
2. **Não use `except: pass` sem logging**
3. **Não repita código (DRY)**
4. **Não deixe prints de debug**
5. **Não faça commits direto na main**
6. **Não ignore warnings**
7. **Não use variáveis globais desnecessariamente**
8. **Não deixe TODOs sem contexto**
9. **Não faça queries SQL vulneráveis a injection**
10. **Não deixe código comentado no commit**

---

## 🔀 Git Workflow

### Commits

```bash
# ✅ BOM: Específico e descritivo
git commit -m "feat: adiciona validação de CPF no cadastro de doador"
git commit -m "fix: corrige erro ao salvar doação sem campanha"
git commit -m "docs: atualiza README com instruções de instalação"

# ❌ EVITAR: Vago
git commit -m "mudanças"
git commit -m "fix"
git commit -m "atualização"
```

### Branches

```bash
# Criar nova feature
git checkout -b feature/nome-da-feature

# Trabalhar na feature
git add .
git commit -m "feat: implementa funcionalidade X"

# Atualizar com main
git fetch origin
git rebase origin/main

# Push
git push origin feature/nome-da-feature

# Criar Pull Request no GitHub
```

---

[⬅️ Voltar ao Índice](./INDEX.md) | [➡️ Próximo: API/Models](./API.md)
