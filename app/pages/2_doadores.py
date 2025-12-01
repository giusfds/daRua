"""
Página de Gerenciamento de Doadores
Lista, busca, cadastro, edição e exclusão de doadores
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
from models.doador import Doador

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

# ============================================================================
# MODAL DE CONFIRMAÇÃO DE EXCLUSÃO
# ============================================================================

if st.session_state.get('confirmar_exclusao_doador'):
    doador_id = st.session_state.get('doador_deletar_id')
    doador = Doador.get_by_id(doador_id)
    
    if doador:
        st.markdown("---")
        st.markdown("### ⚠️ CONFIRMAÇÃO DE EXCLUSÃO")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("**👤 Doador:**")
            st.markdown("**📧 Email:**")
            st.markdown("**📞 Telefone:**")
        
        with col2:
            st.markdown(f"{doador.nome}")
            st.markdown(f"{doador.email or 'Não informado'}")
            st.markdown(f"{doador.telefone or 'Não informado'}")
        
        st.markdown("")
        show_warning_message(
            "⚠️ **ATENÇÃO:** Esta ação não pode ser desfeita!\n\n"
            "Se este doador tiver doações registradas, a exclusão será bloqueada."
        )
        
        st.markdown("")
        
        col1, col2, col3 = st.columns([1, 1, 3])
        
        with col1:
            if st.button("✅ Sim, excluir", type="primary", use_container_width=True):
                try:
                    if doador.delete():
                        show_success_message(f"Doador **{doador.nome}** excluído com sucesso!")
                        
                        st.session_state.pop('confirmar_exclusao_doador', None)
                        st.session_state.pop('doador_deletar_id', None)
                        
                        import time
                        time.sleep(1)
                        
                        st.rerun()
                    else:
                        show_error_message("Erro ao excluir doador do banco de dados")
                
                except Exception as e:
                    erro_str = str(e).lower()
                    if "foreign key" in erro_str or "constraint" in erro_str:
                        show_error_message(
                            "❌ **Não é possível excluir este doador!**\n\n"
                            "Este doador possui doações registradas no sistema. "
                            "Para excluí-lo, primeiro remova todas as doações associadas."
                        )
                    else:
                        show_error_message(f"Erro ao excluir: {str(e)}")
                    
                    st.session_state.pop('confirmar_exclusao_doador', None)
                    st.session_state.pop('doador_deletar_id', None)
        
        with col2:
            if st.button("❌ Cancelar", use_container_width=True):
                st.session_state.pop('confirmar_exclusao_doador', None)
                st.session_state.pop('doador_deletar_id', None)
                st.rerun()
        
        st.markdown("---")

# ============================================================================
# CARREGAR DADOS DO BANCO
# ============================================================================

try:
    doadores_list = Doador.get_all()
    if doadores_list:
        df_doadores = pd.DataFrame([d.to_dict() for d in doadores_list])
        if 'endereco' not in df_doadores.columns:
            df_doadores['endereco'] = df_doadores.apply(
                lambda row: f"{row.get('logradouro', '')}, {row.get('numero', '')} - {row.get('bairro', '')}".strip(' ,-'), 
                axis=1
            )
        if 'data_cadastro' not in df_doadores.columns:
            df_doadores['data_cadastro'] = datetime.now().strftime('%Y-%m-%d')
        if 'idDoador' in df_doadores.columns:
            df_doadores['id'] = df_doadores['idDoador']
    else:
        df_doadores = pd.DataFrame(columns=['id', 'nome', 'email', 'telefone', 'endereco', 'data_cadastro'])
except Exception as e:
    show_error_message(f"Erro ao carregar doadores: {str(e)}")
    df_doadores = pd.DataFrame(columns=['id', 'nome', 'email', 'telefone', 'endereco', 'data_cadastro'])

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
        # NOVO - EDITAR: Desativar modo editar ao clicar em cadastrar
        st.session_state.pop('editar_doador_id', None)
        st.session_state['mostrar_form'] = True
        st.rerun()

st.markdown("---")

# ============================================================================
# FILTRAR DADOS PELA BUSCA
# ============================================================================

if busca:
    try:
        doadores_list = Doador.search_by_name(busca)
        if doadores_list:
            df_filtrado = pd.DataFrame([d.to_dict() for d in doadores_list])
            if 'endereco' not in df_filtrado.columns:
                df_filtrado['endereco'] = df_filtrado.apply(
                    lambda row: f"{row.get('logradouro', '')}, {row.get('numero', '')} - {row.get('bairro', '')}".strip(' ,-'), 
                    axis=1
                )
            if 'data_cadastro' not in df_filtrado.columns:
                df_filtrado['data_cadastro'] = datetime.now().strftime('%Y-%m-%d')
            if 'idDoador' in df_filtrado.columns:
                df_filtrado['id'] = df_filtrado['idDoador']
        else:
            df_filtrado = pd.DataFrame(columns=['id', 'nome', 'email', 'telefone', 'endereco', 'data_cadastro'])
    except Exception as e:
        show_info_message(f"Usando busca local (backend indisponível)")
        if not df_doadores.empty:
            mask = (
                df_doadores['nome'].str.contains(busca, case=False, na=False) |
                df_doadores['email'].str.contains(busca, case=False, na=False) |
                df_doadores['telefone'].str.contains(busca, case=False, na=False)
            )
            df_filtrado = df_doadores[mask]
        else:
            df_filtrado = df_doadores
else:
    df_filtrado = df_doadores

# ============================================================================
# NOVO - EDITAR: FORMULÁRIO DE EDIÇÃO
# ============================================================================

if st.session_state.get('editar_doador_id'):
    doador_id = st.session_state.get('editar_doador_id')
    doador = Doador.get_by_id(doador_id)
    
    if doador:
        with st.expander(f"✏️ Editando: {doador.nome}", expanded=True):
            with st.form("form_editar_doador"):
                st.markdown("### Dados do Doador")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    nome = st.text_input(
                        "Nome Completo *", 
                        value=doador.nome or "",
                        placeholder="Ex: João da Silva"
                    )
                    email = st.text_input(
                        "Email", 
                        value=doador.email or "",
                        placeholder="exemplo@email.com"
                    )
                    telefone = st.text_input(
                        "Telefone", 
                        value=doador.telefone or "",
                        placeholder="(11) 98765-4321"
                    )
                
                with col2:
                    logradouro = st.text_input(
                        "Rua", 
                        value=doador.logradouro or "",
                        placeholder="Rua das Flores"
                    )
                    numero = st.text_input(
                        "Número", 
                        value=doador.numero or "",
                        placeholder="123"
                    )
                    bairro = st.text_input(
                        "Bairro", 
                        value=doador.bairro or "",
                        placeholder="Centro"
                    )
                
                col3, col4 = st.columns(2)
                with col3:
                    cidade = st.text_input(
                        "Cidade", 
                        value=doador.cidade or "",
                        placeholder="Belo Horizonte"
                    )
                    estado = st.text_input(
                        "Estado (UF)", 
                        value=doador.estado or "",
                        placeholder="MG", 
                        max_chars=2
                    )
                with col4:
                    cep = st.text_input(
                        "CEP", 
                        value=doador.cep or "",
                        placeholder="00000-000"
                    )
                
                st.markdown("---")
                
                col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 4])
                
                with col_btn1:
                    submit = st.form_submit_button("💾 Salvar Alterações", use_container_width=True)
                
                with col_btn2:
                    cancelar = st.form_submit_button("❌ Cancelar", use_container_width=True)
                
                # Processar formulário de edição
                if submit:
                    if nome:
                        try:
                            # Atualizar objeto Doador
                            doador.nome = nome
                            doador.telefone = telefone if telefone else None
                            doador.email = email if email else None
                            doador.logradouro = logradouro if logradouro else None
                            doador.numero = numero if numero else None
                            doador.bairro = bairro if bairro else None
                            doador.cidade = cidade if cidade else None
                            doador.estado = estado.upper() if estado else None
                            doador.cep = cep if cep else None
                            
                            # Atualizar no banco
                            if doador.update():
                                show_success_message(f"Doador **{nome}** atualizado com sucesso!")
                                st.balloons()
                                
                                # Limpar estado
                                st.session_state.pop('editar_doador_id', None)
                                
                                import time
                                time.sleep(1)
                                
                                st.rerun()
                            else:
                                show_error_message("Erro ao atualizar doador no banco de dados")
                        except Exception as e:
                            show_error_message(f"Erro ao atualizar doador: {str(e)}")
                    else:
                        show_error_message("Por favor, preencha o campo Nome (obrigatório)")
                
                if cancelar:
                    st.session_state.pop('editar_doador_id', None)
                    st.rerun()
    else:
        show_error_message("Doador não encontrado!")
        st.session_state.pop('editar_doador_id', None)

# ============================================================================
# FORMULÁRIO DE CADASTRO (NOVO DOADOR)
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
                email = st.text_input("Email", placeholder="exemplo@email.com")
                telefone = st.text_input("Telefone", placeholder="(11) 98765-4321")
            
            with col2:
                logradouro = st.text_input("Rua", placeholder="Rua das Flores")
                numero = st.text_input("Número", placeholder="123")
                bairro = st.text_input("Bairro", placeholder="Centro")
            
            col3, col4 = st.columns(2)
            with col3:
                cidade = st.text_input("Cidade", placeholder="Belo Horizonte")
                estado = st.text_input("Estado (UF)", placeholder="MG", max_chars=2)
            with col4:
                cep = st.text_input("CEP", placeholder="00000-000")
            
            st.markdown("---")
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 4])
            
            with col_btn1:
                submit = st.form_submit_button("💾 Salvar", use_container_width=True)
            
            with col_btn2:
                cancelar = st.form_submit_button("❌ Cancelar", use_container_width=True)
            
            # Processar formulário de cadastro
            if submit:
                if nome:
                    try:
                        doador = Doador(
                            nome=nome,
                            telefone=telefone if telefone else None,
                            email=email if email else None,
                            logradouro=logradouro if logradouro else None,
                            numero=numero if numero else None,
                            bairro=bairro if bairro else None,
                            cidade=cidade if cidade else None,
                            estado=estado.upper() if estado else None,
                            cep=cep if cep else None
                        )
                        
                        if doador.save():
                            show_success_message(f"Doador **{nome}** cadastrado com sucesso!")
                            st.balloons()
                            st.session_state['mostrar_form'] = False
                            st.rerun()
                        else:
                            show_error_message("Erro ao salvar doador no banco de dados")
                    except Exception as e:
                        show_error_message(f"Erro ao cadastrar doador: {str(e)}")
                else:
                    show_error_message("Por favor, preencha o campo Nome (obrigatório)")
            
            if cancelar:
                st.session_state['mostrar_form'] = False
                st.rerun()

# ============================================================================
# ESTATÍSTICAS RÁPIDAS
# ============================================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    try:
        total = len(df_doadores) if not df_doadores.empty else 0
        st.metric("Total de Doadores", total)
    except:
        st.metric("Total de Doadores", 0)

with col2:
    st.metric("Cadastros este Mês", "-")

with col3:
    try:
        ativos = len(df_doadores) if not df_doadores.empty else 0
        st.metric("Doadores Ativos", ativos)
    except:
        st.metric("Doadores Ativos", 0)

with col4:
    if busca:
        st.metric("Resultados da Busca", len(df_filtrado))
    else:
        st.metric("Média de Doações/Doador", "-")

st.markdown("---")

# ============================================================================
# TABELA DE DOADORES COM BOTÕES DE AÇÃO
# ============================================================================

st.markdown("### 📋 Lista de Doadores")

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
                    # NOVO - EDITAR: Botão agora funciona!
                    if st.button(
                        "✏️",
                        key=f"edit_{row['id']}",
                        help="Editar doador",
                        use_container_width=True
                    ):
                        # Ativar modo editar
                        st.session_state['editar_doador_id'] = row['id']
                        # Desativar modo cadastrar
                        st.session_state.pop('mostrar_form', None)
                        st.rerun()
                
                with col_del:
                    if st.button(
                        "🗑️",
                        key=f"del_{row['id']}",
                        help="Excluir doador",
                        use_container_width=True
                    ):
                        st.session_state['doador_deletar_id'] = row['id']
                        st.session_state['confirmar_exclusao_doador'] = True
                        st.rerun()
            
            st.markdown("---")
    
    if busca:
        show_info_message(f"Mostrando {len(df_filtrado)} de {len(df_doadores)} doadores")
    else:
        show_info_message(f"Total de {len(df_doadores)} doadores cadastrados")

else:
    show_info_message("Nenhum doador encontrado")
    
    if busca:
        show_info_message(f"Nenhum resultado encontrado para '{busca}'")

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
    - Preencha o campo obrigatório (Nome)
    - Os demais campos são opcionais mas recomendados
    - Clique em "Salvar" para confirmar o cadastro
    
    **Editar Doador:**
    - Clique no botão ✏️ ao lado do doador que deseja editar
    - Altere os dados desejados no formulário
    - Clique em "Salvar Alterações" para confirmar
    
    **Excluir Doador:**
    - Clique no botão 🗑️ ao lado do doador que deseja excluir
    - Confirme a exclusão na tela de confirmação
    - ⚠️ **Atenção:** Doadores com doações registradas não podem ser excluídos
    
    **Campos Obrigatórios:**
    - Nome Completo (*)
    
    **Campos Opcionais:**
    - Email, Telefone, Endereço completo
    
    > 💡 **Dica:** Mantenha os dados dos doadores sempre atualizados para facilitar o contato e a gestão das doações.
    """)

# ============================================================================
# RODAPÉ
# ============================================================================

render_footer()