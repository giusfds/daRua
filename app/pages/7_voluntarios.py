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
from utils.mock_data import get_df_voluntarios

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

# Carregar dados mockados
df_voluntarios = get_df_voluntarios()

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
        ["Todos", "Ativo", "Inativo", "Aguardando aprovação"],
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
                cpf = st.text_input("CPF", placeholder="000.000.000-00")
                email = st.text_input("Email *", placeholder="exemplo@email.com")
            
            with col2:
                telefone = st.text_input("Telefone *", placeholder="(11) 98765-4321")
                data_nascimento = st.date_input(
                    "Data de Nascimento",
                    value=datetime(1990, 1, 1),
                    min_value=datetime(1940, 1, 1),
                    max_value=datetime.now()
                )
            
            st.markdown("### Informações de Voluntariado")
            
            col1, col2 = st.columns(2)
            
            with col1:
                areas_atuacao = st.multiselect(
                    "Áreas de Atuação *",
                    ["Logística", "Triagem", "Atendimento", "Administração", "TI"],
                    default=["Atendimento"]
                )
                
                periodo = st.selectbox(
                    "Período de Disponibilidade",
                    ["Manhã", "Tarde", "Noite", "Integral"]
                )
                
                status = st.selectbox(
                    "Status",
                    ["Ativo", "Inativo", "Aguardando aprovação"],
                    index=2
                )
            
            with col2:
                st.markdown("**Dias Disponíveis:**")
                dias = []
                col2a, col2b = st.columns(2)
                with col2a:
                    if st.checkbox("Segunda-feira"): dias.append("Segunda")
                    if st.checkbox("Terça-feira"): dias.append("Terça")
                    if st.checkbox("Quarta-feira"): dias.append("Quarta")
                    if st.checkbox("Quinta-feira"): dias.append("Quinta")
                with col2b:
                    if st.checkbox("Sexta-feira"): dias.append("Sexta")
                    if st.checkbox("Sábado"): dias.append("Sábado")
                    if st.checkbox("Domingo"): dias.append("Domingo")
            
            experiencia = st.text_area(
                "Experiência Anterior",
                placeholder="Descreva sua experiência prévia com trabalho voluntário ou áreas relacionadas...",
                height=100
            )
            
            st.markdown("---")
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 4])
            
            with col_btn1:
                submit = st.form_submit_button("✅ Cadastrar", use_container_width=True)
            
            with col_btn2:
                cancelar = st.form_submit_button("❌ Cancelar", use_container_width=True)
            
            # Processar formulário
            if submit:
                if nome and email and telefone and areas_atuacao:
                    show_success_message(f"Voluntário **{nome}** cadastrado com sucesso!")
                    show_success_message(f"Email: {email} | Telefone: {telefone}")
                    show_info_message(f"Status: {status} - Aguarde a aprovação para começar!")
                    st.balloons()
                    st.session_state['mostrar_form_voluntario'] = False
                    st.rerun()
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
if busca:
    mask = (
        df_filtrado['nome'].str.contains(busca, case=False, na=False) |
        df_filtrado['email'].str.contains(busca, case=False, na=False) |
        df_filtrado['telefone'].str.contains(busca, case=False, na=False)
    )
    df_filtrado = df_filtrado[mask]

# Filtrar por status
if filtro_status != "Todos":
    df_filtrado = df_filtrado[df_filtrado['status'] == filtro_status]

# Filtrar por área
if filtro_area != "Todas":
    df_filtrado = df_filtrado[df_filtrado['areas_atuacao'].str.contains(filtro_area, case=False, na=False)]

# ============================================================================
# ESTATÍSTICAS RÁPIDAS
# ============================================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total de Voluntários", len(df_voluntarios))

with col2:
    ativos = len(df_voluntarios[df_voluntarios['status'] == 'Ativo'])
    st.metric("Voluntários Ativos", ativos)

with col3:
    aguardando = len(df_voluntarios[df_voluntarios['status'] == 'Aguardando aprovação'])
    st.metric("Aguardando Aprovação", aguardando)

with col4:
    if busca or filtro_status != "Todos" or filtro_area != "Todas":
        st.metric("Resultados", len(df_filtrado))
    else:
        st.metric("Cadastros este Mês", 5)

st.markdown("---")

# ============================================================================
# TABELA DE VOLUNTÁRIOS
# ============================================================================

st.markdown("### 📋 Lista de Voluntários")

# Preparar dados para exibição
df_display = df_filtrado[['id', 'nome', 'email', 'telefone', 'areas_atuacao', 'disponibilidade', 'periodo', 'status']].copy()
df_display.columns = ['ID', 'Nome', 'Email', 'Telefone', 'Áreas de Atuação', 'Disponibilidade', 'Período', 'Status']

