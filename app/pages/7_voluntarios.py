"""
Página de Gerenciamento de Voluntários
Lista, busca, cadastro, edição e exclusão de voluntários
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
    show_info_message,
    show_warning_message
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

# ============================================================================
# MODAL DE CONFIRMAÇÃO DE EXCLUSÃO
# ============================================================================

if st.session_state.get('confirmar_exclusao_voluntario'):
    voluntario_id = st.session_state.get('voluntario_deletar_id')
    voluntario = Voluntario.get_by_id(voluntario_id)
    
    if voluntario:
        st.markdown("---")
        st.markdown("### ⚠️ CONFIRMAÇÃO DE EXCLUSÃO")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("**👤 Voluntário:**")
            st.markdown("**📧 Email:**")
            st.markdown("**📞 Telefone:**")
        
        with col2:
            st.markdown(f"{voluntario.nome}")
            st.markdown(f"{voluntario.email or 'Não informado'}")
            st.markdown(f"{voluntario.telefone or 'Não informado'}")
        
        st.markdown("")
        show_warning_message(
            "⚠️ **ATENÇÃO:** Esta ação não pode ser desfeita!\n\n"
            "Se este voluntário estiver associado a doações, a exclusão será bloqueada."
        )
        
        st.markdown("")
        
        col1, col2, col3 = st.columns([1, 1, 3])
        
        with col1:
            if st.button("✅ Sim, excluir", type="primary", use_container_width=True):
                try:
                    if voluntario.delete():
                        show_success_message(f"Voluntário **{voluntario.nome}** excluído com sucesso!")
                        
                        st.session_state.pop('confirmar_exclusao_voluntario', None)
                        st.session_state.pop('voluntario_deletar_id', None)
                        
                        import time
                        time.sleep(1)
                        
                        st.rerun()
                    else:
                        show_error_message("Erro ao excluir voluntário do banco de dados")
                
                except Exception as e:
                    erro_str = str(e).lower()
                    if "foreign key" in erro_str or "constraint" in erro_str:
                        show_error_message(
                            "❌ **Não é possível excluir este voluntário!**\n\n"
                            "Este voluntário está associado a doações. "
                            "Para excluí-lo, primeiro remova as associações."
                        )
                    else:
                        show_error_message(f"Erro ao excluir: {str(e)}")
                    
                    st.session_state.pop('confirmar_exclusao_voluntario', None)
                    st.session_state.pop('voluntario_deletar_id', None)
        
        with col2:
            if st.button("❌ Cancelar", use_container_width=True):
                st.session_state.pop('confirmar_exclusao_voluntario', None)
                st.session_state.pop('voluntario_deletar_id', None)
                st.rerun()
        
        st.markdown("---")

# ============================================================================
# CARREGAR DADOS DO BANCO
# ============================================================================

try:
    voluntarios_list = Voluntario.get_all()
    if voluntarios_list:
        df_voluntarios = pd.DataFrame([v.to_dict() for v in voluntarios_list])
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
        st.session_state.pop('editar_voluntario_id', None)
        st.session_state['mostrar_form_voluntario'] = True
        st.rerun()

st.markdown("---")

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
# FORMULÁRIO DE EDIÇÃO
# ============================================================================

if st.session_state.get('editar_voluntario_id'):
    voluntario_id = st.session_state.get('editar_voluntario_id')
    voluntario = Voluntario.get_by_id(voluntario_id)
    
    if voluntario:
        with st.expander(f"✏️ Editando: {voluntario.nome}", expanded=True):
            with st.form("form_editar_voluntario"):
                st.markdown("### Dados Pessoais")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    nome = st.text_input(
                        "Nome Completo *", 
                        value=voluntario.nome or "",
                        placeholder="Ex: Alexandre Pereira"
                    )
                    email = st.text_input(
                        "Email *", 
                        value=voluntario.email or "",
                        placeholder="exemplo@email.com"
                    )
                
                with col2:
                    telefone = st.text_input(
                        "Telefone *", 
                        value=voluntario.telefone or "",
                        placeholder="(11) 98765-4321"
                    )
                
                st.markdown("---")
                
                col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 4])
                
                with col_btn1:
                    submit = st.form_submit_button("✅ Salvar Alterações", use_container_width=True)
                
                with col_btn2:
                    cancelar = st.form_submit_button("❌ Cancelar", use_container_width=True)
                
                # Processar formulário de edição
                if submit:
                    if nome and email and telefone:
                        try:
                            # Atualizar objeto
                            voluntario.nome = nome
                            voluntario.email = email
                            voluntario.telefone = telefone
                            
                            # Atualizar no banco
                            if voluntario.update():
                                show_success_message(f"Voluntário **{nome}** atualizado com sucesso!")
                                st.balloons()
                                
                                st.session_state.pop('editar_voluntario_id', None)
                                
                                import time
                                time.sleep(1)
                                
                                st.rerun()
                            else:
                                show_error_message("Erro ao atualizar voluntário no banco de dados")
                        except Exception as e:
                            show_error_message(f"Erro ao atualizar voluntário: {str(e)}")
                    else:
                        show_error_message("Por favor, preencha todos os campos obrigatórios (*)")
                
                if cancelar:
                    st.session_state.pop('editar_voluntario_id', None)
                    st.rerun()
    else:
        show_error_message("Voluntário não encontrado!")
        st.session_state.pop('editar_voluntario_id', None)

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
# TABELA DE VOLUNTÁRIOS COM BOTÕES
# ============================================================================

st.markdown("### 📋 Lista de Voluntários")

if not df_filtrado.empty:
    for index, row in df_filtrado.iterrows():
        with st.container():
            col_dados, col_acoes = st.columns([5, 1])
            
            with col_dados:
                col1, col2, col3, col4 = st.columns([1, 2, 2, 2])
                
                with col1:
                    st.markdown(f"**ID:** {row['id']}")
                
                with col2:
                    st.markdown(f"**Nome:** {row['nome']}")
                
                with col3:
                    st.markdown(f"**Email:** {row.get('email', 'Não informado')}")
                
                with col4:
                    st.markdown(f"**Telefone:** {row.get('telefone', 'Não informado')}")
            
            with col_acoes:
                col_edit, col_del = st.columns(2)
                
                with col_edit:
                    if st.button(
                        "✏️",
                        key=f"edit_vol_{row['id']}",
                        help="Editar voluntário",
                        use_container_width=True
                    ):
                        st.session_state['editar_voluntario_id'] = row['id']
                        st.session_state.pop('mostrar_form_voluntario', None)
                        st.rerun()
                
                with col_del:
                    if st.button(
                        "🗑️",
                        key=f"del_vol_{row['id']}",
                        help="Excluir voluntário",
                        use_container_width=True
                    ):
                        st.session_state['voluntario_deletar_id'] = row['id']
                        st.session_state['confirmar_exclusao_voluntario'] = True
                        st.rerun()
            
            st.markdown("---")
    
    if busca or filtro_status != "Todos" or filtro_area != "Todas":
        show_info_message(f"Mostrando {len(df_filtrado)} de {len(df_voluntarios)} voluntários")
    else:
        show_info_message(f"Total de {len(df_voluntarios)} voluntários cadastrados")

else:
    show_info_message("Nenhum voluntário encontrado")

st.markdown("---")

# ============================================================================
# INFORMAÇÕES ADICIONAIS
# ============================================================================

with st.expander("ℹ️ Informações sobre Gerenciamento de Voluntários"):
    st.markdown("""
    ### Como usar esta página:
    
    **Cadastrar Novo Voluntário:**
    - Clique no botão "Cadastrar Voluntário"
    - Preencha os campos obrigatórios (*)
    - Clique em "Cadastrar"
    
    **Editar Voluntário:**
    - Clique no botão ✏️ ao lado do voluntário
    - Altere os dados necessários
    - Clique em "Salvar Alterações"
    
    **Excluir Voluntário:**
    - Clique no botão 🗑️ ao lado do voluntário
    - Confirme a exclusão
    - ⚠️ Voluntários associados a doações não podem ser excluídos
    
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