"""
Página de Registro e Gerenciamento de Doações
Registra novas doações e visualiza histórico
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
    show_info_message
)
from utils.mock_data import get_df_doacoes, get_doadores_mockados, get_pontos_coleta_mockados

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================

setup_page("Doações - Somos DaRua", "📦")
apply_global_css()

# ============================================================================
# SIDEBAR - NAVEGAÇÃO
# ============================================================================

render_sidebar("Doações")

# ============================================================================
# CONTEÚDO PRINCIPAL
# ============================================================================

st.title("📦 Registrar Doações")
st.markdown("Registre novas doações e acompanhe o histórico de recebimentos")
st.markdown("---")

# Carregar dados mockados
df_doacoes = get_df_doacoes()
doadores = get_doadores_mockados()
pontos = get_pontos_coleta_mockados()

# ============================================================================
# ABAS
# ============================================================================

tab1, tab2 = st.tabs(["📝 Nova Doação", "📋 Histórico de Doações"])

# ============================================================================
# ABA 1 - NOVA DOAÇÃO
# ============================================================================

with tab1:
    st.markdown("### Registrar Nova Doação")
    
    with st.form("form_doacao"):
        col1, col2 = st.columns(2)
        
        with col1:
            data_doacao = st.date_input(
                "Data da Doação *",
                value=datetime.now(),
                max_value=datetime.now()
            )
            
            doador_selecionado = st.selectbox(
                "Doador *",
                options=[d['nome'] for d in doadores],
                placeholder="Selecione um doador..."
            )
            
            tipo_doacao = st.selectbox(
                "Tipo de Doação *",
                ["Alimentos", "Roupas", "Medicamentos", "Dinheiro", "Outros"]
            )
            
            descricao_item = st.text_input(
                "Descrição do Item *",
                placeholder="Ex: Arroz, Feijão, Cesta Básica..."
            )
        
        with col2:
            col2a, col2b = st.columns(2)
            
            with col2a:
                quantidade = st.number_input(
                    "Quantidade *",
                    min_value=1,
                    value=1,
                    step=1
                )
            
            with col2b:
                unidade = st.selectbox(
                    "Unidade *",
                    ["Kg", "Litros", "Unidades", "Caixas", "R$"]
                )
            
            ponto_selecionado = st.selectbox(
                "Ponto de Coleta *",
                options=[p['nome'] for p in pontos]
            )
            
            observacoes = st.text_area(
                "Observações",
                placeholder="Informações adicionais sobre a doação...",
                height=100
            )
        
        st.markdown("---")
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 4])
        
        with col_btn1:
            submit = st.form_submit_button("✅ Registrar Doação", use_container_width=True)
        
        with col_btn2:
            limpar = st.form_submit_button("🔄 Limpar", use_container_width=True)
        
        # Processar formulário
        if submit:
            if doador_selecionado and tipo_doacao and descricao_item and quantidade and unidade and ponto_selecionado:
                show_success_message(f"Doação de **{quantidade} {unidade}** de **{descricao_item}** registrada com sucesso!")
                show_success_message(f"Doador: **{doador_selecionado}** | Ponto: **{ponto_selecionado}**")
                st.balloons()
            else:
                show_error_message("Por favor, preencha todos os campos obrigatórios (*)")
        
        if limpar:
            st.rerun()
    
    st.markdown("---")
    
    # Informações rápidas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Doações Hoje", 8)
    
    with col2:
        st.metric("Doações esta Semana", 45)
    
    with col3:
        st.metric("Doações este Mês", 156)
    
    with col4:
        st.metric("Total de Doações", len(df_doacoes))

# ============================================================================
# ABA 2 - HISTÓRICO
# ============================================================================

with tab2:
    st.markdown("### Histórico de Doações")
    
    # Filtros
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
    
    with col1:
        data_inicio = st.date_input(
            "Data Início",
            value=datetime.now() - timedelta(days=30),
            max_value=datetime.now()
        )
    
    with col2:
        data_fim = st.date_input(
            "Data Fim",
            value=datetime.now(),
            max_value=datetime.now()
        )
    
    with col3:
        filtro_tipo = st.selectbox(
            "Tipo de Doação",
            ["Todos", "Alimentos", "Roupas", "Medicamentos", "Dinheiro", "Outros"]
        )
    
    with col4:
        st.write("")
        st.write("")
        buscar = st.button("🔍 Filtrar", use_container_width=True)
    
    st.markdown("---")
    
    # Filtrar dados
    df_filtrado = df_doacoes.copy()
    df_filtrado['data'] = pd.to_datetime(df_filtrado['data'])
    
    # Aplicar filtros de data
    df_filtrado = df_filtrado[
        (df_filtrado['data'] >= pd.to_datetime(data_inicio)) &
        (df_filtrado['data'] <= pd.to_datetime(data_fim))
    ]
    
    # Aplicar filtro de tipo
    if filtro_tipo != "Todos":
        df_filtrado = df_filtrado[df_filtrado['tipo'] == filtro_tipo]
    
    # Estatísticas do período
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total no Período", len(df_filtrado))
    
    with col2:
        # Contar doações de alimentos
        alimentos = len(df_filtrado[df_filtrado['tipo'] == 'Alimentos'])
        st.metric("Alimentos", alimentos)
    
    with col3:
        # Contar doações de roupas
        roupas = len(df_filtrado[df_filtrado['tipo'] == 'Roupas'])
        st.metric("Roupas", roupas)
    
    with col4:
        # Calcular total em dinheiro
        dinheiro = df_filtrado[
            (df_filtrado['tipo'] == 'Dinheiro') | (df_filtrado['unidade'] == 'R$')
        ]['quantidade'].sum()
        st.metric("Dinheiro", f"R$ {dinheiro:,.2f}")
    
    st.markdown("---")
    
    # Tabela de doações
    st.markdown("#### 📋 Listagem de Doações")
    
    # Preparar dados para exibição
    df_display = df_filtrado[['id', 'data', 'doador', 'tipo', 'item', 'quantidade', 'unidade', 'ponto_coleta', 'status']].copy()
    df_display.columns = ['ID', 'Data', 'Doador', 'Tipo', 'Item', 'Qtd', 'Un.', 'Ponto de Coleta', 'Status']
    
    # Formatar data
    df_display['Data'] = df_display['Data'].dt.strftime('%d/%m/%Y')
    
    # Ordenar por data (mais recentes primeiro)
    df_display = df_display.sort_values('Data', ascending=False)
    
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
            "Data": st.column_config.TextColumn(
                "Data",
                width="small",
            ),
            "Doador": st.column_config.TextColumn(
                "Doador",
                width="medium",
            ),
            "Tipo": st.column_config.TextColumn(
                "Tipo",
                width="small",
            ),
            "Item": st.column_config.TextColumn(
                "Item",
                width="medium",
            ),
            "Qtd": st.column_config.NumberColumn(
                "Qtd",
                width="small",
            ),
            "Un.": st.column_config.TextColumn(
                "Un.",
                width="small",
            ),
            "Ponto de Coleta": st.column_config.TextColumn(
                "Ponto de Coleta",
                width="medium",
            ),
            "Status": st.column_config.TextColumn(
                "Status",
                width="small",
            ),
        }
    )
    
    # Informação sobre resultados
    show_info_message(f"Exibindo {len(df_filtrado)} doações do período de {data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}")
    
    st.markdown("---")
    
    # Botões de exportação (simulados)
    col1, col2, col3 = st.columns([1, 1, 4])
    
    with col1:
        if st.button("📄 Exportar PDF", use_container_width=True):
            show_info_message("Funcionalidade de exportação será implementada em breve!", "🚧")
    
    with col2:
        if st.button("📊 Exportar Excel", use_container_width=True):
            show_info_message("Funcionalidade de exportação será implementada em breve!", "🚧")

st.markdown("---")

# ============================================================================
# INFORMAÇÕES ADICIONAIS
# ============================================================================

with st.expander("ℹ️ Informações sobre Registro de Doações"):
    st.markdown("""
    ### Como usar esta página:
    
    **Registrar Nova Doação:**
    1. Acesse a aba "Nova Doação"
    2. Preencha todos os campos obrigatórios (*)
    3. Clique em "Registrar Doação"
    4. O sistema confirmará o registro com sucesso
    
    **Campos Obrigatórios:**
    - Data da Doação
    - Doador (selecione da lista cadastrada)
    - Tipo de Doação
    - Descrição do Item
    - Quantidade
    - Unidade de Medida
    - Ponto de Coleta
    
    **Visualizar Histórico:**
    1. Acesse a aba "Histórico de Doações"
    2. Use os filtros de data e tipo para refinar a busca
    3. Clique em "Filtrar" para aplicar
    4. Visualize as estatísticas e a tabela detalhada
    
    **Tipos de Doação:**
    - **Alimentos:** Produtos alimentícios, cestas básicas
    - **Roupas:** Vestuário, calçados, roupas de cama
    - **Medicamentos:** Remédios, produtos de saúde
    - **Dinheiro:** Doações em espécie
    - **Outros:** Livros, brinquedos, materiais diversos
    
    **Status das Doações:**
    - **Recebida:** Doação recebida e aguardando triagem
    - **Em Triagem:** Sendo separada e classificada
    - **Distribuída:** Já foi entregue aos beneficiários
    
    > 💡 **Dica:** Registre as doações assim que forem recebidas para manter o controle atualizado!
    """)

# ============================================================================
# RODAPÉ
# ============================================================================

render_footer()