# Exibir tabela
st.dataframe(
    df_display,
    use_container_width=True,
    hide_index=True,
    column_config={
        "ID": st.column_config.NumberColumn(
            "ID",
            width="small",
        ),
        "Nome": st.column_config.TextColumn(
            "Nome",
            width="medium",
        ),
        "Email": st.column_config.TextColumn(
            "Email",
            width="medium",
        ),
        "Telefone": st.column_config.TextColumn(
            "Telefone",
            width="small",
        ),
        "Áreas de Atuação": st.column_config.TextColumn(
            "Áreas de Atuação",
            width="medium",
        ),
        "Disponibilidade": st.column_config.TextColumn(
            "Disponibilidade",
            width="medium",
        ),
        "Período": st.column_config.TextColumn(
            "Período",
            width="small",
        ),
        "Status": st.column_config.TextColumn(
            "Status",
            width="small",
        ),
    }
)

# Informação sobre resultados
if busca or filtro_status != "Todos" or filtro_area != "Todas":
    show_info_message(f"Mostrando {len(df_filtrado)} de {len(df_voluntarios)} voluntários")
else:
    show_info_message(f"Total de {len(df_voluntarios)} voluntários cadastrados")

st.markdown("---")

# ============================================================================
# GRÁFICOS E ANÁLISES
# ============================================================================

st.markdown("### 📊 Análises")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Distribuição por Status")
    status_counts = df_voluntarios['status'].value_counts()
    st.bar_chart(status_counts)

with col2:
    st.markdown("#### Distribuição por Período")
    periodo_counts = df_voluntarios['periodo'].value_counts()
    st.bar_chart(periodo_counts)

st.markdown("---")

# Análise de áreas de atuação
st.markdown("#### Áreas de Atuação mais Populares")

# Contar quantos voluntários atuam em cada área
areas_list = []
for areas in df_voluntarios['areas_atuacao']:
    areas_list.extend([a.strip() for a in areas.split(',')])

areas_series = pd.Series(areas_list).value_counts()
st.bar_chart(areas_series)

st.markdown("---")

# ============================================================================
# AÇÕES RÁPIDAS
# ============================================================================

st.markdown("### ⚡ Ações Rápidas")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("✅ Aprovar Pendentes", use_container_width=True):
        show_success_message(f"{aguardando} voluntário(s) aprovado(s)!")

with col2:
    if st.button("📧 Enviar Email em Massa", use_container_width=True):
        show_info_message("Funcionalidade de envio de email será implementada em breve!", "🚧")

with col3:
    if st.button("📄 Gerar Lista de Presença", use_container_width=True):
        show_info_message("Funcionalidade de geração de lista será implementada em breve!", "🚧")

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
    3. Selecione as áreas de atuação de interesse
    4. Marque os dias e períodos disponíveis
    5. Descreva experiências anteriores (opcional)
    6. Clique em "Cadastrar"
    
    **Campos Obrigatórios:**
    - Nome Completo
    - Email
    - Telefone
    - Áreas de Atuação (pelo menos uma)
    
    **Campos Opcionais:**
    - CPF
    - Data de Nascimento
    - Experiência Anterior
    
    **Buscar e Filtrar:**
    - Use a barra de busca para encontrar por nome, email ou telefone
    - Filtre por status (Ativo, Inativo, Aguardando)
    - Filtre por área de atuação
    - Os filtros podem ser combinados
    
    **Áreas de Atuação:**
    - **Logística:** Transporte e distribuição de doações
    - **Triagem:** Separação e organização de itens doados
    - **Atendimento:** Contato direto com beneficiários
    - **Administração:** Atividades administrativas e gestão
    - **TI:** Suporte técnico e tecnologia
    
    **Status dos Voluntários:**
    - **Ativo:** Voluntário aprovado e em atividade
    - **Inativo:** Voluntário temporariamente afastado
    - **Aguardando aprovação:** Novo cadastro pendente de aprovação
    
    **Períodos de Disponibilidade:**
    - **Manhã:** 6h às 12h
    - **Tarde:** 12h às 18h
    - **Noite:** 18h às 22h
    - **Integral:** Disponibilidade em qualquer horário
    
    **Boas Práticas:**
    - Aprovar ou recusar cadastros em até 48 horas
    - Manter contato regular com voluntários ativos
    - Realizar treinamentos periódicos
    - Reconhecer e valorizar o trabalho voluntário
    - Documentar horas de trabalho voluntário
    
    > 💡 **Dica:** Voluntários bem treinados e engajados são essenciais para o sucesso da organização!
    """)

# ============================================================================
# RODAPÉ
# ============================================================================

render_footer()
