"""
Sistema Somos DaRua - Gestão de Doações
Página Principal / Dashboard

Este é o arquivo principal do sistema que serve como página inicial
mostrando métricas, gráficos e visão geral do sistema de gestão de doações.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path

# Adicionar o diretório utils ao path
sys.path.append(str(Path(__file__).parent))

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
from utils.mock_data import get_metricas_dashboard, get_df_doacoes

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

# Carregar dados mockados
metricas = get_metricas_dashboard()

# ============================================================================
# SEÇÃO 1: CARDS DE MÉTRICAS PRINCIPAIS
# ============================================================================

st.markdown("### 📊 Visão Geral")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="👤 Total de Doadores",
        value=f"{metricas['total_doadores']:,}".replace(",", "."),
        delta="+23 este mês"
    )

with col2:
    st.metric(
        label="🤝 Total de Beneficiários",
        value=f"{metricas['total_beneficiarios']:,}".replace(",", "."),
        delta="+12 este mês"
    )

with col3:
    st.metric(
        label="📦 Total de Doações",
        value=f"{metricas['total_doacoes']:,}".replace(",", "."),
        delta="+156 este mês"
    )

with col4:
    st.metric(
        label="📢 Campanhas Ativas",
        value=metricas['campanhas_ativas'],
        delta="3 novas"
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

with col2:
    # Gráfico de Barras - Doações Mensais
    st.markdown("#### Doações nos Últimos 6 Meses")
    df_mensais = pd.DataFrame(
        list(metricas['doacoes_mensais'].items()),
        columns=['Mês', 'Quantidade']
    )
    
    fig_barras = px.bar(
        df_mensais,
        x='Mês',
        y='Quantidade',
        color_discrete_sequence=[COLORS['primary']]
    )
    fig_barras.update_layout(height=400, xaxis_title="", yaxis_title="Quantidade")
    st.plotly_chart(fig_barras, use_container_width=True)

# Linha 2 de gráficos
st.markdown("#### Tendência de Crescimento de Doadores")
df_doadores = pd.DataFrame(
    list(metricas['doadores_mensais'].items()),
    columns=['Mês', 'Doadores']
)

fig_linha = px.line(
    df_doadores,
    x='Mês',
    y='Doadores',
    markers=True,
    color_discrete_sequence=[COLORS['secondary']]
)
fig_linha.update_layout(height=350, xaxis_title="", yaxis_title="Número de Doadores")
st.plotly_chart(fig_linha, use_container_width=True)

st.markdown("---")

# ============================================================================
# SEÇÃO 3: TABELA DE ÚLTIMAS DOAÇÕES
# ============================================================================

st.markdown("### 📋 Últimas Doações Recebidas")

# Preparar dados da tabela
ultimas_doacoes = metricas['ultimas_doacoes']
df_ultimas = pd.DataFrame(ultimas_doacoes)

# Selecionar e renomear colunas para exibição
df_display = df_ultimas[['data', 'doador', 'item', 'quantidade', 'unidade', 'status']].copy()
df_display.columns = ['Data', 'Doador', 'Item', 'Quantidade', 'Unidade', 'Status']

# Aplicar formatação
df_display['Data'] = pd.to_datetime(df_display['Data']).dt.strftime('%d/%m/%Y')

# Exibir tabela com estilo
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

st.markdown("---")

# ============================================================================
# SEÇÃO 4: DESTAQUES E ALERTAS
# ============================================================================

st.markdown("### 🔔 Destaques e Alertas")

col1, col2, col3 = st.columns(3)

with col1:
    show_info_message("🎯 **Meta do Mês**: Arrecadar 1.000 kg de alimentos\n\n**Progresso**: 750 kg (75%)")

with col2:
    show_success_message("**Campanha Natal Solidário** atingiu 84% da meta!")

with col3:
    show_warning_message("**Atenção**: 3 campanhas terminam em 15 dias")

st.markdown("---")

# ============================================================================
# RODAPÉ
# ============================================================================

render_footer()
