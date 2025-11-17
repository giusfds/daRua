"""
Arquivo de Configuração Central do Sistema Somos DaRua
Este arquivo centraliza:
- Estilos CSS globais
- Configurações de página
- Função de navegação na sidebar
- Esquema de cores do sistema
"""

import streamlit as st

# ============================================================================
# ESQUEMA DE CORES DO SISTEMA
# ============================================================================
"""
Definimos as cores principais que serão usadas em todo o sistema.
Isso garante consistência visual em todas as páginas.
"""

COLORS = {
    'primary': '#A78BFA',        # Roxo claro - usado em botões e títulos (melhor contraste no escuro)
    'primary_dark': '#8B5CF6',   # Roxo médio - usado no hover dos botões
    'secondary': '#60A5FA',      # Azul claro - usado em subtítulos e destaques
    'success': '#34D399',        # Verde claro - usado para mensagens de sucesso
    'warning': '#FBBF24',        # Amarelo - usado para avisos (melhor visibilidade)
    'background': '#0F172A',     # Azul escuro profundo - cor de fundo das páginas
    'white': '#1E293B',          # Cinza azulado escuro - cor de fundo dos cards
    'text_dark': '#E2E8F0',      # Cinza muito claro - cor de texto secundário
    'text_light': '#F8FAFC',     # Quase branco - cor de texto principal
    'border': '#334155',         # Cinza médio - para bordas e separadores
}

# ============================================================================
# CSS GLOBAL DO SISTEMA
# ============================================================================
"""
Este CSS será aplicado em todas as páginas do sistema.
Ele define:
- Cor de fundo das páginas
- Estilo dos botões (cor, bordas, hover)
- Estilo dos títulos e subtítulos
- Estilo dos cards e containers
"""

GLOBAL_CSS = f"""
    <style>
    /* Estilo geral da página */
    .main {{
        background-color: {COLORS['background']};
        color: {COLORS['text_light']};
    }}
    
    /* Estilo dos botões */
    .stButton>button {{
        background-color: {COLORS['primary']};
        color: {COLORS['background']};  /* Texto escuro no botão claro */
        border-radius: 8px;
        padding: 0.5rem 2rem;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    
    .stButton>button:hover {{
        background-color: {COLORS['primary_dark']};
        border: none;
        box-shadow: 0 4px 6px rgba(167, 139, 250, 0.3);
    }}
    
    /* Estilo dos títulos */
    h1 {{
        color: {COLORS['primary']};
        font-weight: 700;
    }}
    
    h2, h3 {{
        color: {COLORS['secondary']};
        font-weight: 600;
    }}
    
    /* Estilo dos cards/containers */
    .metric-card {{
        background-color: {COLORS['white']};
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.3);
        border: 1px solid {COLORS['border']};
        transition: all 0.3s ease;
    }}
    
    .metric-card:hover {{
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }}
    
    /* Estilo da sidebar */
    [data-testid="stSidebar"] {{
        background-color: {COLORS['white']};
        border-right: 1px solid {COLORS['border']};
    }}
    
    /* Estilo dos inputs */
    .stTextInput>div>div>input,
    .stSelectbox>div>div>select,
    .stTextArea>div>div>textarea {{
        background-color: {COLORS['white']};
        color: {COLORS['text_light']};
        border-radius: 8px;
        border: 1px solid {COLORS['border']};
    }}
    
    .stTextInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus,
    .stTextArea>div>div>textarea:focus {{
        border-color: {COLORS['primary']};
        box-shadow: 0 0 0 1px {COLORS['primary']};
    }}
    
    /* Estilo das métricas do Streamlit */
    [data-testid="stMetricValue"] {{
        color: {COLORS['text_light']};
    }}
    
    [data-testid="stMetricLabel"] {{
        color: {COLORS['text_dark']};
    }}
    
    /* Estilo das tabelas */
    .stDataFrame {{
        background-color: {COLORS['white']};
        border: 1px solid {COLORS['border']};
    }}
    
    /* Texto geral */
    p, span, label {{
        color: {COLORS['text_dark']};
    }}
    
    /* Links */
    a {{
        color: {COLORS['secondary']};
    }}
    
    a:hover {{
        color: {COLORS['primary']};
    }}
    </style>
"""

# ============================================================================
# FUNÇÃO DE CONFIGURAÇÃO DE PÁGINA
# ============================================================================
"""
Esta função configura as propriedades básicas de cada página.
Parâmetros:
- page_title: título que aparece na aba do navegador
- page_icon: emoji que aparece ao lado do título
"""

def setup_page(page_title: str, page_icon: str):
    """
    Configura as propriedades da página do Streamlit.
    
    Args:
        page_title (str): Título da página que aparece na aba do navegador
        page_icon (str): Emoji/ícone da página
    
    Esta função define:
    - Título e ícone da página
    - Layout wide (usa toda a largura da tela)
    - Sidebar expandida por padrão
    """
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout="wide",
        initial_sidebar_state="expanded"
    )

