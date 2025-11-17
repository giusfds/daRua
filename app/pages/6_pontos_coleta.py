"""
Página de Gerenciamento de Pontos de Coleta
Cadastra e visualiza locais de coleta de doações
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

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
from utils.mock_data import get_pontos_coleta_mockados

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================

setup_page("Pontos de Coleta - Somos DaRua", "📍")
apply_global_css()

# ============================================================================
# SIDEBAR - NAVEGAÇÃO
# ============================================================================

render_sidebar("Pontos de Coleta")

# ============================================================================
# CONTEÚDO PRINCIPAL
# ============================================================================

st.title("📍 Pontos de Coleta")
st.markdown("Cadastre e gerencie os pontos de coleta de doações")
st.markdown("---")

# Carregar dados mockados
pontos = get_pontos_coleta_mockados()

# ============================================================================
# BUSCA E NOVO CADASTRO
# ============================================================================

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    busca = st.text_input(
        "🔍 Buscar ponto de coleta",
        placeholder="Pesquisar por nome, endereço ou responsável...",
        label_visibility="collapsed"
    )

with col2:
    filtro_status = st.selectbox(
        "Status",
        ["Todos", "Ativo", "Inativo"],
        label_visibility="collapsed"
    )

with col3:
    if st.button("➕ Cadastrar Novo Ponto", use_container_width=True):
        st.session_state['mostrar_form_ponto'] = True

st.markdown("---")

# ============================================================================
# FORMULÁRIO DE CADASTRO
# ============================================================================

if 'mostrar_form_ponto' not in st.session_state:
    st.session_state['mostrar_form_ponto'] = False

if st.session_state['mostrar_form_ponto']:
    with st.expander("📝 Formulário de Cadastro de Ponto de Coleta", expanded=True):
        with st.form("form_ponto"):
            st.markdown("### Dados do Ponto de Coleta")
            
            nome_ponto = st.text_input(
                "Nome do Ponto *",
                placeholder="Ex: Centro Comunitário da Mooca"
            )
            
            st.markdown("#### Endereço")
            
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                rua = st.text_input("Rua *", placeholder="Ex: Rua das Flores")
            
            with col2:
                numero = st.text_input("Número *", placeholder="123")
            
            with col3:
                complemento = st.text_input("Complemento", placeholder="Apto 45")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                bairro = st.text_input("Bairro *", placeholder="Ex: Mooca")
            
            with col2:
                cidade = st.text_input("Cidade *", value="São Paulo")
            
            with col3:
                cep = st.text_input("CEP *", placeholder="00000-000")
            
            st.markdown("#### Informações de Contato")
            
            col1, col2 = st.columns(2)
            
            with col1:
                horario = st.text_input(
                    "Horário de Funcionamento *",
                    placeholder="Ex: Seg-Sex 9h-18h"
                )
                responsavel = st.text_input(
                    "Responsável *",
                    placeholder="Nome do responsável"
                )
                telefone = st.text_input(
                    "Telefone *",
                    placeholder="(11) 98765-4321"
                )
            
            with col2:
                email = st.text_input(
                    "Email",
                    placeholder="contato@exemplo.com"
                )
                observacoes = st.text_area(
                    "Observações",
                    placeholder="Informações adicionais sobre o ponto de coleta...",
                    height=100
                )
                ativo = st.checkbox("Ponto Ativo", value=True)
            
            st.markdown("---")
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 4])
            
            with col_btn1:
                submit = st.form_submit_button("💾 Salvar", use_container_width=True)
            
            with col_btn2:
                cancelar = st.form_submit_button("❌ Cancelar", use_container_width=True)
            
            # Processar formulário
            if submit:
                if nome_ponto and rua and numero and bairro and cidade and cep and horario and responsavel and telefone:
                    endereco_completo = f"{rua}, {numero} - {bairro}, {cidade}, SP - CEP: {cep}"
                    show_success_message(f"Ponto de coleta **{nome_ponto}** cadastrado com sucesso!")
                    show_success_message(f"Endereço: {endereco_completo}")
                    st.balloons()
                    st.session_state['mostrar_form_ponto'] = False
                    st.rerun()
                else:
                    show_error_message("Por favor, preencha todos os campos obrigatórios (*)")
            
            if cancelar:
                st.session_state['mostrar_form_ponto'] = False
                st.rerun()

# ============================================================================
# FILTRAR DADOS
# ============================================================================

pontos_filtrados = pontos.copy()

# Filtrar por busca
if busca:
    pontos_filtrados = [
        p for p in pontos_filtrados
        if busca.lower() in p['nome'].lower() or 
           busca.lower() in p['endereco'].lower() or 
           busca.lower() in p['responsavel'].lower()
    ]

# Filtrar por status
if filtro_status != "Todos":
    pontos_filtrados = [p for p in pontos_filtrados if p['status'] == filtro_status]

# ============================================================================
# ESTATÍSTICAS RÁPIDAS
# ============================================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total de Pontos", len(pontos))

with col2:
    ativos = len([p for p in pontos if p['status'] == 'Ativo'])
    st.metric("Pontos Ativos", ativos)

with col3:
    inativos = len([p for p in pontos if p['status'] == 'Inativo'])
    st.metric("Pontos Inativos", inativos)

with col4:
    if busca or filtro_status != "Todos":
        st.metric("Resultados", len(pontos_filtrados))
    else:
        st.metric("Cadastros este Mês", 2)

st.markdown("---")

# ============================================================================
# EXIBIR CARDS DE PONTOS DE COLETA
# ============================================================================

st.markdown("### 📋 Lista de Pontos de Coleta")

if pontos_filtrados:
    # Exibir em grid de 2 colunas
    for i in range(0, len(pontos_filtrados), 2):
        cols = st.columns(2)
        
        for j, col in enumerate(cols):
            if i + j < len(pontos_filtrados):
                ponto = pontos_filtrados[i + j]
                
                with col:
                    # Status emoji e cor
                    if ponto['status'] == 'Ativo':
                        status_emoji = "🟢"
                    else:
                        status_emoji = "🔴"
                    
                    # Card do ponto
                    with st.container():
                        st.markdown(f"""
                            <div class="ponto-card">
                                <h3 style="margin-top:0;">{status_emoji} {ponto['nome']}</h3>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown(f"**📍 Endereço:**")
                        st.text(ponto['endereco'])
                        
                        st.markdown(f"**🕐 Horário:** {ponto['horario']}")
                        st.markdown(f"**👤 Responsável:** {ponto['responsavel']}")
                        st.markdown(f"**📞 Telefone:** {ponto['telefone']}")
                        st.markdown(f"**📧 Email:** {ponto['email']}")
                        st.markdown(f"**Status:** {ponto['status']}")
                        
                        # Botões de ação
                        col_btn1, col_btn2, col_btn3 = st.columns(3)
                        
                        with col_btn1:
                            if st.button("👁️ Detalhes", key=f"det_{ponto['id']}", use_container_width=True):
                                show_info_message(f"Detalhes do ponto '{ponto['nome']}' serão implementados em breve!", "🚧")
                        
                        with col_btn2:
                            if st.button("✏️ Editar", key=f"edit_{ponto['id']}", use_container_width=True):
                                show_info_message(f"Edição do ponto '{ponto['nome']}' será implementada em breve!", "🚧")
                        
                        with col_btn3:
                            if ponto['status'] == 'Ativo':
                                if st.button("⏸️ Desativar", key=f"des_{ponto['id']}", use_container_width=True):
                                    show_warning_message(f"Ponto '{ponto['nome']}' desativado!")
                            else:
                                if st.button("▶️ Ativar", key=f"ati_{ponto['id']}", use_container_width=True):
                                    show_success_message(f"Ponto '{ponto['nome']}' ativado!")
                    
                    st.markdown("---")
