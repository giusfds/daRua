"""
Sistema Somos DaRua - Gestão de Doações
Página Principal / Dashboard

Este é o arquivo principal do sistema que serve como página inicial
mostrando métricas, gráficos e visão geral do sistema de gestão de doações.

✅ ATUALIZADO: Agora usa dados REAIS do MySQL via backend/models/dashboard_model.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path

# Adicionar o diretório utils ao path
sys.path.append(str(Path(__file__).parent))

# ============================================================================
# IMPORTANTE: IMPORTAÇÃO DE DADOS REAIS DO BACKEND
# ============================================================================
# Adicionar backend ao path para importar models
backend_path = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

# Importar configurações centralizadas
from utils.config import (
    setup_page,
    apply_global_css,
    render_sidebar,
    render_footer,
    show_info_message,
    show_success_message,
    show_warning_message,
    COLORS
)

# MUDANÇA AQUI: Usar dados reais do banco em vez de mock_data
# from utils.mock_data import get_metricas_dashboard  # DESATIVADO
from models.dashboard_model import get_metricas_dashboard  # ✅ DADOS REAIS

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================

setup_page("Somos DaRua - Gestão de Doações", "🤝")
apply_global_css()

# ============================================================================
# SIDEBAR - NAVEGAÇÃO
# ============================================================================

render_sidebar("Dashboard")

# ============================================================================
# CONTEÚDO PRINCIPAL - DASHBOARD
# ============================================================================

# Header
st.title("🏠 Dashboard - Somos DaRua")
st.markdown("### Sistema de Gestão de Doações")
st.markdown("---")

# ============================================================================
# CARREGAR DADOS REAIS DO BANCO
# ============================================================================

try:
    # Esta função busca TODOS os dados do banco MySQL
    metricas = get_metricas_dashboard()
    
    # Verificar se conseguiu conectar
    if not metricas or (metricas.get('total_doadores', 0) == 0 and 
                        metricas.get('total_beneficiarios', 0) == 0 and 
                        metricas.get('total_doacoes', 0) == 0):
        st.warning("⚠️ Banco parece vazio. Cadastre alguns dados primeiro!")
        st.info("💡 Acesse as páginas de cadastro no menu lateral para adicionar doadores, beneficiários, etc.")
        
except Exception as e:
    st.error(f"❌ Erro ao conectar com banco de dados: {e}")
    st.info("💡 Verifique se:")
    st.markdown("""
    1. MySQL está rodando
    2. Banco 'somos_darua' foi criado (`python backend/database/setup.py`)
    3. Credenciais no `.env` estão corretas
    4. Rode as migrations em `/database/migrations/` se necessário
    """)
    st.stop()

# ============================================================================
# SEÇÃO 1: CARDS DE MÉTRICAS PRINCIPAIS
# ============================================================================

st.markdown("### 📊 Visão Geral")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="👤 Total de Doadores",
        value=f"{metricas['total_doadores']:,}".replace(",", "."),
        delta="+23 este mês"  # TODO: Calcular delta real
    )

with col2:
    st.metric(
        label="🤝 Total de Beneficiários",
        value=f"{metricas['total_beneficiarios']:,}".replace(",", "."),
        delta="+12 este mês"  # TODO: Calcular delta real
    )

with col3:
    st.metric(
        label="📦 Total de Doações",
        value=f"{metricas['total_doacoes']:,}".replace(",", "."),
        delta="+156 este mês"  # TODO: Calcular delta real
    )

with col4:
    st.metric(
        label="📢 Campanhas Ativas",
        value=metricas['campanhas_ativas'],
        delta="3 novas"  # TODO: Calcular delta real
    )

st.markdown("---")

# ============================================================================
# SEÇÃO 2: GRÁFICOS
# ============================================================================

st.markdown("### 📈 Análises e Tendências")

# Linha 1 de gráficos
col1, col2 = st.columns(2)

with col1:
    # Gráfico de Pizza - Doações por Categoria
    st.markdown("#### Doações por Categoria")
    
    if metricas['doacoes_por_categoria']:
        df_categorias = pd.DataFrame(
            list(metricas['doacoes_por_categoria'].items()),
            columns=['Categoria', 'Quantidade']
        )
        
        fig_pizza = px.pie(
            df_categorias,
            values='Quantidade',
            names='Categoria',
            color_discrete_sequence=[
                COLORS['primary'], 
                COLORS['secondary'], 
                COLORS['success'], 
                COLORS['warning']
            ]
        )
        fig_pizza.update_traces(textposition='inside', textinfo='percent+label')
        fig_pizza.update_layout(height=400)
        st.plotly_chart(fig_pizza, use_container_width=True)
    else:
        st.info("📝 Execute `add_doacoes_detalhes.sql` para ter dados por categoria")

with col2:
    # Gráfico de Barras - Doações Mensais
    st.markdown("#### Doações nos Últimos 6 Meses")
    
    if metricas['doacoes_mensais']:
        df_mensais = pd.DataFrame(
            list(metricas['doacoes_mensais'].items()),
            columns=['Mês', 'Quantidade']
        )
        
        # Formatar mês (2024-11 → Nov/24)
        df_mensais['Mês'] = pd.to_datetime(df_mensais['Mês']).dt.strftime('%b/%y')
        
        fig_barras = px.bar(
            df_mensais,
            x='Mês',
            y='Quantidade',
            color_discrete_sequence=[COLORS['primary']]
        )
        fig_barras.update_layout(height=400, xaxis_title="", yaxis_title="Quantidade")
        st.plotly_chart(fig_barras, use_container_width=True)
    else:
        st.info("Nenhuma doação nos últimos 6 meses")

# Linha 2 de gráficos
st.markdown("#### Tendência de Crescimento de Doadores")

if metricas['doadores_mensais']:
    df_doadores = pd.DataFrame(
        list(metricas['doadores_mensais'].items()),
        columns=['Mês', 'Doadores']
    )
    
    # Formatar mês
    df_doadores['Mês'] = pd.to_datetime(df_doadores['Mês']).dt.strftime('%b/%y')
    
    fig_linha = px.line(
        df_doadores,
        x='Mês',
        y='Doadores',
        markers=True,
        color_discrete_sequence=[COLORS['secondary']]
    )
    fig_linha.update_layout(height=350, xaxis_title="", yaxis_title="Número de Doadores")
    st.plotly_chart(fig_linha, use_container_width=True)
else:
    st.info("Nenhum doador com doações nos últimos 6 meses")

st.markdown("---")

# ============================================================================
# SEÇÃO 3: TABELA DE ÚLTIMAS DOAÇÕES
# ============================================================================

st.markdown("### 📋 Últimas Doações Recebidas")

if metricas['ultimas_doacoes']:
    df_ultimas = pd.DataFrame(metricas['ultimas_doacoes'])
    
    # Selecionar e renomear colunas
    df_display = df_ultimas[['data', 'doador', 'item', 'quantidade', 'unidade', 'status']].copy()
    df_display.columns = ['Data', 'Doador', 'Item', 'Quantidade', 'Unidade', 'Status']
    
    # Formatar data
    df_display['Data'] = pd.to_datetime(df_display['Data']).dt.strftime('%d/%m/%Y')
    
    # Exibir tabela
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Status": st.column_config.TextColumn(
                "Status",
                width="medium",
            )
        }
    )
else:
    st.info("Nenhuma doação cadastrada ainda. Cadastre doadores e doações nas páginas do menu!")

st.markdown("---")

# ============================================================================
# SEÇÃO 4: DESTAQUES E ALERTAS
# ============================================================================

st.markdown("### 🔔 Destaques e Alertas")

col1, col2, col3 = st.columns(3)

with col1:
    # TODO: Buscar meta real das campanhas
    show_info_message("🎯 **Meta do Mês**: Arrecadar 1.000 kg de alimentos\n\n**Progresso**: 750 kg (75%)")

with col2:
    # TODO: Calcular progresso real das campanhas
    show_success_message("**Campanha Natal Solidário** atingiu 84% da meta!")

with col3:
    # TODO: Buscar campanhas que terminam em breve
    show_warning_message("**Atenção**: 3 campanhas terminam em 15 dias")

st.markdown("---")

# ============================================================================
# RODAPÉ
# ============================================================================

render_footer()

# ============================================================================
# DEBUG (remover em produção)
# ============================================================================
# Descomente para ver dados brutos:
# with st.expander("🐛 Debug - Dados do Banco"):
#     st.json(metricas)