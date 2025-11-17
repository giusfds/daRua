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
from utils.mock_data import get_campanhas_mockadas, get_doadores_mockados

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

# Carregar dados mockados
campanhas = get_campanhas_mockadas()
doadores = get_doadores_mockados()

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
        ["Mais Recentes", "Nome A-Z", "Progresso"],
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
                
                meta = st.number_input(
                    "Meta de Arrecadação *",
                    min_value=1,
                    value=10000,
                    step=100
                )
                
                tipo_meta = st.selectbox(
                    "Tipo de Meta *",
                    ["R$", "Kg", "Unidades", "Kits", "Peças", "Cestas"]
                )
            
            with col2:
                data_fim = st.date_input(
                    "Data de Término *",
                    value=datetime.now() + timedelta(days=60),
                    min_value=datetime.now()
                )
                
                tipos_doacao = st.multiselect(
                    "Tipos de Doação Desejada *",
                    ["Alimentos", "Roupas", "Medicamentos", "Dinheiro", "Material Escolar", "Brinquedos", "Livros", "Outros"],
                    default=["Alimentos"]
                )
                
                responsavel = st.selectbox(
                    "Responsável *",
                    [d['nome'] for d in doadores[:10]]
                )
            
            st.markdown("---")
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 4])
            
            with col_btn1:
                submit = st.form_submit_button("✅ Criar Campanha", use_container_width=True)
            
            with col_btn2:
                cancelar = st.form_submit_button("❌ Cancelar", use_container_width=True)
            
            # Processar formulário
            if submit:
                if nome_campanha and descricao and meta and tipos_doacao and responsavel:
                    show_success_message(f"Campanha **{nome_campanha}** criada com sucesso!")
                    show_success_message(f"Meta: {meta} {tipo_meta} | Responsável: {responsavel}")
                    st.balloons()
                    st.session_state['mostrar_form_campanha'] = False
                    st.rerun()
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
    # Calcular média de progresso das ativas
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
elif ordenar == "Progresso":
    campanhas_filtradas = sorted(campanhas_filtradas, key=lambda x: x['arrecadado']/x['meta'], reverse=True)
# "Mais Recentes" já está na ordem padrão

# ============================================================================
# EXIBIR CARDS DE CAMPANHAS
# ============================================================================

st.markdown("### 📋 Campanhas")

# Exibir em grid de 2 colunas
for i in range(0, len(campanhas_filtradas), 2):
    cols = st.columns(2)
    
    for j, col in enumerate(cols):
        if i + j < len(campanhas_filtradas):
            campanha = campanhas_filtradas[i + j]
            
            with col:
                # Calcular progresso
                progresso = (campanha['arrecadado'] / campanha['meta']) * 100
                progresso = min(progresso, 100)  # Limitar a 100%
                
                # Determinar cor do status
                if campanha['status'] == 'Ativa':
                    status_emoji = "🟢"
                    status_color = "#10B981"
                else:
                    status_emoji = "⚪"
                    status_color = "#6B7280"
                
                # Card da campanha
                with st.container():
                    st.markdown(f"""
                        <div class="campanha-card">
                            <h3 style="margin-top:0;">{campanha['nome']}</h3>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"**{status_emoji} Status:** {campanha['status']}")
                    st.markdown(f"**📅 Período:** {campanha['data_inicio']} a {campanha['data_fim']}")
                    st.markdown(f"**👤 Responsável:** {campanha['responsavel']}")
                    st.markdown(f"**🎯 Meta:** {campanha['meta']:,} {campanha['tipo_meta']}")
                    st.markdown(f"**📊 Arrecadado:** {campanha['arrecadado']:,} {campanha['tipo_meta']}")
                    
                    # Barra de progresso
                    st.progress(progresso / 100)
                    st.markdown(f"**Progresso: {progresso:.1f}%**")
                    
                    # Descrição (resumida)
                    with st.expander("Ver descrição completa"):
                        st.markdown(campanha['descricao'])
                        st.markdown(f"**Tipos de doação:** {campanha['tipos_doacao']}")
                    
                    # Botões de ação
                    col_btn1, col_btn2, col_btn3 = st.columns(3)
                    
                    with col_btn1:
                        if st.button("👁️ Detalhes", key=f"det_{campanha['id']}", use_container_width=True):
                            show_info_message(f"Detalhes da campanha '{campanha['nome']}' serão implementados em breve!", "🚧")
                    
                    with col_btn2:
                        if st.button("✏️ Editar", key=f"edit_{campanha['id']}", use_container_width=True):
                            show_info_message(f"Edição da campanha '{campanha['nome']}' será implementada em breve!", "🚧")
                    
                    with col_btn3:
                        if campanha['status'] == 'Ativa':
                            if st.button("✅ Finalizar", key=f"fin_{campanha['id']}", use_container_width=True):
                                show_success_message(f"Campanha '{campanha['nome']}' finalizada!")
                
                st.markdown("---")

# Informação sobre resultados
if filtro_status != "Todas":
    show_info_message(f"Mostrando {len(campanhas_filtradas)} campanhas com status: {filtro_status}")

st.markdown("---")

# ============================================================================
# GRÁFICO DE DESEMPENHO DAS CAMPANHAS
# ============================================================================

st.markdown("### 📊 Desempenho das Campanhas Ativas")

if campanhas_ativas:
    # Criar DataFrame para gráfico
    df_chart = pd.DataFrame([
        {
            'Campanha': c['nome'][:30] + '...' if len(c['nome']) > 30 else c['nome'],
            'Progresso (%)': (c['arrecadado'] / c['meta']) * 100
        }
        for c in campanhas_ativas
    ])
    
    st.bar_chart(df_chart.set_index('Campanha'))
else:
    show_info_message("Não há campanhas ativas no momento")

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
    3. Defina a meta e o tipo de arrecadação
    4. Selecione os tipos de doação aceitos
    5. Clique em "Criar Campanha"
    
    **Campos Obrigatórios:**
    - Nome da Campanha
    - Descrição Detalhada
    - Data de Início e Término
    - Meta de Arrecadação
    - Tipo de Meta (R$, Kg, Unidades, etc.)
    - Tipos de Doação Desejada
    - Responsável pela campanha
    
    **Gerenciar Campanhas:**
    - Use os filtros para visualizar campanhas ativas ou concluídas
    - Ordene por nome, data ou progresso
    - Clique em "Detalhes" para ver informações completas
    - Clique em "Editar" para modificar dados da campanha
    - Clique em "Finalizar" para encerrar uma campanha ativa
    
    **Status das Campanhas:**
    - **Ativa:** Campanha em andamento, aceitando doações
    - **Concluída:** Campanha encerrada, meta atingida ou prazo expirado
    
    **Boas Práticas:**
    - Defina metas realistas e alcançáveis
    - Mantenha as descrições claras e objetivas
    - Atualize o progresso regularmente
    - Comunique os resultados aos doadores
    - Finalize campanhas quando atingirem a meta ou prazo
    
    > 💡 **Dica:** Campanhas com metas claras e prazos definidos tendem a ter melhor desempenho!
    """)

# ============================================================================
# RODAPÉ
# ============================================================================

render_footer()
