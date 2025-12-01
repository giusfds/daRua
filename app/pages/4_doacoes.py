"""
Página de Registro e Gerenciamento de Doações
VERSÃO ATUALIZADA - Registra, distribui e visualiza doações
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path
from datetime import datetime, timedelta, date

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

# Importar modelos do backend
from models.doacao import Doacao
from models.doador import Doador
from models.ponto_coleta import PontoColeta
from models.campanha_doacao import CampanhaDoacao
from models.beneficiario import Beneficiario
from models.voluntario import Voluntario

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

st.title("📦 Gestão de Doações")
st.markdown("Registre, distribua e acompanhe doações")
st.markdown("---")

# ============================================================================
# CARREGAR DADOS DO BANCO
# ============================================================================

# Carregar doadores
try:
    doadores_list = Doador.get_all()
    doadores = [{'id': d.idDoador, 'nome': d.nome} for d in doadores_list] if doadores_list else []
except Exception as e:
    doadores = []
    show_error_message(f"Erro ao carregar doadores: {str(e)}")

# Carregar pontos de coleta
try:
    pontos_list = PontoColeta.get_all()
    pontos = [{'id': p.idPontoColeta, 'nome': p.responsavel, 'cidade': getattr(p, 'cidade', '')} for p in pontos_list] if pontos_list else []
except Exception as e:
    pontos = []
    show_error_message(f"Erro ao carregar pontos de coleta: {str(e)}")

# Carregar voluntários
try:
    voluntarios_list = Voluntario.get_all()
    voluntarios = [{'id': v.idVoluntario, 'nome': v.nome} for v in voluntarios_list] if voluntarios_list else []
except Exception as e:
    voluntarios = []
    show_error_message(f"Erro ao carregar voluntários: {str(e)}")

# Carregar campanhas
try:
    campanhas_list = CampanhaDoacao.get_all()
    campanhas = [{'id': c.idCampanhaDoacao, 'nome': c.nome} for c in campanhas_list] if campanhas_list else []
except Exception as e:
    campanhas = []

# Carregar beneficiários
try:
    beneficiarios_list = Beneficiario.get_all()
    beneficiarios = [{'id': b.idBeneficiario, 'nome': b.nome} for b in beneficiarios_list] if beneficiarios_list else []
except Exception as e:
    beneficiarios = []

# ============================================================================
# ABAS
# ============================================================================

tab1, tab2, tab3 = st.tabs(["📝 Nova Doação", "📤 Distribuir Doação", "📋 Histórico"])

# ============================================================================
# ABA 1 - NOVA DOAÇÃO
# ============================================================================

with tab1:
    st.markdown("### Registrar Nova Doação")
    st.info("💡 **Como funciona:** O doador entrega os itens no ponto de coleta. Um voluntário recebe e registra a doação no sistema com status 'Recebida'. Depois, você pode distribuir para beneficiários na aba 'Distribuir Doação'.")
    
    if not doadores:
        show_warning_message("Nenhum doador cadastrado! Cadastre doadores antes de registrar doações.")
        if st.button("➕ Ir para Doadores"):
            st.switch_page("pages/2_doadores.py")
        st.stop()
    
    if not pontos:
        show_warning_message("Nenhum ponto de coleta cadastrado! Cadastre um ponto primeiro.")
        if st.button("➕ Ir para Pontos de Coleta"):
            st.switch_page("pages/6_pontos_coleta.py")
        st.stop()
    
    if not voluntarios:
        show_warning_message("Nenhum voluntário cadastrado! Cadastre um voluntário primeiro.")
        if st.button("➕ Ir para Voluntários"):
            st.switch_page("pages/7_voluntarios.py")
        st.stop()
    
    with st.form("form_nova_doacao"):
        st.markdown("#### 📋 Identificação (Obrigatório)")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            doador_sel = st.selectbox(
                "Doador *",
                options=[f"{d['id']} - {d['nome']}" for d in doadores],
                help="Quem está doando"
            )
            doador_id = int(doador_sel.split(" - ")[0])
        
        with col2:
            ponto_sel = st.selectbox(
                "Ponto de Coleta *",
                options=[f"{p['id']} - {p['nome']} ({p['cidade']})" for p in pontos],
                help="Onde a doação foi recebida"
            )
            ponto_id = int(ponto_sel.split(" - ")[0])
        
        with col3:
            voluntario_sel = st.selectbox(
                "Voluntário Responsável *",
                options=[f"{v['id']} - {v['nome']}" for v in voluntarios],
                help="Quem está registrando"
            )
            voluntario_id = int(voluntario_sel.split(" - ")[0])
        
        st.markdown("---")
        st.markdown("#### 📦 Detalhes da Doação")
        
        col1, col2 = st.columns(2)
        
        with col1:
            tipo_doacao = st.selectbox(
                "Tipo de Doação *",
                ["Alimentos", "Roupas", "Medicamentos", "Dinheiro", "Outros"],
                help="Categoria da doação"
            )
            
            descricao_item = st.text_input(
                "Descrição do Item *",
                placeholder="Ex: Arroz integral, Feijão preto, Cesta básica...",
                help="Descreva o item doado"
            )
            
            quantidade = st.number_input(
                "Quantidade *",
                min_value=0.01,
                value=1.0,
                step=0.1,
                help="Quantidade doada"
            )
        
        with col2:
            unidade = st.selectbox(
                "Unidade *",
                ["Unidades", "Kg", "Litros", "Caixas", "R$"],
                help="Unidade de medida"
            )
            
            data_entrega = st.date_input(
                "Data Prevista de Entrega (Opcional)",
                value=None,
                min_value=date.today(),
                help="Quando planeja distribuir (deixe vazio se não souber)"
            )
        
        st.markdown("---")
        st.markdown("#### 🎯 Informações Adicionais (Opcional)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if campanhas:
                campanha_sel = st.selectbox(
                    "Campanha (Opcional)",
                    options=["Sem campanha"] + [f"{c['id']} - {c['nome']}" for c in campanhas],
                    help="Vincule a uma campanha específica"
                )
                campanha_id = None if campanha_sel == "Sem campanha" else int(campanha_sel.split(" - ")[0])
            else:
                st.info("ℹ️ Nenhuma campanha cadastrada")
                campanha_id = None
        
        with col2:
            observacoes = st.text_area(
                "Observações",
                placeholder="Informações adicionais sobre a doação...",
                help="Campo livre para anotações",
                height=100
            )
        
        st.markdown("---")
        
        submitted = st.form_submit_button("💾 Registrar Doação", use_container_width=True, type="primary")
    
    if submitted:
        if not descricao_item or descricao_item.strip() == "":
            show_error_message("Preencha a descrição do item!")
        else:
            doacao = Doacao(
                doador_id=doador_id,
                ponto_coleta_id=ponto_id,
                voluntario_coleta_id=voluntario_id,
                tipo_doacao=tipo_doacao,
                descricao_item=descricao_item,
                quantidade=quantidade,
                unidade=unidade,
                campanha_id=campanha_id,
                observacoes=observacoes if observacoes else None,
                data_entrega=data_entrega if data_entrega else None
            )
            
            if doacao.save():
                show_success_message(f"Doação #{doacao.idDoacao} registrada com sucesso!")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("ID", f"#{doacao.idDoacao}")
                with col2:
                    st.metric("Status", "🟢 Recebida")
                with col3:
                    st.metric("Quantidade", f"{quantidade} {unidade}")
                
                st.markdown("---")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📤 Distribuir Agora", use_container_width=True):
                        st.session_state['doacao_para_distribuir'] = doacao.idDoacao
                        st.rerun()
                with col2:
                    if st.button("➕ Registrar Outra", use_container_width=True):
                        st.rerun()
            else:
                show_error_message("Erro ao registrar doação!")

# ============================================================================
# ABA 2 - DISTRIBUIR DOAÇÃO
# ============================================================================

with tab2:
    st.markdown("### 📤 Distribuir Doação para Beneficiários")
    st.info("💡 **Como funciona:** Selecione uma doação 'Recebida', escolha os beneficiários que receberão, selecione os voluntários que farão a entrega e confirme. O status mudará automaticamente para 'Distribuída'.")
    
    # Carregar doações recebidas
    try:
        doacoes_recebidas = Doacao.listar_por_status("Recebida")
    except:
        doacoes_recebidas = []
    
    if not doacoes_recebidas:
        show_warning_message("Não há doações aguardando distribuição!")
        if st.button("➕ Registrar Nova Doação"):
            st.switch_page("pages/4_doacoes.py")
        st.stop()
    
    if not beneficiarios:
        show_warning_message("Nenhum beneficiário cadastrado! Cadastre beneficiários primeiro.")
        if st.button("➕ Ir para Beneficiários"):
            st.switch_page("pages/3_beneficiarios.py")
        st.stop()
    
    # Verificar se há doação pré-selecionada
    doacao_pre_sel = st.session_state.get('doacao_para_distribuir', None)
    index_padrao = 0
    
    # Criar opções de doações
    doacoes_options = []
    for idx, d in enumerate(doacoes_recebidas):
        try:
            doador = Doador.get_by_id(d.doador_id)
            doador_nome = doador.nome if doador else "Desconhecido"
        except:
            doador_nome = "Desconhecido"
        
        opcao = f"#{d.idDoacao} - {d.tipo_doacao} ({d.quantidade} {d.unidade}) - {doador_nome}"
        doacoes_options.append(opcao)
        
        if doacao_pre_sel and d.idDoacao == doacao_pre_sel:
            index_padrao = idx
    
    # Limpar sessão
    if doacao_pre_sel:
        del st.session_state['doacao_para_distribuir']
    
    # Selecionar doação
    doacao_sel = st.selectbox(
        "Selecione a doação:",
        options=doacoes_options,
        index=index_padrao,
        help="Escolha a doação que será distribuída"
    )
    
    doacao_id = int(doacao_sel.split(" - ")[0].replace("#", ""))
    doacao_atual = next((d for d in doacoes_recebidas if d.idDoacao == doacao_id), None)
    
    if doacao_atual:
        # Mostrar detalhes
        with st.expander("🔍 Detalhes da Doação", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**📋 Geral**")
                st.write(f"**ID:** #{doacao_atual.idDoacao}")
                st.write(f"**Tipo:** {doacao_atual.tipo_doacao}")
                st.write(f"**Qtd:** {doacao_atual.quantidade} {doacao_atual.unidade}")
            
            with col2:
                st.markdown("**👤 Doador**")
                try:
                    doador = Doador.get_by_id(doacao_atual.doador_id)
                    st.write(f"**Nome:** {doador.nome if doador else 'N/A'}")
                except:
                    st.write("**Nome:** N/A")
            
            with col3:
                st.markdown("**📍 Coleta**")
                try:
                    ponto = PontoColeta.get_by_id(doacao_atual.ponto_coleta_id)
                    st.write(f"**Ponto:** {ponto.responsavel if ponto else 'N/A'}")
                except:
                    st.write("**Ponto:** N/A")
            
            if doacao_atual.descricao_item:
                st.markdown(f"**📝 Descrição:** {doacao_atual.descricao_item}")
        
        st.markdown("---")
        
        # Formulário de distribuição
        with st.form("form_distribuir"):
            st.markdown("#### 👥 Beneficiários")
            st.caption("Selecione um ou mais beneficiários")
            
            beneficiarios_selecionados = []
            cols = st.columns(3)
            
            for idx, benef in enumerate(beneficiarios):
                col_idx = idx % 3
                with cols[col_idx]:
                    if st.checkbox(benef['nome'], key=f"benef_{benef['id']}"):
                        beneficiarios_selecionados.append(benef['id'])
            
            if beneficiarios_selecionados:
                st.success(f"✅ {len(beneficiarios_selecionados)} beneficiário(s) selecionado(s)")
            else:
                st.warning("⚠️ Selecione pelo menos um beneficiário")
            
            st.markdown("---")
            st.markdown("#### 🙋 Voluntários Distribuidores (Opcional)")
            st.caption("Selecione quem fará a entrega")
            
            voluntarios_selecionados = []
            if voluntarios:
                cols = st.columns(3)
                
                for idx, vol in enumerate(voluntarios):
                    col_idx = idx % 3
                    with cols[col_idx]:
                        if st.checkbox(vol['nome'], key=f"vol_{vol['id']}"):
                            voluntarios_selecionados.append(vol['id'])
                
                if voluntarios_selecionados:
                    st.success(f"✅ {len(voluntarios_selecionados)} voluntário(s) selecionado(s)")
            
            st.markdown("---")
            st.markdown("#### 📅 Data de Entrega")
            
            data_entrega_dist = st.date_input(
                "Quando será entregue?",
                value=date.today(),
                min_value=date.today()
            )
            
            st.markdown("---")
            
            confirmar = st.form_submit_button("✅ Confirmar Distribuição", use_container_width=True, type="primary")
        
        if confirmar:
            if not beneficiarios_selecionados:
                show_error_message("Selecione pelo menos um beneficiário!")
            else:
                sucesso, msg = Doacao.distribuir(
                    doacao_id=doacao_id,
                    beneficiarios_ids=beneficiarios_selecionados,
                    voluntarios_ids=voluntarios_selecionados if voluntarios_selecionados else None,
                    data_entrega=data_entrega_dist
                )
                
                if sucesso:
                    show_success_message(msg)
                    st.balloons()
                    
                    if st.button("📤 Distribuir Outra"):
                        st.rerun()
                else:
                    show_error_message(msg)

# ============================================================================
# ABA 3 - HISTÓRICO
# ============================================================================

with tab3:
    st.markdown("### 📋 Histórico de Doações")
    
    # Carregar doações
    try:
        doacoes_list = Doacao.get_all()
        if doacoes_list:
            doacoes_data = []
            for d in doacoes_list:
                doacao_dict = d.to_dict()
                
                # Buscar nomes
                try:
                    doador = Doador.get_by_id(d.doador_id)
                    doacao_dict['doador_nome'] = doador.nome if doador else 'Desconhecido'
                except:
                    doacao_dict['doador_nome'] = 'Desconhecido'
                
                doacoes_data.append(doacao_dict)
            
            df_doacoes = pd.DataFrame(doacoes_data)
        else:
            df_doacoes = pd.DataFrame()
    except Exception as e:
        show_error_message(f"Erro ao carregar doações: {str(e)}")
        df_doacoes = pd.DataFrame()
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filtro_tipo = st.selectbox(
            "Tipo",
            ["Todos", "Alimentos", "Roupas", "Medicamentos", "Dinheiro", "Outros"]
        )
    
    with col2:
        filtro_status = st.selectbox(
            "Status",
            ["Todos", "Recebida", "Distribuída"]
        )
    
    with col3:
        st.write("")
        st.write("")
        if st.button("🔍 Filtrar", use_container_width=True):
            pass
    
    # Estatísticas
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    try:
        stats = Doacao.estatisticas_geral()
        
        with col1:
            st.metric("📦 Total", stats.get('total_doacoes', 0))
        
        with col2:
            st.metric("🟢 Recebidas", stats.get('total_recebidas', 0))
        
        with col3:
            st.metric("🔴 Distribuídas", stats.get('total_distribuidas', 0))
        
        with col4:
            st.metric("📊 Quantidade", f"{stats.get('quantidade_total', 0) or 0:.1f}")
    except:
        pass
    
    st.markdown("---")
    
    # Tabela
    if not df_doacoes.empty:
        try:
            # Filtrar
            df_filtrado = df_doacoes.copy()
            
            if filtro_tipo != "Todos":
                df_filtrado = df_filtrado[df_filtrado['tipo_doacao'] == filtro_tipo]
            
            if filtro_status != "Todos":
                df_filtrado = df_filtrado[df_filtrado['status'] == filtro_status]
            
            # Preparar para exibição
            df_display = df_filtrado[[
                'idDoacao', 'data_criacao', 'doador_nome', 'tipo_doacao',
                'descricao_item', 'quantidade', 'unidade', 'status'
            ]].copy()
            
            df_display.columns = ['ID', 'Data', 'Doador', 'Tipo', 'Item', 'Qtd', 'Un.', 'Status']
            df_display['Data'] = pd.to_datetime(df_display['Data']).dt.strftime('%d/%m/%Y')
            df_display = df_display.sort_values('ID', ascending=False)
            
            st.dataframe(df_display, use_container_width=True, hide_index=True)
            
            show_info_message(f"Exibindo {len(df_filtrado)} doações")
        except Exception as e:
            show_error_message(f"Erro ao exibir tabela: {str(e)}")
    else:
        show_info_message("Nenhuma doação cadastrada")

st.markdown("---")

# ============================================================================
# RODAPÉ
# ============================================================================

render_footer()