# ============================================================================
# FUNÇÃO DE APLICAÇÃO DO CSS GLOBAL
# ============================================================================
"""
Esta função aplica o CSS global definido acima na página atual.
Deve ser chamada em todas as páginas após setup_page().
"""

def apply_global_css():
    """
    Aplica o CSS global do sistema na página atual.
    
    Esta função injeta o CSS definido em GLOBAL_CSS usando
    st.markdown com unsafe_allow_html=True, o que permite
    usar HTML e CSS personalizados no Streamlit.
    """
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ============================================================================
# FUNÇÃO DE RENDERIZAÇÃO DA SIDEBAR
# ============================================================================
"""
Esta função cria a sidebar (barra lateral) com:
- Logo/título do sistema
- Links de navegação para todas as páginas
- Informações de versão
"""

def render_sidebar(current_page: str = ""):
    """
    Renderiza a sidebar com navegação do sistema.
    
    Args:
        current_page (str): Nome da página atual (opcional)
                           Usado para destacar a página ativa
    
    Esta função cria:
    - Título do sistema com emoji
    - Links de navegação para todas as páginas
    - Separador visual
    - Informações de versão e sistema
    
    IMPORTANTE: Os caminhos dos page_link são relativos à estrutura:
    - main.py (raiz do projeto)
    - pages/ (pasta com as outras páginas)
    """
    with st.sidebar:
        # Título do sistema
        st.title("🤝 Somos DaRua")
        st.markdown("---")
        
        # Links de navegação
        # NOTA: Quando estamos em uma página dentro de pages/, 
        # usamos "main.py" para voltar à raiz
        # Quando estamos na raiz (main.py), usamos "pages/X.py"
        
        st.page_link("main.py", label="🏠 Dashboard", icon="🏠")
        st.page_link("pages/2_doadores.py", label="👤 Doadores", icon="👤")
        st.page_link("pages/3_beneficiarios.py", label="🤝 Beneficiários", icon="🤝")
        st.page_link("pages/4_doacoes.py", label="📦 Doações", icon="📦")
        st.page_link("pages/5_campanhas.py", label="📢 Campanhas", icon="📢")
        st.page_link("pages/6_pontos_coleta.py", label="📍 Pontos de Coleta", icon="📍")
        st.page_link("pages/7_voluntarios.py", label="🙋 Voluntários", icon="🙋")
        st.page_link("pages/8_relatorios.py", label="📊 Relatórios", icon="📊")
        
        # Separador e informações do sistema
        st.markdown("---")
        st.caption("Versão 1.0.0 - Frontend")
        st.caption("Sistema de Gestão de Doações")

# ============================================================================
# FUNÇÃO DE RODAPÉ PADRÃO
# ============================================================================
"""
Esta função cria um rodapé padrão para todas as páginas.
Mantém a identidade visual e informações do sistema.
"""

def render_footer():
    """
    Renderiza o rodapé padrão do sistema.
    
    Exibe:
    - Nome do sistema
    - Mensagem motivacional
    - Formatação centralizada
    """
    st.markdown(f"""
        <div style='text-align: center; padding: 2rem 0; color: {COLORS['text_dark']};'>
            <p><strong>Somos DaRua</strong> - Sistema de Gestão de Doações</p>
            <p>Transformando vidas através da solidariedade ❤️</p>
        </div>
    """, unsafe_allow_html=True)

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def create_metric_card(label: str, value: str, delta: str = None):
    """
    Cria um card de métrica estilizado.
    
    Args:
        label (str): Rótulo da métrica (ex: "Total de Doadores")
        value (str): Valor da métrica (ex: "150")
        delta (str): Variação da métrica (ex: "+10 este mês")
    
    Retorna um st.metric com estilo consistente do sistema.
    """
    return st.metric(label=label, value=value, delta=delta)

def show_info_message(message: str, icon: str = "ℹ️"):
    """
    Exibe uma mensagem informativa padronizada.
    
    Args:
        message (str): Mensagem a ser exibida
        icon (str): Emoji/ícone para a mensagem (padrão: ℹ️)
    """
    st.info(f"{icon} {message}")

def show_success_message(message: str, icon: str = "✅"):
    """
    Exibe uma mensagem de sucesso padronizada.
    
    Args:
        message (str): Mensagem a ser exibida
        icon (str): Emoji/ícone para a mensagem (padrão: ✅)
    """
    st.success(f"{icon} {message}")

def show_warning_message(message: str, icon: str = "⚠️"):
    """
    Exibe uma mensagem de aviso padronizada.
    
    Args:
        message (str): Mensagem a ser exibida
        icon (str): Emoji/ícone para a mensagem (padrão: ⚠️)
    """
    st.warning(f"{icon} {message}")

def show_error_message(message: str, icon: str = "❌"):
    """
    Exibe uma mensagem de erro padronizada.
    
    Args:
        message (str): Mensagem a ser exibida
        icon (str): Emoji/ícone para a mensagem (padrão: ❌)
    """
    st.error(f"{icon} {message}")
