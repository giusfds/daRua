"""
Página de Relatórios e Estatísticas
Visualiza relatórios detalhados e estatísticas do sistema
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Adicionar o diretório utils ao path
sys.path.append(str(Path(__file__).parent.parent))

# Importar configurações centralizadas
from utils.config import (
    setup_page,
    apply_global_css,
    render_sidebar,
    render_footer,
    show_success_message,
    show_info_message,
    COLORS
)
from utils.mock_data import (
    get_metricas_dashboard, get_df_doacoes, get_df_doadores,
    get_df_beneficiarios, get_campanhas_mockadas
)

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================

setup_page("Relatórios - Somos DaRua", "📊")
apply_global_css()

# ============================================================================
# SIDEBAR - NAVEGAÇÃO
# ============================================================================

render_sidebar("Relatórios")

# ============================================================================
# CONTEÚDO PRINCIPAL
# ============================================================================

st.title("📊 Relatórios e Estatísticas")
st.markdown("Visualize estatísticas detalhadas e gere relatórios do sistema")
st.markdown("---")

# Carregar dados mockados
metricas = get_metricas_dashboard()
df_doacoes = get_df_doacoes()
df_doadores = get_df_doadores()
df_beneficiarios = get_df_beneficiarios()
campanhas = get_campanhas_mockadas()

# ============================================================================
# FILTROS DE PERÍODO E TIPO DE RELATÓRIO
# ============================================================================

col1, col2, col3 = st.columns([2, 2, 2])

with col1:
    data_inicio = st.date_input(
        "Data Início",
        value=datetime.now() - timedelta(days=180),
        max_value=datetime.now()
    )

with col2:
    data_fim = st.date_input(
        "Data Fim",
        value=datetime.now(),
        max_value=datetime.now()
    )

with col3:
    tipo_relatorio = st.selectbox(
        "Tipo de Relatório",
        ["Visão Geral", "Doações", "Doadores", "Beneficiários", "Campanhas"]
    )

st.markdown("---")

# ============================================================================
# SEÇÃO 1 - VISÃO GERAL COM COMPARAÇÕES
# ============================================================================

st.markdown("### 📈 Visão Geral")

col1, col2, col3, col4 = st.columns(4)

# Calcular variações (simuladas)
with col1:
    st.metric(
        label="👤 Total de Doadores",
        value=f"{metricas['total_doadores']:,}".replace(",", "."),
        delta="+8.5%",
        delta_color="normal"
    )

with col2:
    st.metric(
        label="🤝 Total de Beneficiários",
        value=f"{metricas['total_beneficiarios']:,}".replace(",", "."),
        delta="+12.3%",
        delta_color="normal"
    )

with col3:
    st.metric(
        label="📦 Total de Doações",
        value=f"{metricas['total_doacoes']:,}".replace(",", "."),
        delta="+15.7%",
        delta_color="normal"
    )

with col4:
    st.metric(
        label="📢 Campanhas Ativas",
        value=metricas['campanhas_ativas'],
        delta="+3",
        delta_color="normal"
    )

st.markdown("---")

# ============================================================================
# SEÇÃO 2 - GRÁFICOS DETALHADOS
# ============================================================================

st.markdown("### 📊 Análises Detalhadas")

# Gráfico de Pizza - Distribuição por Tipo de Doação
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Distribuição por Tipo de Doação")
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
        ],
        hole=0.4
    )
    fig_pizza.update_traces(textposition='inside', textinfo='percent+label')
    fig_pizza.update_layout(height=400, showlegend=True)
    st.plotly_chart(fig_pizza, use_container_width=True)

with col2:
    st.markdown("#### Ranking de Doadores (Top 10)")
    # Criar dados fictícios para ranking
    top_doadores = pd.DataFrame({
        'Doador': [
            'João Silva', 'Maria Santos', 'Pedro Oliveira', 'Ana Costa',
            'Carlos Souza', 'Juliana Almeida', 'Ricardo Ferreira', 'Fernanda Lima',
            'Paulo Rodrigues', 'Mariana Carvalho'
        ],
        'Doações': [45, 38, 32, 28, 25, 22, 20, 18, 15, 12]
    })
    
    fig_ranking = px.bar(
        top_doadores,
        x='Doações',
        y='Doador',
        orientation='h',
        color='Doações',
        color_continuous_scale=[[0, COLORS['background']], [1, COLORS['primary']]]
    )
    fig_ranking.update_layout(height=400, showlegend=False, yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_ranking, use_container_width=True)

st.markdown("---")

# Gráfico de Linha - Evolução Mensal
st.markdown("#### Evolução Mensal de Doações")

meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
valores_2024 = [1200, 1350, 1100, 1450, 1600, 1800, 1650, 1750, 1900, 2050, 2200, 2400]
valores_2023 = [980, 1050, 890, 1150, 1280, 1420, 1380, 1450, 1550, 1680, 1820, 1950]

df_evolucao = pd.DataFrame({
    'Mês': meses * 2,
    'Doações': valores_2024 + valores_2023,
    'Ano': ['2024'] * 12 + ['2023'] * 12
})

fig_linha = px.line(
    df_evolucao,
    x='Mês',
    y='Doações',
    color='Ano',
    markers=True,
    color_discrete_map={'2024': COLORS['primary'], '2023': COLORS['text_dark']}
)
fig_linha.update_layout(height=400)
st.plotly_chart(fig_linha, use_container_width=True)

st.markdown("---")

# Gráfico de Área - Novos Cadastros
st.markdown("#### Novos Cadastros por Mês (Doadores e Beneficiários)")

df_cadastros = pd.DataFrame({
    'Mês': meses,
    'Doadores': [15, 18, 21, 25, 29, 32, 28, 31, 35, 38, 42, 45],
    'Beneficiários': [8, 10, 12, 15, 11, 13, 16, 14, 18, 20, 22, 25]
})

fig_area = go.Figure()
fig_area.add_trace(go.Scatter(
    x=df_cadastros['Mês'], y=df_cadastros['Doadores'],
    mode='lines', name='Doadores',
    fill='tonexty', line=dict(color=COLORS['primary'])
))
fig_area.add_trace(go.Scatter(
    x=df_cadastros['Mês'], y=df_cadastros['Beneficiários'],
    mode='lines', name='Beneficiários',
    fill='tozeroy', line=dict(color=COLORS['secondary'])
))
fig_area.update_layout(height=400, xaxis_title="", yaxis_title="Quantidade")
st.plotly_chart(fig_area, use_container_width=True)

st.markdown("---")

# ============================================================================
# SEÇÃO 3 - TABELAS DETALHADAS
# ============================================================================

st.markdown("### 📋 Tabelas Detalhadas")

tab1, tab2, tab3 = st.tabs(["Campanhas", "Doadores Ativos", "Beneficiários Atendidos"])

with tab1:
    st.markdown("#### Resumo de Campanhas")
    
    # Preparar dados das campanhas
    df_campanhas = pd.DataFrame(campanhas)
    df_campanhas['% Atingido'] = (df_campanhas['arrecadado'] / df_campanhas['meta'] * 100).round(1)
    
    df_campanhas_display = df_campanhas[['nome', 'meta', 'tipo_meta', 'arrecadado', '% Atingido', 'status']].copy()
    df_campanhas_display.columns = ['Campanha', 'Meta', 'Tipo', 'Arrecadado', '% Atingido', 'Status']
    
    st.dataframe(
        df_campanhas_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Campanha": st.column_config.TextColumn("Campanha", width="large"),
            "Meta": st.column_config.NumberColumn("Meta", format="%d"),
            "Tipo": st.column_config.TextColumn("Tipo", width="small"),
            "Arrecadado": st.column_config.NumberColumn("Arrecadado", format="%d"),
            "% Atingido": st.column_config.ProgressColumn(
                "% Atingido",
                min_value=0,
                max_value=100,
                format="%.1f%%"
            ),
            "Status": st.column_config.TextColumn("Status", width="small"),
        }
    )

with tab2:
    st.markdown("#### Doadores Mais Ativos")
    
    # Criar dados de doadores ativos (simulados)
    doadores_ativos = pd.DataFrame({
        'Nome': [
            'João Silva', 'Maria Santos', 'Pedro Oliveira', 'Ana Costa',
            'Carlos Souza', 'Juliana Almeida', 'Ricardo Ferreira', 'Fernanda Lima',
            'Paulo Rodrigues', 'Mariana Carvalho', 'Lucas Martins', 'Patrícia Ribeiro'
        ],
        'Total Doações': [45, 38, 32, 28, 25, 22, 20, 18, 15, 12, 10, 8],
        'Última Doação': [
            '2024-11-08', '2024-11-10', '2024-11-05', '2024-11-09',
            '2024-11-07', '2024-11-11', '2024-11-06', '2024-11-04',
            '2024-11-10', '2024-11-03', '2024-11-02', '2024-11-01'
        ],
        'Valor Total (R$)': [4500, 3800, 3200, 2800, 2500, 2200, 2000, 1800, 1500, 1200, 1000, 800]
    })
    
    st.dataframe(
        doadores_ativos,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Nome": st.column_config.TextColumn("Nome", width="medium"),
            "Total Doações": st.column_config.NumberColumn("Total de Doações"),
            "Última Doação": st.column_config.DateColumn("Última Doação"),
            "Valor Total (R$)": st.column_config.NumberColumn(
                "Valor Total (R$)",
                format="R$ %.2f"
            ),
        }
    )

with tab3:
    st.markdown("#### Beneficiários Atendidos")
    
    # Dados simulados de beneficiários
    beneficiarios_atendidos = df_beneficiarios[df_beneficiarios['status'] == 'Ativo'].head(15)
    df_benef_display = beneficiarios_atendidos[['nome', 'idade', 'necessidades', 'data_cadastro']].copy()
    df_benef_display.columns = ['Nome', 'Idade', 'Necessidades', 'Data Cadastro']
    
    st.dataframe(
        df_benef_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Nome": st.column_config.TextColumn("Nome", width="medium"),
            "Idade": st.column_config.NumberColumn("Idade", width="small"),
            "Necessidades": st.column_config.TextColumn("Necessidades", width="large"),
            "Data Cadastro": st.column_config.DateColumn("Data de Cadastro"),
        }
    )

st.markdown("---")

# ============================================================================
# SEÇÃO 4 - EXPORTAÇÃO
# ============================================================================

st.markdown("### 📥 Exportar Relatórios")

col1, col2, col3, col4 = st.columns([1, 1, 1, 3])

with col1:
    if st.button("📄 Baixar PDF", use_container_width=True):
        show_info_message("Funcionalidade de exportação PDF será implementada em breve!", "🚧")

with col2:
    if st.button("📊 Exportar Excel", use_container_width=True):
        show_info_message("Funcionalidade de exportação Excel será implementada em breve!", "🚧")

with col3:
    if st.button("📧 Enviar por Email", use_container_width=True):
        show_info_message("Funcionalidade de envio por email será implementada em breve!", "🚧")

st.markdown("---")

# ============================================================================
# INSIGHTS E DESTAQUES
# ============================================================================

st.markdown("### 💡 Insights e Destaques")

col1, col2, col3 = st.columns(3)

with col1:
    show_success_message("""**Crescimento Positivo**
    
