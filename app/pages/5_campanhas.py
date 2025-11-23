"""
Página de Gerenciamento de Campanhas
Cria e gerencia campanhas de arrecadação
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path
from datetime import datetime, timedelta

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
    COLORS
)

# Importar modelo do backend
from models.campanha_doacao import CampanhaDoacao

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================

setup_page("Campanhas - Somos DaRua", "📢")
apply_global_css()

# ============================================================================
# SIDEBAR - NAVEGAÇÃO
# ============================================================================

render_sidebar("Campanhas")

# ============================================================================
# CONTEÚDO PRINCIPAL
# ============================================================================

st.title("📢 Campanhas de Arrecadação")
st.markdown("Crie e gerencie campanhas para arrecadação de doações")
st.markdown("---")

# Carregar dados do banco
try:
    campanhas_list = CampanhaDoacao.get_all()
    if campanhas_list:
        campanhas = []
        for c in campanhas_list:
            camp_dict = c.to_dict()
            # Adicionar campos de compatibilidade
            camp_dict['id'] = c.idCampanhaDoacao
            camp_dict['status'] = 'Ativa' if c.data_termino is None or c.data_termino >= datetime.now().date() else 'Concluída'
            camp_dict['responsavel'] = 'Administrador'
            camp_dict['meta'] = 10000
            camp_dict['arrecadado'] = 5000
            camp_dict['tipo_meta'] = 'R$'
            camp_dict['tipos_doacao'] = 'Alimentos, Roupas'
            campanhas.append(camp_dict)
    else:
        campanhas = []
except Exception as e:
    show_error_message(f"Erro ao carregar campanhas: {str(e)}")
    campanhas = []

# ============================================================================
# BOTÃO NOVA CAMPANHA E FILTROS
# ============================================================================

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    if st.button("➕ Nova Campanha", use_container_width=True):
        st.session_state['mostrar_form_campanha'] = True

with col2:
    filtro_status = st.selectbox(
        "Filtrar por Status",
        ["Todas", "Ativa", "Concluída"],
        label_visibility="collapsed"
    )

with col3:
    ordenar = st.selectbox(
        "Ordenar por",
        ["Mais Recentes", "Nome A-Z"],
        label_visibility="collapsed"
    )

st.markdown("---")

# ============================================================================
# FORMULÁRIO DE NOVA CAMPANHA
# ============================================================================

if 'mostrar_form_campanha' not in st.session_state:
    st.session_state['mostrar_form_campanha'] = False

if st.session_state['mostrar_form_campanha']:
    with st.expander("📝 Formulário de Nova Campanha", expanded=True):
        with st.form("form_campanha"):
            st.markdown("### Dados da Campanha")
            
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
            
            st.markdown("---")
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 4])
            
            with col_btn1:
                submit = st.form_submit_button("✅ Criar Campanha", use_container_width=True)
            
            with col_btn2:
                cancelar = st.form_submit_button("❌ Cancelar", use_container_width=True)
            
            # Processar formulário
            if submit:
                if nome_campanha and descricao:
                    try:
                        # Criar objeto CampanhaDoacao
                        campanha = CampanhaDoacao(
                            nome=nome_campanha,
                            descricao=descricao,
                            data_inicio=data_inicio,
                            data_termino=data_fim
                        )
                        
                        # Salvar no banco
                        if campanha.save():
                            show_success_message(f"Campanha **{nome_campanha}** criada com sucesso!")
                            st.balloons()
                            st.session_state['mostrar_form_campanha'] = False
                            st.rerun()
                        else:
                            show_error_message("Erro ao salvar campanha no banco de dados")
                    except Exception as e:
                        show_error_message(f"Erro ao criar campanha: {str(e)}")
                else:
                    show_error_message("Por favor, preencha todos os campos obrigatórios (*)")
            
            if cancelar:
                st.session_state['mostrar_form_campanha'] = False
                st.rerun()

# ============================================================================
# ESTATÍSTICAS RÁPIDAS
# ============================================================================

col1, col2, col3, col4 = st.columns(4)

# Filtrar campanhas por status
campanhas_ativas = [c for c in campanhas if c['status'] == 'Ativa']
campanhas_concluidas = [c for c in campanhas if c['status'] == 'Concluída']

with col1:
    st.metric("Total de Campanhas", len(campanhas))

with col2:
    st.metric("Campanhas Ativas", len(campanhas_ativas))

with col3:
    st.metric("Campanhas Concluídas", len(campanhas_concluidas))

with col4:
    if campanhas_ativas:
        progresso_medio = sum([c['arrecadado']/c['meta']*100 for c in campanhas_ativas]) / len(campanhas_ativas)
        st.metric("Progresso Médio", f"{progresso_medio:.0f}%")
    else:
        st.metric("Progresso Médio", "0%")

st.markdown("---")

# ============================================================================
# FILTRAR E ORDENAR CAMPANHAS
# ============================================================================

# Filtrar por status
if filtro_status == "Ativa":
    campanhas_filtradas = campanhas_ativas
elif filtro_status == "Concluída":
    campanhas_filtradas = campanhas_concluidas
else:
    campanhas_filtradas = campanhas

# Ordenar
if ordenar == "Nome A-Z":
    campanhas_filtradas = sorted(campanhas_filtradas, key=lambda x: x['nome'])

# ============================================================================
# EXIBIR CARDS DE CAMPANHAS
# ============================================================================

st.markdown("### 📋 Campanhas")

if campanhas_filtradas:
    # Exibir em grid de 2 colunas
    for i in range(0, len(campanhas_filtradas), 2):
        cols = st.columns(2)
        
        for j, col in enumerate(cols):
            if i + j < len(campanhas_filtradas):
                campanha = campanhas_filtradas[i + j]
                
                with col:
                    # Calcular progresso
                    progresso = (campanha['arrecadado'] / campanha['meta']) * 100
                    progresso = min(progresso, 100)
                    
                    # Status emoji
                    status_emoji = "🟢" if campanha['status'] == 'Ativa' else "⚪"
                    
                    # Card da campanha
                    with st.container():
                        st.markdown(f"### {campanha['nome']}")
                        st.markdown(f"**{status_emoji} Status:** {campanha['status']}")
                        
                        # Datas
                        if campanha.get('data_inicio'):
                            data_ini = campanha['data_inicio'] if isinstance(campanha['data_inicio'], str) else campanha['data_inicio'].strftime('%d/%m/%Y')
                            data_fim = campanha['data_termino'] if isinstance(campanha['data_termino'], str) else campanha['data_termino'].strftime('%d/%m/%Y')
                            st.markdown(f"**📅 Período:** {data_ini} a {data_fim}")
                        
                        st.markdown(f"**👤 Responsável:** {campanha['responsavel']}")
                        st.markdown(f"**🎯 Meta:** {campanha['meta']:,} {campanha['tipo_meta']}")
                        st.markdown(f"**📊 Arrecadado:** {campanha['arrecadado']:,} {campanha['tipo_meta']}")
                        
                        # Barra de progresso
                        st.progress(progresso / 100)
                        st.markdown(f"**Progresso: {progresso:.1f}%**")
                        
                        # Descrição
                        with st.expander("Ver descrição completa"):
                            st.markdown(campanha.get('descricao', 'Sem descrição'))
                    
                    st.markdown("---")
else:
    show_info_message("Nenhuma campanha encontrada")

# Informação sobre resultados
if filtro_status != "Todas":
    show_info_message(f"Mostrando {len(campanhas_filtradas)} campanhas com status: {filtro_status}")

st.markdown("---")

# ============================================================================
# INFORMAÇÕES ADICIONAIS
# ============================================================================

with st.expander("ℹ️ Informações sobre Gerenciamento de Campanhas"):
    st.markdown("""
    ### Como usar esta página:
    
    **Criar Nova Campanha:**
    1. Clique no botão "Nova Campanha"
    2. Preencha todos os campos obrigatórios (*)
    3. Defina as datas de início e término
    4. Clique em "Criar Campanha"
    
    **Campos Obrigatórios:**
    - Nome da Campanha
    - Descrição Detalhada
    - Data de Início e Término
    
    **Gerenciar Campanhas:**
    - Use os filtros para visualizar campanhas ativas ou concluídas
    - Ordene por nome ou data
    
    > 💡 **Dica:** Campanhas com descrições claras tendem a ter melhor desempenho!
    """)

# ============================================================================
# RODAPÉ
# ============================================================================

render_footer()