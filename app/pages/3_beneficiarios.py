"""
Página de Gerenciamento de Beneficiários
Lista, busca e cadastro de pessoas beneficiadas
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path
from datetime import datetime

# Adicionar o diretório utils ao path
sys.path.append(str(Path(__file__).parent.parent))

# Importar configurações centralizadas
from utils.config import (
    setup_page,
    apply_global_css,
    render_sidebar,
    render_footer,
    show_success_message,
    show_error_message,
    show_info_message
)
from utils.mock_data import get_df_beneficiarios

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================

setup_page("Beneficiários - Somos DaRua", "🤝")
apply_global_css()

# ============================================================================
# SIDEBAR - NAVEGAÇÃO
# ============================================================================

render_sidebar("Beneficiários")

# ============================================================================
# CONTEÚDO PRINCIPAL
# ============================================================================

st.title("🤝 Gerenciar Beneficiários")
st.markdown("Cadastre e gerencie os beneficiários do sistema")
st.markdown("---")

# Carregar dados mockados
df_beneficiarios = get_df_beneficiarios()

# ============================================================================
# SEÇÃO DE BUSCA, FILTROS E NOVO CADASTRO
# ============================================================================

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    busca = st.text_input(
        "🔍 Buscar beneficiário",
        placeholder="Pesquisar por nome...",
        label_visibility="collapsed"
    )

with col2:
    filtro_status = st.selectbox(
        "Filtrar por Status",
        ["Todos", "Ativo", "Inativo", "Aguardando"],
        label_visibility="collapsed"
    )

with col3:
    if st.button("➕ Cadastrar Novo Beneficiário", use_container_width=True):
        st.session_state['mostrar_form_benef'] = True

st.markdown("---")

# ============================================================================
# FILTRAR DADOS
# ============================================================================

df_filtrado = df_beneficiarios.copy()

# Filtrar por busca
if busca:
    df_filtrado = df_filtrado[
        df_filtrado['nome'].str.contains(busca, case=False, na=False)
    ]

# Filtrar por status
if filtro_status != "Todos":
    df_filtrado = df_filtrado[df_filtrado['status'] == filtro_status]

# ============================================================================
# FORMULÁRIO DE CADASTRO
# ============================================================================

if 'mostrar_form_benef' not in st.session_state:
    st.session_state['mostrar_form_benef'] = False

if st.session_state['mostrar_form_benef']:
    with st.expander("📝 Formulário de Cadastro de Beneficiário", expanded=True):
        with st.form("form_beneficiario"):
            st.markdown("### Dados do Beneficiário")
            
            col1, col2 = st.columns(2)
            
            with col1:
                nome = st.text_input("Nome Completo *", placeholder="Ex: Maria das Graças")
                data_nascimento = st.date_input(
                    "Data de Nascimento",
                    value=datetime(2000, 1, 1),
                    min_value=datetime(1930, 1, 1),
                    max_value=datetime.now()
                )
                genero = st.selectbox(
                    "Gênero",
                    ["Masculino", "Feminino", "Outro", "Prefiro não informar"]
                )
            
            with col2:
                descricao = st.text_area(
                    "Descrição da Situação",
                    placeholder="Descreva brevemente a situação do beneficiário...",
                    height=100
                )
                status = st.selectbox(
                    "Status",
                    ["Ativo", "Inativo", "Aguardando"]
                )
            
            st.markdown("### Necessidades Principais")
            
            necessidades = st.multiselect(
                "Selecione as necessidades",
                ["Alimentação", "Vestuário", "Abrigo", "Saúde", "Educação"],
                default=["Alimentação"]
            )
            
            st.markdown("---")
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 4])
            
            with col_btn1:
                submit = st.form_submit_button("💾 Salvar", use_container_width=True)
            
            with col_btn2:
                cancelar = st.form_submit_button("❌ Cancelar", use_container_width=True)
            
            # Processar formulário
            if submit:
                if nome:
                    show_success_message(f"Beneficiário **{nome}** cadastrado com sucesso!")
                    st.balloons()
                    st.session_state['mostrar_form_benef'] = False
                    st.rerun()
                else:
                    show_error_message("Por favor, preencha o campo Nome Completo")
            
            if cancelar:
                st.session_state['mostrar_form_benef'] = False
                st.rerun()

# ============================================================================
# ESTATÍSTICAS RÁPIDAS
# ============================================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total de Beneficiários", len(df_beneficiarios))

with col2:
    ativos = len(df_beneficiarios[df_beneficiarios['status'] == 'Ativo'])
    st.metric("Beneficiários Ativos", ativos)

with col3:
    aguardando = len(df_beneficiarios[df_beneficiarios['status'] == 'Aguardando'])
    st.metric("Aguardando Atendimento", aguardando)

with col4:
    if busca or filtro_status != "Todos":
        st.metric("Resultados", len(df_filtrado))
    else:
        cadastros_mes = 12
        st.metric("Cadastros este Mês", cadastros_mes)

st.markdown("---")

# ============================================================================
# TABELA DE BENEFICIÁRIOS
# ============================================================================

st.markdown("### 📋 Lista de Beneficiários")

# Preparar dados para exibição
df_display = df_filtrado[['id', 'nome', 'idade', 'genero', 'descricao', 'necessidades', 'status']].copy()
df_display.columns = ['ID', 'Nome', 'Idade', 'Gênero', 'Descrição', 'Necessidades', 'Status']

# Exibir tabela
st.dataframe(
    df_display,
    use_container_width=True,
    hide_index=True,
    column_config={
        "ID": st.column_config.NumberColumn(
            "ID",
            width="small",
        ),
        "Nome": st.column_config.TextColumn(
            "Nome",
            width="medium",
        ),
        "Idade": st.column_config.NumberColumn(
            "Idade",
            width="small",
        ),
        "Gênero": st.column_config.TextColumn(
            "Gênero",
            width="small",
        ),
        "Descrição": st.column_config.TextColumn(
            "Descrição",
            width="large",
        ),
        "Necessidades": st.column_config.TextColumn(
            "Necessidades",
            width="medium",
        ),
        "Status": st.column_config.TextColumn(
            "Status",
            width="small",
        ),
    }
)

# Informação sobre resultados
if busca or filtro_status != "Todos":
    show_info_message(f"Mostrando {len(df_filtrado)} de {len(df_beneficiarios)} beneficiários")
else:
    show_info_message(f"Total de {len(df_beneficiarios)} beneficiários cadastrados")

st.markdown("---")

# ============================================================================
# GRÁFICOS E ANÁLISES
# ============================================================================

st.markdown("### 📊 Análises")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Distribuição por Status")
    status_counts = df_beneficiarios['status'].value_counts()
    st.bar_chart(status_counts)

with col2:
    st.markdown("#### Faixa Etária")
    # Criar faixas etárias
    bins = [0, 18, 30, 50, 65, 100]
    labels = ['0-17', '18-29', '30-49', '50-64', '65+']
    df_beneficiarios['faixa_etaria'] = pd.cut(df_beneficiarios['idade'], bins=bins, labels=labels, right=False)
    faixa_counts = df_beneficiarios['faixa_etaria'].value_counts().sort_index()
    st.bar_chart(faixa_counts)

st.markdown("---")

# ============================================================================
# INFORMAÇÕES ADICIONAIS
# ============================================================================

with st.expander("ℹ️ Informações sobre Gerenciamento de Beneficiários"):
    st.markdown("""
    ### Como usar esta página:
    
    **Buscar Beneficiários:**
    - Use a barra de busca para encontrar beneficiários por nome
    - Use o filtro de status para visualizar apenas Ativos, Inativos ou Aguardando
    - Os filtros podem ser combinados
    
    **Cadastrar Novo Beneficiário:**
    - Clique no botão "Cadastrar Novo Beneficiário"
    - Preencha o campo obrigatório (Nome Completo)
    - Informe a data de nascimento para cálculo automático da idade
    - Selecione o gênero
    - Descreva brevemente a situação da pessoa
    - Marque as necessidades principais
    - Defina o status inicial
    
    **Status dos Beneficiários:**
    - **Ativo:** Beneficiário em atendimento regular
    - **Inativo:** Beneficiário que não está mais sendo atendido
    - **Aguardando:** Beneficiário cadastrado aguardando início do atendimento
    
    **Necessidades:**
    - Alimentação: Precisa de cestas básicas, refeições
    - Vestuário: Precisa de roupas, calçados
    - Abrigo: Precisa de moradia temporária ou permanente
    - Saúde: Precisa de medicamentos, consultas
    - Educação: Precisa de material escolar, cursos
    
    > 💡 **Dica:** Mantenha as informações atualizadas para melhor direcionar as doações e campanhas.
    """)

# ============================================================================
# RODAPÉ
# ============================================================================

render_footer()