else:
    show_info_message("Nenhum ponto de coleta encontrado com os filtros aplicados")

# Informação sobre resultados
if busca or filtro_status != "Todos":
    show_info_message(f"Mostrando {len(pontos_filtrados)} de {len(pontos)} pontos de coleta")

st.markdown("---")

# ============================================================================
# MAPA (SIMULADO)
# ============================================================================

st.markdown("### 🗺️ Mapa de Pontos de Coleta")
show_info_message("Visualização de mapa com localização dos pontos será implementada em breve!", "🚧")

# ============================================================================
# INFORMAÇÕES ADICIONAIS
# ============================================================================

with st.expander("ℹ️ Informações sobre Pontos de Coleta"):
    st.markdown("""
    ### Como usar esta página:
    
    **Cadastrar Novo Ponto:**
    1. Clique no botão "Cadastrar Novo Ponto"
    2. Preencha todos os campos obrigatórios (*)
    3. Informe o endereço completo com CEP
    4. Defina o horário de funcionamento
    5. Indique o responsável e dados de contato
    6. Marque se o ponto está ativo
    7. Clique em "Salvar"
    
    **Campos Obrigatórios:**
    - Nome do Ponto
    - Rua e Número
    - Bairro, Cidade e CEP
    - Horário de Funcionamento
    - Responsável
    - Telefone de Contato
    
    **Campos Opcionais:**
    - Complemento do endereço
    - Email
    - Observações
    
    **Buscar Pontos:**
    - Use a barra de busca para encontrar por nome, endereço ou responsável
    - Filtre por status (Ativo/Inativo)
    - Os filtros podem ser combinados
    
    **Gerenciar Pontos:**
    - Clique em "Detalhes" para ver informações completas
    - Clique em "Editar" para modificar dados do ponto
    - Use "Desativar" para pausar temporariamente um ponto
    - Use "Ativar" para reativar um ponto desativado
    
    **Status dos Pontos:**
    - **Ativo:** Ponto em funcionamento, aceitando doações
    - **Inativo:** Ponto temporariamente fechado ou desativado
    
    **Boas Práticas:**
    - Mantenha os dados de contato sempre atualizados
    - Informe horários de funcionamento precisos
    - Atualize o status quando houver mudanças
    - Mantenha observações relevantes para doadores
    
    > 💡 **Dica:** Pontos de coleta bem localizados e com horários flexíveis facilitam as doações!
    """)

# ============================================================================
# RODAPÉ
# ============================================================================

render_footer()
