"""
Página de Gerenciamento de Beneficiários
Lista, busca, cadastro, edição e exclusão de beneficiários
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
from models.beneficiario import Beneficiario

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

# ============================================================================
# MODAL DE CONFIRMAÇÃO DE EXCLUSÃO
# ============================================================================

if st.session_state.get('confirmar_exclusao_beneficiario'):
    beneficiario_id = st.session_state.get('beneficiario_deletar_id')
    beneficiario = Beneficiario.get_by_id(beneficiario_id)
    
    if beneficiario:
        st.markdown("---")
        st.markdown("### ⚠️ CONFIRMAÇÃO DE EXCLUSÃO")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("**👤 Beneficiário:**")
            st.markdown("**📅 Idade:**")
            st.markdown("**👥 Gênero:**")
        
        with col2:
            st.markdown(f"{beneficiario.nome}")
            st.markdown(f"{beneficiario.idade or 'Não informado'}")
            genero_map = {'M': 'Masculino', 'F': 'Feminino', 'O': 'Outro', 'N': 'Não informado'}
            st.markdown(f"{genero_map.get(beneficiario.genero, 'Não informado')}")
        
        st.markdown("")
        show_warning_message(
            "⚠️ **ATENÇÃO:** Esta ação não pode ser desfeita!\n\n"
            "Se este beneficiário tiver doações recebidas, a exclusão será bloqueada."
        )
        
        st.markdown("")
        
        col1, col2, col3 = st.columns([1, 1, 3])
        
        with col1:
            if st.button("✅ Sim, excluir", type="primary", use_container_width=True):
                try:
                    if beneficiario.delete():
                        show_success_message(f"Beneficiário **{beneficiario.nome}** excluído com sucesso!")
                        
                        st.session_state.pop('confirmar_exclusao_beneficiario', None)
                        st.session_state.pop('beneficiario_deletar_id', None)
                        
                        import time
                        time.sleep(1)
                        
                        st.rerun()
                    else:
                        show_error_message("Erro ao excluir beneficiário do banco de dados")
                
                except Exception as e:
                    erro_str = str(e).lower()
                    if "foreign key" in erro_str or "constraint" in erro_str:
                        show_error_message(
                            "❌ **Não é possível excluir este beneficiário!**\n\n"
                            "Este beneficiário possui doações recebidas no sistema. "
                            "Para excluí-lo, primeiro remova todas as doações associadas."
                        )
                    else:
                        show_error_message(f"Erro ao excluir: {str(e)}")
                    
                    st.session_state.pop('confirmar_exclusao_beneficiario', None)
                    st.session_state.pop('beneficiario_deletar_id', None)
        
        with col2:
            if st.button("❌ Cancelar", use_container_width=True):
                st.session_state.pop('confirmar_exclusao_beneficiario', None)
                st.session_state.pop('beneficiario_deletar_id', None)
                st.rerun()
        
        st.markdown("---")

# ============================================================================
# CARREGAR DADOS DO BANCO
# ============================================================================

try:
    beneficiarios_list = Beneficiario.get_all()
    if beneficiarios_list:
        df_beneficiarios = pd.DataFrame([b.to_dict() for b in beneficiarios_list])
        if 'id' not in df_beneficiarios.columns and 'idBeneficiario' in df_beneficiarios.columns:
            df_beneficiarios['id'] = df_beneficiarios['idBeneficiario']
        if 'necessidades' not in df_beneficiarios.columns:
            df_beneficiarios['necessidades'] = 'Não especificado'
        if 'status' not in df_beneficiarios.columns:
            df_beneficiarios['status'] = 'Ativo'
    else:
        df_beneficiarios = pd.DataFrame(columns=['id', 'nome', 'idade', 'genero', 'descricao', 'necessidades', 'status'])
except Exception as e:
    show_error_message(f"Erro ao carregar beneficiários: {str(e)}")
    df_beneficiarios = pd.DataFrame(columns=['id', 'nome', 'idade', 'genero', 'descricao', 'necessidades', 'status'])

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
        st.session_state.pop('editar_beneficiario_id', None)
        st.session_state['mostrar_form_benef'] = True
        st.rerun()

st.markdown("---")

# ============================================================================
# FILTRAR DADOS
# ============================================================================

df_filtrado = df_beneficiarios.copy()

# Filtrar por busca
if busca:
    try:
        if not df_beneficiarios.empty:
            df_filtrado = df_filtrado[
                df_filtrado['nome'].str.contains(busca, case=False, na=False)
            ]
    except Exception as e:
        show_info_message("Erro ao filtrar dados")
        df_filtrado = df_beneficiarios

# Filtrar por status
if filtro_status != "Todos":
    try:
        if not df_filtrado.empty and 'status' in df_filtrado.columns:
            df_filtrado = df_filtrado[df_filtrado['status'] == filtro_status]
    except Exception as e:
        pass

# ============================================================================
# FORMULÁRIO DE EDIÇÃO
# ============================================================================

if st.session_state.get('editar_beneficiario_id'):
    beneficiario_id = st.session_state.get('editar_beneficiario_id')
    beneficiario = Beneficiario.get_by_id(beneficiario_id)
    
    if beneficiario:
        with st.expander(f"✏️ Editando: {beneficiario.nome}", expanded=True):
            with st.form("form_editar_beneficiario"):
                st.markdown("### Dados do Beneficiário")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    nome = st.text_input(
                        "Nome Completo *", 
                        value=beneficiario.nome or "",
                        placeholder="Ex: Maria das Graças"
                    )
                    
                    # Calcular idade aproximada se tiver
                    idade_valor = beneficiario.idade or 30
                    data_nascimento = st.date_input(
                        "Data de Nascimento",
                        value=datetime(datetime.now().year - idade_valor, 1, 1),
                        min_value=datetime(1930, 1, 1),
                        max_value=datetime.now()
                    )
                    
                    # Mapear gênero
                    genero_map = {'M': 'Masculino', 'F': 'Feminino', 'O': 'Outro', 'N': 'Prefiro não informar'}
                    genero_reverso = {v: k for k, v in genero_map.items()}
                    genero_atual = genero_map.get(beneficiario.genero, 'Prefiro não informar')
                    
                    genero = st.selectbox(
                        "Gênero",
                        ["Masculino", "Feminino", "Outro", "Prefiro não informar"],
                        index=["Masculino", "Feminino", "Outro", "Prefiro não informar"].index(genero_atual)
                    )
                
                with col2:
                    descricao = st.text_area(
                        "Descrição da Situação",
                        value=beneficiario.descricao or "",
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
                    submit = st.form_submit_button("💾 Salvar Alterações", use_container_width=True)
                
                with col_btn2:
                    cancelar = st.form_submit_button("❌ Cancelar", use_container_width=True)
                
                # Processar formulário de edição
                if submit:
                    if nome:
                        try:
                            # Calcular idade
                            idade = (datetime.now() - datetime.combine(data_nascimento, datetime.min.time())).days // 365
                            
                            # Converter gênero
                            genero_bd = genero_reverso.get(genero, "N")
                            
                            # Criar descrição com necessidades
                            desc_completa = descricao
                            if necessidades:
                                desc_completa += f" | Necessidades: {', '.join(necessidades)}"
                            
                            # Atualizar objeto
                            beneficiario.nome = nome
                            beneficiario.idade = idade
                            beneficiario.genero = genero_bd
                            beneficiario.descricao = desc_completa if desc_completa else None
                            
                            # Atualizar no banco
                            if beneficiario.update():
                                show_success_message(f"Beneficiário **{nome}** atualizado com sucesso!")
                                st.balloons()
                                
                                st.session_state.pop('editar_beneficiario_id', None)
                                
                                import time
                                time.sleep(1)
                                
                                st.rerun()
                            else:
                                show_error_message("Erro ao atualizar beneficiário no banco de dados")
                        except Exception as e:
                            show_error_message(f"Erro ao atualizar beneficiário: {str(e)}")
                    else:
                        show_error_message("Por favor, preencha o campo Nome Completo")
                
                if cancelar:
                    st.session_state.pop('editar_beneficiario_id', None)
                    st.rerun()
    else:
        show_error_message("Beneficiário não encontrado!")
        st.session_state.pop('editar_beneficiario_id', None)

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
                    try:
                        # Calcular idade
                        idade = (datetime.now() - datetime.combine(data_nascimento, datetime.min.time())).days // 365
                        
                        # Converter gênero
                        genero_map = {
                            "Masculino": "M",
                            "Feminino": "F",
                            "Outro": "O",
                            "Prefiro não informar": "N"
                        }
                        genero_bd = genero_map.get(genero, "N")
                        
                        # Criar descrição com necessidades
                        desc_completa = descricao
                        if necessidades:
                            desc_completa += f" | Necessidades: {', '.join(necessidades)}"
                        
                        # Criar objeto Beneficiario
                        beneficiario = Beneficiario(
                            nome=nome,
                            idade=idade,
                            genero=genero_bd,
                            descricao=desc_completa if desc_completa else None
                        )
                        
                        # Salvar no banco
                        if beneficiario.save():
                            show_success_message(f"Beneficiário **{nome}** cadastrado com sucesso!")
                            st.balloons()
                            st.session_state['mostrar_form_benef'] = False
                            st.rerun()
                        else:
                            show_error_message("Erro ao salvar beneficiário no banco de dados")
                    except Exception as e:
                        show_error_message(f"Erro ao cadastrar beneficiário: {str(e)}")
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
    try:
        total = len(df_beneficiarios) if not df_beneficiarios.empty else 0
        st.metric("Total de Beneficiários", total)
    except:
        st.metric("Total de Beneficiários", 0)

with col2:
    try:
        if not df_beneficiarios.empty and 'status' in df_beneficiarios.columns:
            ativos = len(df_beneficiarios[df_beneficiarios['status'] == 'Ativo'])
        else:
            ativos = 0
        st.metric("Beneficiários Ativos", ativos)
    except:
        st.metric("Beneficiários Ativos", 0)

with col3:
    try:
        if not df_beneficiarios.empty and 'status' in df_beneficiarios.columns:
            aguardando = len(df_beneficiarios[df_beneficiarios['status'] == 'Aguardando'])
        else:
            aguardando = 0
        st.metric("Aguardando Atendimento", aguardando)
    except:
        st.metric("Aguardando Atendimento", 0)

with col4:
    if busca or filtro_status != "Todos":
        st.metric("Resultados", len(df_filtrado))
    else:
        st.metric("Cadastros este Mês", "-")

st.markdown("---")

# ============================================================================
# TABELA DE BENEFICIÁRIOS COM BOTÕES
# ============================================================================

st.markdown("### 📋 Lista de Beneficiários")

if not df_filtrado.empty:
    for index, row in df_filtrado.iterrows():
        with st.container():
            col_dados, col_acoes = st.columns([5, 1])
            
            with col_dados:
                col1, col2, col3, col4 = st.columns([1, 2, 1, 2])
                
                with col1:
                    st.markdown(f"**ID:** {row['id']}")
                
                with col2:
                    st.markdown(f"**Nome:** {row['nome']}")
                
                with col3:
                    st.markdown(f"**Idade:** {row.get('idade', 'N/A')}")
                
                with col4:
                    genero_map = {'M': 'Masculino', 'F': 'Feminino', 'O': 'Outro', 'N': 'N/A'}
                    st.markdown(f"**Gênero:** {genero_map.get(row.get('genero'), 'N/A')}")
            
            with col_acoes:
                col_edit, col_del = st.columns(2)
                
                with col_edit:
                    if st.button(
                        "✏️",
                        key=f"edit_benef_{row['id']}",
                        help="Editar beneficiário",
                        use_container_width=True
                    ):
                        st.session_state['editar_beneficiario_id'] = row['id']
                        st.session_state.pop('mostrar_form_benef', None)
                        st.rerun()
                
                with col_del:
                    if st.button(
                        "🗑️",
                        key=f"del_benef_{row['id']}",
                        help="Excluir beneficiário",
                        use_container_width=True
                    ):
                        st.session_state['beneficiario_deletar_id'] = row['id']
                        st.session_state['confirmar_exclusao_beneficiario'] = True
                        st.rerun()
            
            st.markdown("---")
    
    if busca or filtro_status != "Todos":
        show_info_message(f"Mostrando {len(df_filtrado)} de {len(df_beneficiarios)} beneficiários")
    else:
        show_info_message(f"Total de {len(df_beneficiarios)} beneficiários cadastrados")

else:
    show_info_message("Nenhum beneficiário encontrado")

st.markdown("---")

# ============================================================================
# GRÁFICOS E ANÁLISES
# ============================================================================

st.markdown("### 📊 Análises")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Distribuição por Status")
    if not df_beneficiarios.empty and 'status' in df_beneficiarios.columns:
        import plotly.express as px
        status_counts = df_beneficiarios['status'].value_counts()
        fig_status = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="",
            color_discrete_sequence=['#8B5CF6', '#3B82F6', '#10B981']
        )
        fig_status.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_status, use_container_width=True)
    else:
        st.info("Sem dados para exibir")

with col2:
    st.markdown("#### Faixa Etária")
    if not df_beneficiarios.empty and 'idade' in df_beneficiarios.columns:
        import plotly.express as px
        bins = [0, 18, 30, 50, 65, 100]
        labels = ['0-17', '18-29', '30-49', '50-64', '65+']
        df_beneficiarios['faixa_etaria'] = pd.cut(df_beneficiarios['idade'], bins=bins, labels=labels, right=False)
        faixa_counts = df_beneficiarios['faixa_etaria'].value_counts().sort_index()
        fig_faixa = px.pie(
            values=faixa_counts.values,
            names=faixa_counts.index,
            title="",
            color_discrete_sequence=['#8B5CF6', '#7C3AED', '#3B82F6', '#10B981', '#F59E0B']
        )
        fig_faixa.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_faixa, use_container_width=True)
    else:
        st.info("Sem dados para exibir")

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
    
    **Editar Beneficiário:**
    - Clique no botão ✏️ ao lado do beneficiário que deseja editar
    - Altere os dados desejados
    - Clique em "Salvar Alterações"
    
    **Excluir Beneficiário:**
    - Clique no botão 🗑️ ao lado do beneficiário
    - Confirme a exclusão
    - ⚠️ Beneficiários com doações recebidas não podem ser excluídos
    
    **Status dos Beneficiários:**
    - **Ativo:** Beneficiário em atendimento regular
    - **Inativo:** Beneficiário que não está mais sendo atendido
    - **Aguardando:** Beneficiário cadastrado aguardando início do atendimento
    
    > 💡 **Dica:** Mantenha as informações atualizadas para melhor direcionar as doações e campanhas.
    """)

# ============================================================================
# RODAPÉ
# ============================================================================

render_footer()