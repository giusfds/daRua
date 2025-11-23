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

# Carregar dados do banco
try:
    doadores_list = Doador.get_all()
    if doadores_list:
        df_doadores = pd.DataFrame([d.to_dict() for d in doadores_list])
        # Adicionar colunas derivadas para compatibilidade
        if 'endereco' not in df_doadores.columns:
            df_doadores['endereco'] = df_doadores.apply(
                lambda row: f"{row.get('logradouro', '')}, {row.get('numero', '')} - {row.get('bairro', '')}".strip(' ,-'), 
                axis=1
            )
        if 'data_cadastro' not in df_doadores.columns:
            df_doadores['data_cadastro'] = datetime.now().strftime('%Y-%m-%d')
        # Renomear colunas para compatibilidade
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
        st.session_state['mostrar_form'] = True

st.markdown("---")

# ============================================================================
# FILTRAR DADOS PELA BUSCA
# ============================================================================

if busca:
    try:
        # Tentar buscar pelo backend
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
        # Fallback para busca local se backend falhar
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
            
            # Processar formulário
            if submit:
                if nome:
                    try:
                        # Criar objeto Doador
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
                        
                        # Salvar no banco
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
# TABELA DE DOADORES
# ============================================================================

st.markdown("### 📋 Lista de Doadores")

if not df_filtrado.empty:
    # Preparar dados para exibição
    df_display = df_filtrado[['id', 'nome', 'email', 'telefone', 'endereco', 'data_cadastro']].copy()
    df_display.columns = ['ID', 'Nome', 'Email', 'Telefone', 'Endereço', 'Data Cadastro']
    
    # Formatar data
    try:
        df_display['Data Cadastro'] = pd.to_datetime(df_display['Data Cadastro']).dt.strftime('%d/%m/%Y')
    except:
        pass
    
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
            "Endereço": st.column_config.TextColumn("Endereço", width="large"),
            "Data Cadastro": st.column_config.TextColumn("Data Cadastro", width="small"),
        }
    )
else:
    show_info_message("Nenhum doador encontrado")

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
    - Preencha o campo obrigatório (Nome)
    - Os demais campos são opcionais mas recomendados
    - Clique em "Salvar" para confirmar o cadastro
    
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