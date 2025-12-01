"""
Página de Gestão de Campanhas - Sistema Somos DaRua
Permite criar, visualizar, editar e excluir campanhas de doação
Inclui gestão de metas e acompanhamento de progresso
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

# Adicionar diretórios ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.models.campanha_doacao import CampanhaDoacao
from app.utils.config import (
    setup_page,
    apply_global_css,
    render_sidebar,
    render_footer,
    show_success_message,
    show_error_message,
    show_info_message,
    show_warning_message
)

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================

setup_page(
    page_title="Campanhas - Somos DaRua",
    page_icon="📢"
)

apply_global_css()
render_sidebar()

# ============================================================================
# TÍTULO DA PÁGINA
# ============================================================================

st.markdown("# 📢 Gestão de Campanhas")
st.markdown("Organize e acompanhe campanhas de doação com metas e progresso")
st.markdown("---")

# ============================================================================
# MODAL DE CONFIRMAÇÃO DE EXCLUSÃO
# ============================================================================

if st.session_state.get('confirmar_exclusao_campanha'):
    campanha_id = st.session_state.get('campanha_deletar_id')
    
    if campanha_id:
        campanha = CampanhaDoacao.get_by_id(campanha_id)
        
        if campanha:
            st.markdown("### ⚠️ CONFIRMAR EXCLUSÃO")
            
            with st.container():
                st.warning(f"""
                **Tem certeza que deseja excluir esta campanha?**
                
                **Nome:** {campanha.nome}
                **Período:** {campanha.data_inicio} a {campanha.data_termino}
                **Meta:** {campanha.meta:,.2f} {campanha.tipo_meta}
                **Arrecadado:** {campanha.arrecadado:,.2f} {campanha.tipo_meta}
                
                ⚠️ **Esta ação não pode ser desfeita!**
                """)
                
                col1, col2, col3 = st.columns([1, 1, 4])
                
                with col1:
                    if st.button("✅ Sim, excluir", use_container_width=True, type="primary"):
                        try:
                            if campanha.delete():
                                show_success_message(f"Campanha **{campanha.nome}** excluída com sucesso!")
                                
                                st.session_state.pop('confirmar_exclusao_campanha', None)
                                st.session_state.pop('campanha_deletar_id', None)
                                
                                import time
                                time.sleep(1)
                                
                                st.rerun()
                            else:
                                show_error_message("Erro ao excluir campanha")
                        except Exception as e:
                            erro_str = str(e).lower()
                            if "foreign key" in erro_str or "constraint" in erro_str:
                                show_error_message(
                                    "❌ **Não é possível excluir esta campanha!**\n\n"
                                    "Existem doações ou necessidades vinculadas a ela.\n"
                                    "Remova esses vínculos antes de excluir a campanha."
                                )
                            else:
                                show_error_message(f"Erro ao excluir: {str(e)}")
                        
                        st.session_state.pop('confirmar_exclusao_campanha', None)
                        st.session_state.pop('campanha_deletar_id', None)
                
                with col2:
                    if st.button("❌ Cancelar", use_container_width=True):
                        st.session_state.pop('confirmar_exclusao_campanha', None)
                        st.session_state.pop('campanha_deletar_id', None)
                        st.rerun()
            
            st.markdown("---")

# ============================================================================
# CARREGAR DADOS DO BANCO
# ============================================================================

try:
    campanhas_list = CampanhaDoacao.get_all()
    if campanhas_list:
        campanhas = []
        for c in campanhas_list:
            camp_dict = c.to_dict()
            camp_dict['id'] = c.idCampanhaDoacao
            camp_dict['status'] = 'Ativa' if c.data_termino is None or c.data_termino >= datetime.now().date() else 'Concluída'
            camp_dict['responsavel'] = 'Administrador'
            campanhas.append(camp_dict)
    else:
        campanhas = []
except Exception as e:
    show_error_message(f"Erro ao carregar campanhas: {str(e)}")
    campanhas = []

# ============================================================================
# FILTROS E BUSCA
# ============================================================================

col_busca, col_filtro, col_ordenacao, col_btn = st.columns([3, 2, 2, 2])

with col_busca:
    busca = st.text_input(
        "🔍 Buscar campanha",
        placeholder="Digite o nome...",
        label_visibility="collapsed"
    )

with col_filtro:
    filtro_status = st.selectbox(
        "Status",
        ["Todas", "Ativa", "Concluída"],
        label_visibility="collapsed"
    )

with col_ordenacao:
    ordenacao = st.selectbox(
        "Ordenar por",
        ["Mais Recentes", "Mais Antigas", "Nome A-Z", "Nome Z-A", "Maior Progresso"],
        label_visibility="collapsed"
    )

with col_btn:
    st.write("")  # Espaçamento
    if st.button("➕ Nova Campanha", use_container_width=True, type="primary"):
        st.session_state['mostrar_form_campanha'] = True
        st.session_state.pop('editar_campanha_id', None)
        st.rerun()

# Aplicar filtros
campanhas_filtradas = campanhas.copy()

if busca:
    campanhas_filtradas = [
        c for c in campanhas_filtradas 
        if busca.lower() in c['nome'].lower()
    ]

if filtro_status != "Todas":
    campanhas_filtradas = [
        c for c in campanhas_filtradas 
        if c['status'] == filtro_status
    ]

# Aplicar ordenação
if ordenacao == "Mais Recentes":
    campanhas_filtradas.sort(key=lambda x: x.get('data_inicio', ''), reverse=True)
elif ordenacao == "Mais Antigas":
    campanhas_filtradas.sort(key=lambda x: x.get('data_inicio', ''))
elif ordenacao == "Nome A-Z":
    campanhas_filtradas.sort(key=lambda x: x['nome'])
elif ordenacao == "Nome Z-A":
    campanhas_filtradas.sort(key=lambda x: x['nome'], reverse=True)
elif ordenacao == "Maior Progresso":
    campanhas_filtradas.sort(key=lambda x: x.get('progresso', 0), reverse=True)

st.markdown("---")

# ============================================================================
# FORMULÁRIO DE EDIÇÃO
# ============================================================================

if st.session_state.get('editar_campanha_id'):
    campanha_id = st.session_state.get('editar_campanha_id')
    campanha = CampanhaDoacao.get_by_id(campanha_id)
    
    if campanha:
        with st.expander(f"✏️ Editando: {campanha.nome}", expanded=True):
            with st.form("form_editar_campanha"):
                st.markdown("### 📝 Dados da Campanha")
                
                nome_campanha = st.text_input(
                    "Nome da Campanha *",
                    value=campanha.nome or "",
                    placeholder="Ex: Natal Solidário 2024"
                )
                
                descricao = st.text_area(
                    "Descrição Detalhada *",
                    value=campanha.descricao or "",
                    placeholder="Descreva os objetivos e detalhes da campanha...",
                    height=100
                )
                
                col1, col2 = st.columns(2)
                
                with col1:
                    data_ini_valor = campanha.data_inicio if campanha.data_inicio else datetime.now()
                    if isinstance(data_ini_valor, str):
                        data_ini_valor = datetime.strptime(data_ini_valor, '%Y-%m-%d')
                    
                    data_inicio = st.date_input(
                        "Data de Início *",
                        value=data_ini_valor,
                        min_value=datetime(2020, 1, 1)
                    )
                
                with col2:
                    data_fim_valor = campanha.data_termino if campanha.data_termino else datetime.now() + timedelta(days=60)
                    if isinstance(data_fim_valor, str):
                        data_fim_valor = datetime.strptime(data_fim_valor, '%Y-%m-%d')
                    
                    data_fim = st.date_input(
                        "Data de Término *",
                        value=data_fim_valor,
                        min_value=datetime(2020, 1, 1)
                    )
                
                st.markdown("### 🎯 Meta e Arrecadação")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    tipo_meta = st.selectbox(
                        "Tipo de Meta",
                        ["R$", "Kg", "Unidades", "Litros", "Caixas"],
                        index=["R$", "Kg", "Unidades", "Litros", "Caixas"].index(campanha.tipo_meta or "R$")
                    )
                
                with col2:
                    meta = st.number_input(
                        "Meta *",
                        min_value=0.0,
                        value=float(campanha.meta or 0.0),
                        step=100.0,
                        format="%.2f",
                        help="Valor ou quantidade que deseja arrecadar"
                    )
                
                with col3:
                    arrecadado = st.number_input(
                        "Arrecadado",
                        min_value=0.0,
                        value=float(campanha.arrecadado or 0.0),
                        step=10.0,
                        format="%.2f",
                        help="Valor ou quantidade já arrecadada"
                    )
                
                # Mostrar progresso atual
                if meta > 0:
                    progresso_atual = (arrecadado / meta) * 100
                    st.progress(min(progresso_atual / 100, 1.0))
                    
                    col_prog1, col_prog2 = st.columns(2)
                    with col_prog1:
                        st.markdown(f"**Progresso: {progresso_atual:.1f}%**")
                    with col_prog2:
                        falta = meta - arrecadado
                        if falta > 0:
                            st.markdown(f"**Faltam: {falta:,.2f} {tipo_meta}**")
                        else:
                            st.markdown(f"**✅ Meta atingida!**")
                
                st.markdown("---")
                
                col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 4])
                
                with col_btn1:
                    submit = st.form_submit_button("✅ Salvar Alterações", use_container_width=True)
                
                with col_btn2:
                    cancelar = st.form_submit_button("❌ Cancelar", use_container_width=True)
                
                if submit:
                    if nome_campanha and descricao and meta > 0:
                        try:
                            campanha.nome = nome_campanha
                            campanha.descricao = descricao
                            campanha.data_inicio = data_inicio
                            campanha.data_termino = data_fim
                            campanha.meta = meta
                            campanha.arrecadado = arrecadado
                            campanha.tipo_meta = tipo_meta
                            
                            if campanha.update():
                                show_success_message(f"Campanha **{nome_campanha}** atualizada com sucesso!")
                                st.balloons()
                                
                                st.session_state.pop('editar_campanha_id', None)
                                
                                import time
                                time.sleep(1)
                                
                                st.rerun()
                            else:
                                show_error_message("Erro ao atualizar campanha no banco de dados")
                        except Exception as e:
                            show_error_message(f"Erro ao atualizar campanha: {str(e)}")
                    else:
                        show_error_message("Preencha todos os campos obrigatórios e defina uma meta maior que zero")
                
                if cancelar:
                    st.session_state.pop('editar_campanha_id', None)
                    st.rerun()
    else:
        show_error_message("Campanha não encontrada!")
        st.session_state.pop('editar_campanha_id', None)

# ============================================================================
# FORMULÁRIO DE NOVA CAMPANHA
# ============================================================================

if 'mostrar_form_campanha' not in st.session_state:
    st.session_state['mostrar_form_campanha'] = False

if st.session_state['mostrar_form_campanha']:
    with st.expander("📝 Formulário de Nova Campanha", expanded=True):
        with st.form("form_campanha"):
            st.markdown("### 📝 Dados da Campanha")
            
            nome_campanha = st.text_input(
                "Nome da Campanha *",
                placeholder="Ex: Natal Solidário 2024"
            )
            
            descricao = st.text_area(
                "Descrição Detalhada *",
                placeholder="Descreva os objetivos e detalhes da campanha...",
                height=100
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                data_inicio = st.date_input(
                    "Data de Início *",
                    value=datetime.now(),
                    min_value=datetime.now()
                )
            
            with col2:
                data_fim = st.date_input(
                    "Data de Término *",
                    value=datetime.now() + timedelta(days=60),
                    min_value=datetime.now()
                )
            
            st.markdown("### 🎯 Meta da Campanha")
            
            col1, col2 = st.columns(2)
            
            with col1:
                tipo_meta = st.selectbox(
                    "Tipo de Meta",
                    ["R$", "Kg", "Unidades", "Litros", "Caixas"],
                    help="Selecione o tipo de medida para a meta"
                )
            
            with col2:
                meta = st.number_input(
                    "Meta *",
                    min_value=0.0,
                    value=10000.0,
                    step=100.0,
                    format="%.2f",
                    help="Valor ou quantidade que deseja arrecadar"
                )
            
            st.info(f"💡 **Meta definida:** {meta:,.2f} {tipo_meta}")
            
            st.markdown("---")
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 4])
            
            with col_btn1:
                submit = st.form_submit_button("✅ Criar Campanha", use_container_width=True)
            
            with col_btn2:
                cancelar = st.form_submit_button("❌ Cancelar", use_container_width=True)
            
            if submit:
                if nome_campanha and descricao and meta > 0:
                    try:
                        campanha = CampanhaDoacao(
                            nome=nome_campanha,
                            descricao=descricao,
                            data_inicio=data_inicio,
                            data_termino=data_fim,
                            meta=meta,
                            arrecadado=0.0,
                            tipo_meta=tipo_meta
                        )
                        
                        if campanha.save():
                            show_success_message(f"Campanha **{nome_campanha}** criada com sucesso!")
                            st.info(f"✅ Meta: {meta:,.2f} {tipo_meta}")
                            st.balloons()
                            st.session_state['mostrar_form_campanha'] = False
                            st.rerun()
                        else:
                            show_error_message("Erro ao salvar campanha no banco de dados")
                    except Exception as e:
                        show_error_message(f"Erro ao criar campanha: {str(e)}")
                else:
                    show_error_message("Preencha todos os campos obrigatórios e defina uma meta maior que zero")
            
            if cancelar:
                st.session_state['mostrar_form_campanha'] = False
                st.rerun()

# ============================================================================
# ESTATÍSTICAS RÁPIDAS
# ============================================================================

st.markdown("### 📊 Estatísticas Gerais")

col1, col2, col3, col4 = st.columns(4)

total_campanhas = len(campanhas)
campanhas_ativas = len([c for c in campanhas if c['status'] == 'Ativa'])
campanhas_concluidas = len([c for c in campanhas if c['status'] == 'Concluída'])

# Calcular total arrecadado (apenas R$)
total_arrecadado = sum([c.get('arrecadado', 0) for c in campanhas if c.get('tipo_meta') == 'R$'])

with col1:
    st.metric("📊 Total de Campanhas", total_campanhas)

with col2:
    st.metric("🟢 Campanhas Ativas", campanhas_ativas)

with col3:
    st.metric("⚪ Campanhas Concluídas", campanhas_concluidas)

with col4:
    st.metric("💰 Total Arrecadado (R$)", f"R$ {total_arrecadado:,.2f}")

st.markdown("---")

# ============================================================================
# EXIBIR CARDS DE CAMPANHAS
# ============================================================================

st.markdown("### 📋 Campanhas")

if campanhas_filtradas:
    for campanha in campanhas_filtradas:
        with st.container():
            col_dados, col_acoes = st.columns([5, 1])
            
            with col_dados:
                # Calcular progresso REAL
                meta_valor = campanha.get('meta', 1)
                arrecadado_valor = campanha.get('arrecadado', 0)
                
                if meta_valor > 0:
                    progresso = (arrecadado_valor / meta_valor) * 100
                    progresso = min(progresso, 100)
                else:
                    progresso = 0
                
                # Status emoji
                status_emoji = "🟢" if campanha['status'] == 'Ativa' else "⚪"
                
                st.markdown(f"### {campanha['nome']}")
                st.markdown(f"**{status_emoji} Status:** {campanha['status']}")
                
                # Datas
                if campanha.get('data_inicio'):
                    data_ini = campanha['data_inicio'] if isinstance(campanha['data_inicio'], str) else campanha['data_inicio'].strftime('%d/%m/%Y')
                    data_fim = campanha['data_termino'] if isinstance(campanha['data_termino'], str) else campanha['data_termino'].strftime('%d/%m/%Y')
                    st.markdown(f"**📅 Período:** {data_ini} a {data_fim}")
                
                st.markdown(f"**👤 Responsável:** {campanha['responsavel']}")
                
                # Exibir meta e arrecadado REAIS
                tipo_meta = campanha.get('tipo_meta', 'R$')
                st.markdown(f"**🎯 Meta:** {meta_valor:,.2f} {tipo_meta}")
                st.markdown(f"**📊 Arrecadado:** {arrecadado_valor:,.2f} {tipo_meta}")
                
                # Barra de progresso
                st.progress(progresso / 100)
                
                # Mostrar progresso e faltante
                col_prog1, col_prog2 = st.columns(2)
                with col_prog1:
                    st.markdown(f"**Progresso: {progresso:.1f}%**")
                with col_prog2:
                    falta = meta_valor - arrecadado_valor
                    if falta > 0:
                        st.markdown(f"**Faltam: {falta:,.2f} {tipo_meta}**")
                    else:
                        st.markdown(f"**✅ Meta atingida!**")
                
                # Descrição
                if campanha.get('descricao'):
                    with st.expander("📄 Ver descrição completa"):
                        st.markdown(campanha['descricao'])
            
            with col_acoes:
                col_edit, col_del = st.columns(2)
                
                with col_edit:
                    if st.button(
                        "✏️",
                        key=f"edit_camp_{campanha['id']}",
                        help="Editar campanha",
                        use_container_width=True
                    ):
                        st.session_state['editar_campanha_id'] = campanha['id']
                        st.session_state.pop('mostrar_form_campanha', None)
                        st.rerun()
                
                with col_del:
                    if st.button(
                        "🗑️",
                        key=f"del_camp_{campanha['id']}",
                        help="Excluir campanha",
                        use_container_width=True
                    ):
                        st.session_state['campanha_deletar_id'] = campanha['id']
                        st.session_state['confirmar_exclusao_campanha'] = True
                        st.rerun()
            
            st.markdown("---")
else:
    show_info_message("Nenhuma campanha encontrada com os filtros aplicados")

# ============================================================================
# INFORMAÇÕES ADICIONAIS
# ============================================================================

with st.expander("ℹ️ Informações sobre Campanhas"):
    st.markdown("""
    ### 📢 Como funcionam as Campanhas
    
    As campanhas são eventos organizados para arrecadar doações com objetivos específicos:
    
    **Recursos disponíveis:**
    - ✅ **Criar campanhas** com nome, descrição e período
    - 🎯 **Definir metas** em R$, Kg, Unidades, Litros ou Caixas
    - 📊 **Acompanhar progresso** em tempo real
    - ✏️ **Editar campanhas** ativas
    - 🗑️ **Excluir campanhas** concluídas
    
    **Gestão de Metas:**
    - Defina uma meta clara para a campanha
    - Acompanhe o progresso em porcentagem
    - Atualize o valor arrecadado conforme as doações
    - Veja quanto ainda falta para atingir a meta
    
    **Status:**
    - 🟢 **Ativa:** Campanha em andamento
    - ⚪ **Concluída:** Campanha encerrada
    
    **Dicas:**
    - Use nomes descritivos (Ex: "Campanha de Inverno 2024")
    - Defina metas realistas e alcançáveis
    - Atualize regularmente o valor arrecadado
    - Mantenha a descrição clara e objetiva
    """)

# ============================================================================
# RODAPÉ
# ============================================================================

render_footer()