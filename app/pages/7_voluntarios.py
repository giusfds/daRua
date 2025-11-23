"""
Página de Gerenciamento de Voluntários
Cadastra e gerencia voluntários da organização
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path
from datetime import datetime

# Adicionar o diretório utils ao path
sys.path.append(str(Path(__file__).parent.parent))

# Adicionar backend ao path
backend_path = Path(__file__).parent.parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

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

# Importar modelo do backend
from models.voluntario import Voluntario

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================

setup_page("Voluntários - Somos DaRua", "🙋")
apply_global_css()

# ============================================================================
# SIDEBAR - NAVEGAÇÃO
# ============================================================================

render_sidebar("Voluntários")

# ============================================================================
# CONTEÚDO PRINCIPAL
# ============================================================================

st.title("🙋 Cadastro de Voluntários")
st.markdown("Cadastre e gerencie os voluntários da organização")
st.markdown("---")

# Carregar dados do banco
try:
    voluntarios_list = Voluntario.get_all()
    if voluntarios_list:
        df_voluntarios = pd.DataFrame([v.to_dict() for v in voluntarios_list])
        # Adicionar colunas de compatibilidade
        if 'id' not in df_voluntarios.columns and 'idVoluntario' in df_voluntarios.columns:
            df_voluntarios['id'] = df_voluntarios['idVoluntario']
        if 'areas_atuacao' not in df_voluntarios.columns:
            df_voluntarios['areas_atuacao'] = 'Atendimento'
        if 'disponibilidade' not in df_voluntarios.columns:
            df_voluntarios['disponibilidade'] = 'Segunda a Sexta'
        if 'periodo' not in df_voluntarios.columns:
            df_voluntarios['periodo'] = 'Manhã'
        if 'status' not in df_voluntarios.columns:
            df_voluntarios['status'] = 'Ativo'
    else:
        df_voluntarios = pd.DataFrame(columns=['id', 'nome', 'email', 'telefone', 'areas_atuacao', 'disponibilidade', 'periodo', 'status'])
except Exception as e:
    show_error_message(f"Erro ao carregar voluntários: {str(e)}")
    df_voluntarios = pd.DataFrame(columns=['id', 'nome', 'email', 'telefone', 'areas_atuacao', 'disponibilidade', 'periodo', 'status'])

# ============================================================================
# BUSCA, FILTROS E NOVO CADASTRO
# ============================================================================

col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

with col1:
    busca = st.text_input(
        "🔍 Buscar voluntário",
        placeholder="Pesquisar por nome, email ou telefone...",
        label_visibility="collapsed"
    )

with col2:
    filtro_status = st.selectbox(
        "Status",
        ["Todos", "Ativo", "Inativo"],
        label_visibility="collapsed"
    )

with col3:
    filtro_area = st.selectbox(
        "Área de Atuação",
        ["Todas", "Logística", "Triagem", "Atendimento", "Administração", "TI"],
        label_visibility="collapsed"
    )

with col4:
    if st.button("➕ Cadastrar Voluntário", use_container_width=True):
        st.session_state['mostrar_form_voluntario'] = True

st.markdown("---")

# ============================================================================
# FORMULÁRIO DE CADASTRO
# ============================================================================

if 'mostrar_form_voluntario' not in st.session_state:
    st.session_state['mostrar_form_voluntario'] = False

if st.session_state['mostrar_form_voluntario']:
    with st.expander("📝 Formulário de Cadastro de Voluntário", expanded=True):
        with st.form("form_voluntario"):
            st.markdown("### Dados Pessoais")
            
            col1, col2 = st.columns(2)
            
            with col1:
                nome = st.text_input("Nome Completo *", placeholder="Ex: Alexandre Pereira")
                email = st.text_input("Email *", placeholder="exemplo@email.com")
            
            with col2:
                telefone = st.text_input("Telefone *", placeholder="(11) 98765-4321")
            
            st.markdown("---")
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 4])
            
            with col_btn1:
                submit = st.form_submit_button("✅ Cadastrar", use_container_width=True)
            
            with col_btn2:
                cancelar = st.form_submit_button("❌ Cancelar", use_container_width=True)
            
            # Processar formulário
            if submit:
                if nome and email and telefone:
                    try:
                        # Criar objeto Voluntario
                        voluntario = Voluntario(
                            nome=nome,
                            email=email,
                            telefone=telefone
                        )
                        
                        # Salvar no banco
                        if voluntario.save():
                            show_success_message(f"Voluntário **{nome}** cadastrado com sucesso!")
                            show_success_message(f"Email: {email} | Telefone: {telefone}")
                            st.balloons()
                            st.session_state['mostrar_form_voluntario'] = False
                            st.rerun()
                        else:
                            show_error_message("Erro ao salvar voluntário no banco de dados")
                    except Exception as e:
                        show_error_message(f"Erro ao cadastrar voluntário: {str(e)}")
                else:
                    show_error_message("Por favor, preencha todos os campos obrigatórios (*)")
            
            if cancelar:
                st.session_state['mostrar_form_voluntario'] = False
                st.rerun()

# ============================================================================
# FILTRAR DADOS
# ============================================================================

df_filtrado = df_voluntarios.copy()

# Filtrar por busca
if busca and not df_filtrado.empty:
    try:
        mask = (
            df_filtrado['nome'].str.contains(busca, case=False, na=False) |
            df_filtrado['email'].str.contains(busca, case=False, na=False) |
            df_filtrado['telefone'].str.contains(busca, case=False, na=False)
        )
        df_filtrado = df_filtrado[mask]
    except:
        pass

# Filtrar por status
if filtro_status != "Todos" and not df_filtrado.empty:
    try:
        df_filtrado = df_filtrado[df_filtrado['status'] == filtro_status]
    except:
        pass

# Filtrar por área
if filtro_area != "Todas" and not df_filtrado.empty:
    try:
        df_filtrado = df_filtrado[df_filtrado['areas_atuacao'].str.contains(filtro_area, case=False, na=False)]
    except:
        pass

# ============================================================================
# ESTATÍSTICAS RÁPIDAS
# ============================================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    try:
        total = len(df_voluntarios) if not df_voluntarios.empty else 0
        st.metric("Total de Voluntários", total)
    except:
        st.metric("Total de Voluntários", 0)

with col2:
    try:
        if not df_voluntarios.empty and 'status' in df_voluntarios.columns:
            ativos = len(df_voluntarios[df_voluntarios['status'] == 'Ativo'])
        else:
            ativos = 0
        st.metric("Voluntários Ativos", ativos)
    except:
        st.metric("Voluntários Ativos", 0)

with col3:
    st.metric("Aguardando Aprovação", "-")

with col4:
    if busca or filtro_status != "Todos" or filtro_area != "Todas":
        st.metric("Resultados", len(df_filtrado))
    else:
        st.metric("Cadastros este Mês", "-")

st.markdown("---")

# ============================================================================
# TABELA DE VOLUNTÁRIOS
# ============================================================================

st.markdown("### 📋 Lista de Voluntários")

if not df_filtrado.empty:
    # Preparar dados para exibição
    df_display = df_filtrado[['id', 'nome', 'email', 'telefone', 'areas_atuacao', 'disponibilidade', 'periodo', 'status']].copy()
    df_display.columns = ['ID', 'Nome', 'Email', 'Telefone', 'Áreas de Atuação', 'Disponibilidade', 'Período', 'Status']
    
    # Exibir tabela
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ID": st.column_config.NumberColumn("ID", width="small"),
            "Nome": st.column_config.TextColumn("Nome", width="medium"),
            "Email": st.column_config.TextColumn("Email", width="medium"),
            "Telefone": st.column_config.TextColumn("Telefone", width="small"),
            "Áreas de Atuação": st.column_config.TextColumn("Áreas de Atuação", width="medium"),
            "Disponibilidade": st.column_config.TextColumn("Disponibilidade", width="medium"),
            "Período": st.column_config.TextColumn("Período", width="small"),
            "Status": st.column_config.TextColumn("Status", width="small"),
        }
    )
else:
    show_info_message("Nenhum voluntário encontrado")

# Informação sobre resultados
if busca or filtro_status != "Todos" or filtro_area != "Todas":
    show_info_message(f"Mostrando {len(df_filtrado)} de {len(df_voluntarios)} voluntários")
else:
    show_info_message(f"Total de {len(df_voluntarios)} voluntários cadastrados")

st.markdown("---")

# ============================================================================
# INFORMAÇÕES ADICIONAIS
# ============================================================================

with st.expander("ℹ️ Informações sobre Gerenciamento de Voluntários"):
    st.markdown("""
    ### Como usar esta página:
    
    **Cadastrar Novo Voluntário:**
    1. Clique no botão "Cadastrar Voluntário"
    2. Preencha os campos obrigatórios (*)
    3. Clique em "Cadastrar"
    
    **Campos Obrigatórios:**
    - Nome Completo
    - Email
    - Telefone
    
    **Buscar e Filtrar:**
    - Use a barra de busca para encontrar por nome, email ou telefone
    - Filtre por status e área de atuação
    - Os filtros podem ser combinados
    
    > 💡 **Dica:** Voluntários bem treinados e engajados são essenciais para o sucesso da organização!
    """)

# ============================================================================
# RODAPÉ
# ============================================================================

render_footer()