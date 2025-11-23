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
from models.ponto_coleta import PontoColeta

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

# Carregar dados do banco
try:
    pontos_list = PontoColeta.get_all()
    if pontos_list:
        pontos = []
        for p in pontos_list:
            ponto_dict = p.to_dict()
            # Adicionar campos de compatibilidade
            ponto_dict['id'] = p.idPontoColeta
            ponto_dict['nome'] = p.responsavel  # Usar responsável como nome
            # Montar endereço completo
            end_parts = []
            if p.logradouro:
                end_parts.append(p.logradouro)
            if p.numero:
                end_parts.append(p.numero)
            if p.bairro:
                end_parts.append(f"- {p.bairro}")
            if p.cidade:
                end_parts.append(f", {p.cidade}")
            if p.estado:
                end_parts.append(f" - {p.estado}")
            if p.cep:
                end_parts.append(f" - CEP: {p.cep}")
            ponto_dict['endereco'] = ' '.join(end_parts) if end_parts else 'Endereço não informado'
            ponto_dict['horario'] = 'Seg-Sex 9h-18h'  # Valor padrão
            ponto_dict['telefone'] = '-'  # Valor padrão
            ponto_dict['email'] = '-'  # Valor padrão
            ponto_dict['status'] = 'Ativo'  # Valor padrão
            pontos.append(ponto_dict)
    else:
        pontos = []
except Exception as e:
    show_error_message(f"Erro ao carregar pontos de coleta: {str(e)}")
    pontos = []

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
            
            responsavel = st.text_input(
                "Responsável *",
                placeholder="Nome do responsável pelo ponto"
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
                bairro = st.text_input("Bairro *", placeholder="Ex: Centro")
            
            with col2:
                cidade = st.text_input("Cidade *", placeholder="Belo Horizonte")
            
            with col3:
                estado = st.text_input("Estado (UF) *", placeholder="MG", max_chars=2)
            
            cep = st.text_input("CEP", placeholder="00000-000")
            
            st.markdown("---")
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 4])
            
            with col_btn1:
                submit = st.form_submit_button("💾 Salvar", use_container_width=True)
            
            with col_btn2:
                cancelar = st.form_submit_button("❌ Cancelar", use_container_width=True)
            
            # Processar formulário
            if submit:
                if responsavel and rua and numero and bairro and cidade and estado:
                    try:
                        # Criar objeto PontoColeta
                        ponto = PontoColeta(
                            responsavel=responsavel,
                            logradouro=rua,
                            numero=numero,
                            complemento=complemento if complemento else None,
                            bairro=bairro,
                            cidade=cidade,
                            estado=estado.upper(),
                            cep=cep if cep else None
                        )
                        
                        # Salvar no banco
                        if ponto.save():
                            endereco_completo = f"{rua}, {numero} - {bairro}, {cidade}, {estado}"
                            show_success_message(f"Ponto de coleta **{responsavel}** cadastrado com sucesso!")
                            show_success_message(f"Endereço: {endereco_completo}")
                            st.balloons()
                            st.session_state['mostrar_form_ponto'] = False
                            st.rerun()
                        else:
                            show_error_message("Erro ao salvar ponto no banco de dados")
                    except Exception as e:
                        show_error_message(f"Erro ao cadastrar ponto: {str(e)}")
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
        st.metric("Cadastros este Mês", "-")

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
                    # Status emoji
                    status_emoji = "🟢" if ponto['status'] == 'Ativo' else "🔴"
                    
                    # Card do ponto
                    with st.container():
                        st.markdown(f"### {status_emoji} {ponto['nome']}")
                        
                        st.markdown(f"**📍 Endereço:**")
                        st.text(ponto['endereco'])
                        
                        st.markdown(f"**🕐 Horário:** {ponto['horario']}")
                        st.markdown(f"**👤 Responsável:** {ponto['responsavel']}")
                        st.markdown(f"**📞 Telefone:** {ponto['telefone']}")
                        st.markdown(f"**📧 Email:** {ponto['email']}")
                        st.markdown(f"**Status:** {ponto['status']}")
                    
                    st.markdown("---")
else:
    show_info_message("Nenhum ponto de coleta encontrado com os filtros aplicados")

# Informação sobre resultados
if busca or filtro_status != "Todos":
    show_info_message(f"Mostrando {len(pontos_filtrados)} de {len(pontos)} pontos de coleta")

st.markdown("---")

# ============================================================================
# INFORMAÇÕES ADICIONAIS
# ============================================================================

with st.expander("ℹ️ Informações sobre Pontos de Coleta"):
    st.markdown("""
    ### Como usar esta página:
    
    **Cadastrar Novo Ponto:**
    1. Clique no botão "Cadastrar Novo Ponto"
    2. Preencha todos os campos obrigatórios (*)
    3. Informe o endereço completo
    4. Clique em "Salvar"
    
    **Campos Obrigatórios:**
    - Responsável
    - Rua e Número
    - Bairro, Cidade e Estado
    
    **Buscar Pontos:**
    - Use a barra de busca para encontrar por nome, endereço ou responsável
    - Filtre por status (Ativo/Inativo)
    
    > 💡 **Dica:** Pontos de coleta bem localizados facilitam as doações!
    """)

# ============================================================================
# RODAPÉ
# ============================================================================

render_footer()