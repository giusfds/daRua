"""
Página de Gerenciamento de Doadores
Lista, busca e cadastro de novos doadores
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
from utils.mock_data import get_df_doadores

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================

setup_page("Doadores - Somos DaRua", "👤")
apply_global_css()

# ============================================================================
# SIDEBAR - NAVEGAÇÃO
# ============================================================================

render_sidebar("Doadores")

# ============================================================================
# CONTEÚDO PRINCIPAL
# ============================================================================

st.title("👤 Gerenciar Doadores")
st.markdown("Cadastre e gerencie os doadores do sistema")
st.markdown("---")

# Carregar dados mockados
df_doadores = get_df_doadores()

# ============================================================================
# SEÇÃO DE BUSCA E NOVO CADASTRO
# ============================================================================

col1, col2 = st.columns([3, 1])

with col1:
    busca = st.text_input(
        "🔍 Buscar doador",
        placeholder="Pesquisar por nome, email ou telefone...",
        label_visibility="collapsed"
    )

with col2:
    if st.button("➕ Cadastrar Novo Doador", use_container_width=True):
        st.session_state['mostrar_form'] = True

st.markdown("---")

# ============================================================================
# FILTRAR DADOS PELA BUSCA
# ============================================================================

if busca:
    # Filtrar por nome, email ou telefone
    mask = (
        df_doadores['nome'].str.contains(busca, case=False, na=False) |
        df_doadores['email'].str.contains(busca, case=False, na=False) |
        df_doadores['telefone'].str.contains(busca, case=False, na=False)
    )
    df_filtrado = df_doadores[mask]
else:
    df_filtrado = df_doadores

# ============================================================================
# FORMULÁRIO DE CADASTRO
# ============================================================================

if 'mostrar_form' not in st.session_state:
    st.session_state['mostrar_form'] = False

if st.session_state['mostrar_form']:
    with st.expander("📝 Formulário de Cadastro de Doador", expanded=True):
        with st.form("form_doador"):
            st.markdown("### Dados do Doador")
            
            col1, col2 = st.columns(2)
            
            with col1:
                nome = st.text_input("Nome Completo *", placeholder="Ex: João da Silva")
                cpf = st.text_input("CPF *", placeholder="000.000.000-00")
                email = st.text_input("Email", placeholder="exemplo@email.com")
            
            with col2:
                telefone = st.text_input("Telefone", placeholder="(11) 98765-4321")
                endereco = st.text_input("Endereço Completo", placeholder="Rua, número - Bairro, Cidade")
                data_cadastro = st.date_input("Data de Cadastro", value=datetime.now())
            
            st.markdown("---")
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 4])
            
            with col_btn1:
                submit = st.form_submit_button("💾 Salvar", use_container_width=True)
            
            with col_btn2:
                cancelar = st.form_submit_button("❌ Cancelar", use_container_width=True)
            
            # Processar formulário
            if submit:
                if nome and cpf:
                    show_success_message(f"Doador **{nome}** cadastrado com sucesso!")
                    st.balloons()
                    st.session_state['mostrar_form'] = False
                    st.rerun()
                else:
                    show_error_message("Por favor, preencha os campos obrigatórios (Nome e CPF)")
            
            if cancelar:
                st.session_state['mostrar_form'] = False
                st.rerun()

# ============================================================================
# ESTATÍSTICAS RÁPIDAS
# ============================================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total de Doadores", len(df_doadores))

with col2:
    st.metric("Cadastros este Mês", 23)

with col3:
    st.metric("Doadores Ativos", len(df_doadores) - 5)

with col4:
    if busca:
        st.metric("Resultados da Busca", len(df_filtrado))
    else:
        st.metric("Média de Doações/Doador", "7.2")

st.markdown("---")

# ============================================================================
# TABELA DE DOADORES
# ============================================================================

st.markdown("### 📋 Lista de Doadores")

# Preparar dados para exibição
df_display = df_filtrado[['id', 'nome', 'email', 'telefone', 'endereco', 'data_cadastro']].copy()
df_display.columns = ['ID', 'Nome', 'Email', 'Telefone', 'Endereço', 'Data Cadastro']

# Formatar data
df_display['Data Cadastro'] = pd.to_datetime(df_display['Data Cadastro']).dt.strftime('%d/%m/%Y')

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
        "Email": st.column_config.TextColumn(
            "Email",
            width="medium",
        ),
        "Telefone": st.column_config.TextColumn(
            "Telefone",
            width="small",
        ),
        "Endereço": st.column_config.TextColumn(
            "Endereço",
            width="large",
        ),
        "Data Cadastro": st.column_config.TextColumn(
            "Data Cadastro",
            width="small",
        ),
    }
)

# Informação sobre resultados
if busca:
    show_info_message(f"Mostrando {len(df_filtrado)} de {len(df_doadores)} doadores")
else:
    show_info_message(f"Total de {len(df_doadores)} doadores cadastrados")

st.markdown("---")

# ============================================================================
# INFORMAÇÕES ADICIONAIS
# ============================================================================

with st.expander("ℹ️ Informações sobre Gerenciamento de Doadores"):
    st.markdown("""
    ### Como usar esta página:
    
    **Buscar Doadores:**
    - Use a barra de busca para encontrar doadores por nome, email ou telefone
    - A busca é feita em tempo real e não diferencia maiúsculas de minúsculas
    
    **Cadastrar Novo Doador:**
    - Clique no botão "Cadastrar Novo Doador"
    - Preencha os campos obrigatórios (Nome e CPF)
    - Os demais campos são opcionais mas recomendados
    - Clique em "Salvar" para confirmar o cadastro
    
    **Campos Obrigatórios:**
    - Nome Completo (*)
    - CPF (*)
    
    **Campos Opcionais:**
    - Email
    - Telefone
    - Endereço Completo
    
    > 💡 **Dica:** Mantenha os dados dos doadores sempre atualizados para facilitar o contato e a gestão das doações.
    """)

# ============================================================================
# RODAPÉ
# ============================================================================

render_footer()