As doações aumentaram 15.7% no último trimestre, superando a meta estabelecida.""", "📈")

with col2:
    show_info_message("""**Meta Alcançada**
    
4 campanhas atingiram 100% da meta este mês, beneficiando 350 famílias.""", "🎯")

with col3:
    show_info_message("""**Atenção Necessária**
    
3 campanhas estão com baixo desempenho e podem precisar de divulgação adicional.""", "⚠️")

st.markdown("---")

# ============================================================================
# INFORMAÇÕES ADICIONAIS
# ============================================================================

with st.expander("ℹ️ Informações sobre Relatórios e Estatísticas"):
    st.markdown("""
    ### Como usar esta página:
    
    **Filtrar Dados:**
    - Use os campos "Data Início" e "Data Fim" para definir o período
    - Selecione o tipo de relatório desejado
    - Os gráficos e tabelas serão atualizados automaticamente
    
    **Tipos de Relatórios Disponíveis:**
    - **Visão Geral:** Resumo completo de todas as métricas
    - **Doações:** Análise detalhada das doações recebidas
    - **Doadores:** Estatísticas sobre doadores e suas contribuições
    - **Beneficiários:** Informações sobre beneficiários atendidos
    - **Campanhas:** Desempenho e resultados das campanhas
    
    **Interpretar os Gráficos:**
    
    1. **Gráfico de Pizza:** Mostra a distribuição percentual das doações por categoria
    2. **Ranking de Doadores:** Top 10 doadores mais ativos
    3. **Evolução Mensal:** Tendência de doações ao longo do tempo
    4. **Novos Cadastros:** Crescimento da base de doadores e beneficiários
    
    **Tabelas Detalhadas:**
    - **Campanhas:** Status, metas e percentual atingido
    - **Doadores Ativos:** Ranking por número de doações
    - **Beneficiários:** Lista de pessoas sendo atendidas
    
    **Exportar Relatórios:**
    - **PDF:** Gera documento formatado para impressão
    - **Excel:** Exporta dados para análise em planilhas
    - **Email:** Envia relatório por email para destinatários
    
    **Métricas e Indicadores:**
    - **Delta (%):** Indica crescimento ou queda em relação ao período anterior
    - **Verde:** Crescimento positivo
    - **Vermelho:** Queda ou resultado negativo
    - **Cinza:** Sem variação significativa
    
    **Boas Práticas:**
    - Gere relatórios mensais para acompanhar tendências
    - Compare períodos similares (mês a mês, ano a ano)
    - Use os insights para tomar decisões estratégicas
    - Compartilhe resultados com a equipe e doadores
    - Documente aprendizados e sucessos
    
    > 💡 **Dica:** Relatórios regulares ajudam a identificar padrões, melhorar processos e demonstrar impacto!
    """)

# ============================================================================
# RODAPÉ
# ============================================================================

render_footer()
