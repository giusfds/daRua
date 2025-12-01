"""
Modelo Dashboard - Métricas e estatísticas para o dashboard principal
Segue o mesmo padrão dos outros models do projeto
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import DatabaseConnection
from typing import Dict, List, Any


class DashboardModel:
    """Modelo para buscar dados agregados do dashboard"""
    
    @staticmethod
    def get_metricas() -> Dict[str, Any]:
        """
        Função principal que retorna TODAS as métricas do dashboard.
        
        Retorna um dicionário com:
        - total_doadores: quantidade de doadores
        - total_beneficiarios: quantidade de beneficiários
        - total_doacoes: quantidade de doações
        - campanhas_ativas: quantidade de campanhas ativas
        - doacoes_por_categoria: dict com categorias e quantidades
        - doacoes_mensais: dict com meses e quantidades (últimos 6)
        - doadores_mensais: dict com meses e novos doadores (últimos 6)
        - ultimas_doacoes: lista com últimas 10 doações
        """
        return {
            'total_doadores': DashboardModel._get_total_doadores(),
            'total_beneficiarios': DashboardModel._get_total_beneficiarios(),
            'total_doacoes': DashboardModel._get_total_doacoes(),
            'campanhas_ativas': DashboardModel._get_campanhas_ativas(),
            'doacoes_por_categoria': DashboardModel._get_doacoes_por_categoria(),
            'doacoes_mensais': DashboardModel._get_doacoes_mensais(),
            'doadores_mensais': DashboardModel._get_doadores_mensais(),
            'ultimas_doacoes': DashboardModel._get_ultimas_doacoes()
        }
    
    @staticmethod
    def _get_total_doadores() -> int:
        """Conta total de doadores"""
        query = "SELECT COUNT(*) as total FROM Doador"
        with DatabaseConnection() as db:
            result = db.fetch_one(query)
            return result['total'] if result else 0
    
    @staticmethod
    def _get_total_beneficiarios() -> int:
        """Conta total de beneficiários"""
        query = "SELECT COUNT(*) as total FROM Beneficiario"
        with DatabaseConnection() as db:
            result = db.fetch_one(query)
            return result['total'] if result else 0
    
    @staticmethod
    def _get_total_doacoes() -> int:
        """Conta total de doações"""
        query = "SELECT COUNT(*) as total FROM Doacao"
        with DatabaseConnection() as db:
            result = db.fetch_one(query)
            return result['total'] if result else 0
    
    @staticmethod
    def _get_campanhas_ativas() -> int:
        """Conta campanhas ativas (sem data término ou futuras)"""
        query = """
            SELECT COUNT(*) as total 
            FROM CampanhaDoacao 
            WHERE DataTermino IS NULL OR DataTermino >= CURDATE()
        """
        with DatabaseConnection() as db:
            result = db.fetch_one(query)
            return result['total'] if result else 0
    
    @staticmethod
    def _get_doacoes_por_categoria() -> Dict[str, int]:
        """
        Agrupa doações por TipoDoacao.
        
        NOTA: Seu schema original não tem coluna TipoDoacao na tabela Doacao.
        Você precisa rodar a migration add_doacoes_detalhes.sql primeiro!
        
        Se a coluna não existir, retorna dict vazio.
        """
        query = """
            SELECT TipoDoacao, COUNT(*) as total
            FROM Doacao
            GROUP BY TipoDoacao
            ORDER BY total DESC
        """
        try:
            with DatabaseConnection() as db:
                results = db.fetch_all(query)
                return {row['TipoDoacao']: row['total'] for row in results}
        except Exception as e:
            print(f"⚠️ Erro ao buscar por categoria (rode add_doacoes_detalhes.sql): {e}")
            return {}
    
    @staticmethod
    def _get_doacoes_mensais() -> Dict[str, int]:
        """Doações dos últimos 6 meses, agrupadas por mês"""
        query = """
            SELECT 
                DATE_FORMAT(DataCriacao, '%Y-%m') as mes,
                COUNT(*) as total
            FROM Doacao
            WHERE DataCriacao >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
            GROUP BY mes
            ORDER BY mes ASC
        """
        with DatabaseConnection() as db:
            results = db.fetch_all(query)
            return {row['mes']: row['total'] for row in results}
    
    @staticmethod
    def _get_doadores_mensais() -> Dict[str, int]:
        """
        Novos doadores por mês (baseado na primeira doação).
        
        Como não há DataCadastro em Doador, usamos a primeira doação
        de cada doador para contar "novos doadores" por mês.
        """
        query = """
            SELECT 
                DATE_FORMAT(MIN(d.DataCriacao), '%Y-%m') as mes,
                COUNT(DISTINCT d.Doador_idDoador) as total_doadores
            FROM Doacao d
            WHERE d.DataCriacao >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
            GROUP BY d.Doador_idDoador
        """
        with DatabaseConnection() as db:
            results = db.fetch_all(query)
            
            # Agrupar por mês (vários doadores podem ter 1ª doação no mesmo mês)
            meses_dict = {}
            for row in results:
                mes = row['mes']
                meses_dict[mes] = meses_dict.get(mes, 0) + 1
            
            return meses_dict
    
    @staticmethod
    def _get_ultimas_doacoes() -> List[Dict[str, Any]]:
        """
        Últimas 10 doações com nome do doador.
        
        Campos retornados:
        - data: DataCriacao
        - doador: Nome do doador
        - item: DescricaoItem (se coluna existir)
        - quantidade: Quantidade (se coluna existir)
        - unidade: Unidade (se coluna existir)
        - status: Status (se coluna existir)
        """
        # Versão SEM as colunas adicionais (schema original)
        query_basica = """
            SELECT 
                d.DataCriacao as data,
                doador.Nome as doador,
                'Item não especificado' as item,
                1 as quantidade,
                'Unidades' as unidade,
                'Recebida' as status
            FROM Doacao d
            INNER JOIN Doador doador ON d.Doador_idDoador = doador.idDoador
            ORDER BY d.DataCriacao DESC
            LIMIT 10
        """
        
        # Versão COM as colunas adicionais (após migration)
        query_completa = """
            SELECT 
                d.DataCriacao as data,
                doador.Nome as doador,
                COALESCE(d.DescricaoItem, 'Item não especificado') as item,
                COALESCE(d.Quantidade, 1) as quantidade,
                COALESCE(d.Unidade, 'Unidades') as unidade,
                COALESCE(d.Status, 'Recebida') as status
            FROM Doacao d
            INNER JOIN Doador doador ON d.Doador_idDoador = doador.idDoador
            ORDER BY d.DataCriacao DESC
            LIMIT 10
        """
        
        with DatabaseConnection() as db:
            try:
                # Tenta query completa primeiro
                results = db.fetch_all(query_completa)
            except Exception as e:
                print(f"⚠️ Usando query básica (rode add_doacoes_detalhes.sql para mais dados)")
                results = db.fetch_all(query_basica)
            
            # Converter datas para string
            for row in results:
                if row.get('data'):
                    row['data'] = str(row['data'])
            
            return results


# Função de compatibilidade com seu main.py atual
def get_metricas_dashboard() -> Dict[str, Any]:
    """
    Função wrapper para manter compatibilidade com seu código atual.
    Seu main.py chama: metricas = get_metricas_dashboard()
    """
    return DashboardModel.get_metricas()


if __name__ == "__main__":
    print("\n=== TESTE MODELO DASHBOARD ===\n")
    
    metricas = get_metricas_dashboard()
    
    print(f"Total de Doadores: {metricas['total_doadores']}")
    print(f"Total de Beneficiários: {metricas['total_beneficiarios']}")
    print(f"Total de Doações: {metricas['total_doacoes']}")
    print(f"Campanhas Ativas: {metricas['campanhas_ativas']}")
    
    print("\n📊 Doações por Categoria:")
    print(metricas['doacoes_por_categoria'])
    
    print("\n📅 Doações Mensais:")
    print(metricas['doacoes_mensais'])
    
    print("\n👥 Doadores Mensais:")
    print(metricas['doadores_mensais'])
    
    print("\n📋 Últimas Doações:")
    for d in metricas['ultimas_doacoes'][:3]:
        print(f"  {d['data']} - {d['doador']}: {d['item']}")
    
    print("\n✅ Teste concluído!")