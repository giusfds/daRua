"""
Modelo Doacao - Representa doações no sistema
VERSÃO CORRIGIDA - Remove completamente beneficiario_id (não existe na tabela!)
"""

from typing import Optional, List, Dict, Tuple
from datetime import date, datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import DatabaseConnection


class Doacao:
    """
    Representa uma doação no sistema.
    
    ESTRUTURA DA TABELA:
    - idDoacao (PK)
    - Doador_idDoador (FK - OBRIGATÓRIO)
    - PontoColeta_idPontoColeta (FK - OBRIGATÓRIO)
    - VoluntarioColeta_idVoluntario (FK - OBRIGATÓRIO)
    - CampanhaDoacao_idCampanhaDoacao (FK - OPCIONAL)
    - TipoDoacao, DescricaoItem, Quantidade, Unidade
    - DataCriacao, DataEntrega, Observacoes, Status
    
    IMPORTANTE: Beneficiário NÃO é coluna na tabela Doacao!
    O relacionamento é N:N através da tabela Recebe.
    Use o método distribuir() para associar beneficiários.
    
    STATUS AUTOMÁTICO:
    - "Recebida": sem beneficiários na tabela Recebe
    - "Distribuída": com beneficiários na tabela Recebe
    """
    
    def __init__(
        self,
        doador_id: int,
        data_criacao: Optional[date] = None,
        data_entrega: Optional[date] = None,
        tipo_doacao: str = "Outros",
        descricao_item: str = "Item não especificado",
        quantidade: float = 1.0,
        unidade: str = "Unidades",
        observacoes: Optional[str] = None,
        status: str = "Recebida",
        campanha_id: Optional[int] = None,
        ponto_coleta_id: Optional[int] = None,
        voluntario_coleta_id: Optional[int] = None,
        idDoacao: Optional[int] = None
    ):
        """
        Inicializa uma doação.
        
        Args:
            doador_id: ID do doador (OBRIGATÓRIO)
            ponto_coleta_id: ID do ponto de coleta (OBRIGATÓRIO)
            voluntario_coleta_id: ID do voluntário que registrou (OBRIGATÓRIO)
            campanha_id: ID da campanha (opcional)
            data_criacao: Data de registro (usa hoje se None)
            data_entrega: Data prevista/realizada de entrega
            tipo_doacao: Tipo do item (Alimentos, Roupas, etc)
            descricao_item: Descrição detalhada
            quantidade: Quantidade doada
            unidade: Unidade de medida (Kg, Litros, Unidades, etc)
            observacoes: Observações adicionais
            status: Status da doação (calculado automaticamente)
            idDoacao: ID da doação (None para nova doação)
        """
        self.idDoacao = idDoacao
        self.doador_id = doador_id
        self.campanha_id = campanha_id
        self.ponto_coleta_id = ponto_coleta_id
        self.voluntario_coleta_id = voluntario_coleta_id
        self.data_criacao = data_criacao or date.today()
        self.data_entrega = data_entrega
        self.tipo_doacao = tipo_doacao
        self.descricao_item = descricao_item
        self.quantidade = quantidade
        self.unidade = unidade
        self.observacoes = observacoes
        self.status = status
    
    def __repr__(self):
        return f"Doacao(id={self.idDoacao}, doador_id={self.doador_id}, tipo={self.tipo_doacao}, item={self.descricao_item})"
    
    def validate(self) -> tuple[bool, str]:
        """
        Valida os dados da doação antes de salvar.
        
        Returns:
            tuple[bool, str]: (é_válido, mensagem_erro)
        """
        # Validações de campos obrigatórios
        if not self.doador_id or self.doador_id <= 0:
            return False, "Doador é obrigatório e deve ser válido"
        
        if not self.ponto_coleta_id or self.ponto_coleta_id <= 0:
            return False, "Ponto de Coleta é obrigatório"
        
        if not self.voluntario_coleta_id or self.voluntario_coleta_id <= 0:
            return False, "Voluntário Responsável é obrigatório"
        
        if not self.descricao_item or not self.descricao_item.strip():
            return False, "Descrição do item é obrigatória"
        
        if self.quantidade <= 0:
            return False, "Quantidade deve ser maior que zero"
        
        # Validações de valores
        tipos_validos = ["Alimentos", "Roupas", "Medicamentos", "Dinheiro", "Outros"]
        if self.tipo_doacao not in tipos_validos:
            return False, f"Tipo de doação deve ser um de: {', '.join(tipos_validos)}"
        
        unidades_validas = ["Kg", "Litros", "Unidades", "Caixas", "R$"]
        if self.unidade not in unidades_validas:
            return False, f"Unidade deve ser uma de: {', '.join(unidades_validas)}"
        
        # Validação de datas
        if self.data_entrega and self.data_criacao:
            if self.data_entrega < self.data_criacao:
                return False, "Data de entrega não pode ser anterior à data de criação"
        
        return True, ""
    
    def save(self) -> bool:
        """
        Salva uma nova doação no banco de dados.
        
        IMPORTANTE: O status sempre começa como "Recebida".
        Use o método distribuir() para associar beneficiários e mudar o status.
        
        Returns:
            bool: True se salvou com sucesso, False caso contrário
        """
        valido, erro = self.validate()
        if not valido:
            print(f"✗ Validação falhou: {erro}")
            return False
        
        # SQL SEM Beneficiario_idBeneficiario (não existe!)
        query = """
            INSERT INTO Doacao (
                Doador_idDoador,
                CampanhaDoacao_idCampanhaDoacao, 
                PontoColeta_idPontoColeta,
                VoluntarioColeta_idVoluntario,
                DataCriacao, 
                DataEntrega,
                TipoDoacao, 
                DescricaoItem, 
                Quantidade, 
                Unidade, 
                Observacoes, 
                Status
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            self.doador_id,
            self.campanha_id,
            self.ponto_coleta_id,
            self.voluntario_coleta_id,
            self.data_criacao,
            self.data_entrega,
            self.tipo_doacao,
            self.descricao_item,
            self.quantidade,
            self.unidade,
            self.observacoes,
            "Recebida"  # Status inicial sempre "Recebida"
        )
        
        with DatabaseConnection() as db:
            if db.execute_query(query, params):
                self.idDoacao = db.get_last_insert_id()
                self.status = "Recebida"
                print(f"✓ Doação salva com sucesso! ID: {self.idDoacao}")
                return True
        
        print("✗ Erro ao salvar doação")
        return False
    
    def update(self) -> bool:
        """
        Atualiza uma doação existente no banco de dados.
        
        ATENÇÃO: Para mudar o status, use o método distribuir() ao invés
        de atualizar manualmente, pois o status é calculado automaticamente.
        
        Returns:
            bool: True se atualizou com sucesso, False caso contrário
        """
        if not self.idDoacao:
            print("✗ Doação não possui ID")
            return False
        
        valido, erro = self.validate()
        if not valido:
            print(f"✗ Validação falhou: {erro}")
            return False
        
        # SQL SEM Beneficiario_idBeneficiario (não existe!)
        query = """
            UPDATE Doacao SET
                Doador_idDoador = %s,
                CampanhaDoacao_idCampanhaDoacao = %s,
                PontoColeta_idPontoColeta = %s,
                VoluntarioColeta_idVoluntario = %s,
                DataCriacao = %s,
                DataEntrega = %s,
                TipoDoacao = %s,
                DescricaoItem = %s,
                Quantidade = %s,
                Unidade = %s,
                Observacoes = %s,
                Status = %s
            WHERE idDoacao = %s
        """
        params = (
            self.doador_id,
            self.campanha_id,
            self.ponto_coleta_id,
            self.voluntario_coleta_id,
            self.data_criacao,
            self.data_entrega,
            self.tipo_doacao,
            self.descricao_item,
            self.quantidade,
            self.unidade,
            self.observacoes,
            self.status,
            self.idDoacao
        )
        
        with DatabaseConnection() as db:
            if db.execute_query(query, params):
                print(f"✓ Doação {self.idDoacao} atualizada com sucesso!")
                return True
        
        print(f"✗ Erro ao atualizar doação {self.idDoacao}")
        return False
    
    def delete(self) -> bool:
        """
        Remove uma doação do banco de dados.
        
        ATENÇÃO: Isso também remove as associações com beneficiários
        e voluntários distribuidores (CASCADE).
        
        Returns:
            bool: True se deletou com sucesso, False caso contrário
        """
        if not self.idDoacao:
            print("✗ Doação não possui ID")
            return False
        
        query = "DELETE FROM Doacao WHERE idDoacao = %s"
        
        with DatabaseConnection() as db:
            if db.execute_query(query, (self.idDoacao,)):
                print(f"✓ Doação {self.idDoacao} removida com sucesso!")
                return True
        
        print(f"✗ Erro ao remover doação {self.idDoacao}")
        return False
    
    # ========================================================================
    # MÉTODOS DE DISTRIBUIÇÃO
    # ========================================================================
    
    @staticmethod
    def distribuir(
        doacao_id: int,
        beneficiarios_ids: List[int],
        voluntarios_ids: Optional[List[int]] = None,
        data_entrega: Optional[date] = None
    ) -> Tuple[bool, str]:
        """
        Distribui uma doação para beneficiários específicos.
        
        PROCESSO:
        1. Remove associações anteriores da tabela Recebe
        2. Remove associações anteriores da tabela Possui
        3. Adiciona novos beneficiários na tabela Recebe
        4. Adiciona voluntários distribuidores na tabela Possui
        5. Atualiza data de entrega
        6. Recalcula o status automaticamente
        
        Args:
            doacao_id: ID da doação
            beneficiarios_ids: Lista de IDs dos beneficiários
            voluntarios_ids: Lista de IDs dos voluntários distribuidores (opcional)
            data_entrega: Data da entrega (opcional)
            
        Returns:
            Tuple[bool, str]: (sucesso, mensagem)
        """
        if not beneficiarios_ids:
            return False, "❌ Selecione pelo menos um beneficiário!"
        
        with DatabaseConnection() as db:
            try:
                # Inicia transação
                db.connection.start_transaction()
                
                # 1 e 2. Remove associações anteriores
                db.execute_query(
                    "DELETE FROM Recebe WHERE Doacao_idDoacao = %s",
                    (doacao_id,)
                )
                db.execute_query(
                    "DELETE FROM Possui WHERE Doacao_idDoacao = %s",
                    (doacao_id,)
                )
                
                # 3. Adiciona novos beneficiários na tabela Recebe
                for beneficiario_id in beneficiarios_ids:
                    db.execute_query(
                        """
                        INSERT INTO Recebe (Beneficiario_idBeneficiario, Doacao_idDoacao)
                        VALUES (%s, %s)
                        """,
                        (beneficiario_id, doacao_id)
                    )
                
                # 4. Adiciona voluntários distribuidores na tabela Possui
                if voluntarios_ids:
                    for voluntario_id in voluntarios_ids:
                        db.execute_query(
                            """
                            INSERT INTO Possui (Doacao_idDoacao, Voluntario_idVoluntario)
                            VALUES (%s, %s)
                            """,
                            (doacao_id, voluntario_id)
                        )
                
                # 5. Atualiza data de entrega se fornecida
                if data_entrega:
                    db.execute_query(
                        "UPDATE Doacao SET DataEntrega = %s WHERE idDoacao = %s",
                        (data_entrega, doacao_id)
                    )
                
                # 6. Recalcula o status (agora será "Distribuída")
                Doacao.calcular_status(doacao_id, db)
                
                # Confirma transação
                db.connection.commit()
                
                qtd_beneficiarios = len(beneficiarios_ids)
                qtd_voluntarios = len(voluntarios_ids) if voluntarios_ids else 0
                
                return True, f"✅ Doação distribuída para {qtd_beneficiarios} beneficiário(s) por {qtd_voluntarios} voluntário(s)!"
                
            except Exception as e:
                # Desfaz tudo em caso de erro
                db.connection.rollback()
                return False, f"❌ Erro ao distribuir doação: {str(e)}"
    
    @staticmethod
    def calcular_status(doacao_id: int, db=None) -> bool:
        """
        Calcula e atualiza o status de uma doação automaticamente.
        
        REGRA:
        - Sem beneficiários na tabela Recebe → Status = "Recebida"
        - Com beneficiários na tabela Recebe → Status = "Distribuída"
        
        Args:
            doacao_id: ID da doação
            db: Conexão DatabaseConnection (opcional, para usar em transação)
            
        Returns:
            bool: True se atualizou com sucesso
        """
        usar_conexao_propria = db is None
        
        try:
            if usar_conexao_propria:
                db = DatabaseConnection()
                db.__enter__()
            
            # Conta quantos beneficiários estão associados na tabela Recebe
            result = db.fetch_one(
                "SELECT COUNT(*) as count FROM Recebe WHERE Doacao_idDoacao = %s",
                (doacao_id,)
            )
            
            count = result['count'] if result else 0
            
            # Define status baseado na contagem
            novo_status = "Distribuída" if count > 0 else "Recebida"
            
            # Atualiza o status
            db.execute_query(
                "UPDATE Doacao SET Status = %s WHERE idDoacao = %s",
                (novo_status, doacao_id)
            )
            
            if usar_conexao_propria:
                db.connection.commit()
            
            return True
            
        except Exception as e:
            if usar_conexao_propria and db:
                db.connection.rollback()
            print(f"❌ Erro ao calcular status: {e}")
            return False
        finally:
            if usar_conexao_propria and db:
                db.__exit__(None, None, None)
    
    @staticmethod
    def listar_beneficiarios(doacao_id: int) -> List[Dict]:
        """
        Lista todos os beneficiários de uma doação específica.
        
        Args:
            doacao_id: ID da doação
            
        Returns:
            Lista de dicionários com os dados dos beneficiários
        """
        query = """
            SELECT b.*
            FROM Beneficiario b
            INNER JOIN Recebe r ON b.idBeneficiario = r.Beneficiario_idBeneficiario
            WHERE r.Doacao_idDoacao = %s
            ORDER BY b.Nome
        """
        
        with DatabaseConnection() as db:
            return db.fetch_all(query, (doacao_id,))
    
    @staticmethod
    def listar_voluntarios_distribuidores(doacao_id: int) -> List[Dict]:
        """
        Lista todos os voluntários distribuidores de uma doação.
        
        Args:
            doacao_id: ID da doação
            
        Returns:
            Lista de dicionários com os dados dos voluntários
        """
        query = """
            SELECT v.*
            FROM Voluntario v
            INNER JOIN Possui p ON v.idVoluntario = p.Voluntario_idVoluntario
            WHERE p.Doacao_idDoacao = %s
            ORDER BY v.Nome
        """
        
        with DatabaseConnection() as db:
            return db.fetch_all(query, (doacao_id,))
    
    @staticmethod
    def listar_por_status(status: str) -> List['Doacao']:
        """
        Lista doações filtradas por status.
        
        Args:
            status: Status desejado ("Recebida" ou "Distribuída")
            
        Returns:
            Lista de objetos Doacao
        """
        query = "SELECT * FROM Doacao WHERE Status = %s ORDER BY DataCriacao DESC"
        
        with DatabaseConnection() as db:
            results = db.fetch_all(query, (status,))
            return [
                Doacao(
                    idDoacao=row['idDoacao'],
                    doador_id=row['Doador_idDoador'],
                    campanha_id=row.get('CampanhaDoacao_idCampanhaDoacao'),
                    ponto_coleta_id=row.get('PontoColeta_idPontoColeta'),
                    voluntario_coleta_id=row.get('VoluntarioColeta_idVoluntario'),
                    data_criacao=row['DataCriacao'],
                    data_entrega=row.get('DataEntrega'),
                    tipo_doacao=row.get('TipoDoacao', 'Outros'),
                    descricao_item=row.get('DescricaoItem', 'Item não especificado'),
                    quantidade=float(row.get('Quantidade', 1.0)),
                    unidade=row.get('Unidade', 'Unidades'),
                    observacoes=row.get('Observacoes'),
                    status=row.get('Status', 'Recebida')
                )
                for row in results
            ]
    
    @staticmethod
    def estatisticas_geral() -> Dict:
        """
        Retorna estatísticas gerais sobre as doações.
        
        Returns:
            Dicionário com estatísticas (total, recebidas, distribuídas, etc)
        """
        query = """
            SELECT 
                COUNT(*) AS total_doacoes,
                SUM(CASE WHEN Status = 'Recebida' THEN 1 ELSE 0 END) AS total_recebidas,
                SUM(CASE WHEN Status = 'Distribuída' THEN 1 ELSE 0 END) AS total_distribuidas,
                SUM(Quantidade) AS quantidade_total
            FROM Doacao
        """
        
        with DatabaseConnection() as db:
            result = db.fetch_one(query)
            return result if result else {}
    
    # ========================================================================
    # MÉTODOS ESTÁTICOS ORIGINAIS
    # ========================================================================
    
    @staticmethod
    def get_by_id(doacao_id: int) -> Optional['Doacao']:
        """Busca uma doação por ID"""
        query = "SELECT * FROM Doacao WHERE idDoacao = %s"
        
        with DatabaseConnection() as db:
            result = db.fetch_one(query, (doacao_id,))
            if result:
                return Doacao(
                    idDoacao=result['idDoacao'],
                    doador_id=result['Doador_idDoador'],
                    campanha_id=result.get('CampanhaDoacao_idCampanhaDoacao'),
                    ponto_coleta_id=result.get('PontoColeta_idPontoColeta'),
                    voluntario_coleta_id=result.get('VoluntarioColeta_idVoluntario'),
                    data_criacao=result['DataCriacao'],
                    data_entrega=result.get('DataEntrega'),
                    tipo_doacao=result.get('TipoDoacao', 'Outros'),
                    descricao_item=result.get('DescricaoItem', 'Item não especificado'),
                    quantidade=float(result.get('Quantidade', 1.0)),
                    unidade=result.get('Unidade', 'Unidades'),
                    observacoes=result.get('Observacoes'),
                    status=result.get('Status', 'Recebida')
                )
        return None
    
    @staticmethod
    def get_all() -> List['Doacao']:
        """Retorna todas as doações cadastradas"""
        query = "SELECT * FROM Doacao ORDER BY DataCriacao DESC"
        
        with DatabaseConnection() as db:
            results = db.fetch_all(query)
            return [
                Doacao(
                    idDoacao=row['idDoacao'],
                    doador_id=row['Doador_idDoador'],
                    campanha_id=row.get('CampanhaDoacao_idCampanhaDoacao'),
                    ponto_coleta_id=row.get('PontoColeta_idPontoColeta'),
                    voluntario_coleta_id=row.get('VoluntarioColeta_idVoluntario'),
                    data_criacao=row['DataCriacao'],
                    data_entrega=row.get('DataEntrega'),
                    tipo_doacao=row.get('TipoDoacao', 'Outros'),
                    descricao_item=row.get('DescricaoItem', 'Item não especificado'),
                    quantidade=float(row.get('Quantidade', 1.0)),
                    unidade=row.get('Unidade', 'Unidades'),
                    observacoes=row.get('Observacoes'),
                    status=row.get('Status', 'Recebida')
                )
                for row in results
            ]
    
    @staticmethod
    def get_by_doador(doador_id: int) -> List['Doacao']:
        """Busca todas as doações de um doador específico"""
        query = "SELECT * FROM Doacao WHERE Doador_idDoador = %s ORDER BY DataCriacao DESC"
        
        with DatabaseConnection() as db:
            results = db.fetch_all(query, (doador_id,))
            return [
                Doacao(
                    idDoacao=row['idDoacao'],
                    doador_id=row['Doador_idDoador'],
                    campanha_id=row.get('CampanhaDoacao_idCampanhaDoacao'),
                    ponto_coleta_id=row.get('PontoColeta_idPontoColeta'),
                    voluntario_coleta_id=row.get('VoluntarioColeta_idVoluntario'),
                    data_criacao=row['DataCriacao'],
                    data_entrega=row.get('DataEntrega'),
                    tipo_doacao=row.get('TipoDoacao', 'Outros'),
                    descricao_item=row.get('DescricaoItem', 'Item não especificado'),
                    quantidade=float(row.get('Quantidade', 1.0)),
                    unidade=row.get('Unidade', 'Unidades'),
                    observacoes=row.get('Observacoes'),
                    status=row.get('Status', 'Recebida')
                )
                for row in results
            ]
    
    @staticmethod
    def get_by_tipo(tipo_doacao: str) -> List['Doacao']:
        """Busca doações por tipo"""
        query = "SELECT * FROM Doacao WHERE TipoDoacao = %s ORDER BY DataCriacao DESC"
        
        with DatabaseConnection() as db:
            results = db.fetch_all(query, (tipo_doacao,))
            return [
                Doacao(
                    idDoacao=row['idDoacao'],
                    doador_id=row['Doador_idDoador'],
                    campanha_id=row.get('CampanhaDoacao_idCampanhaDoacao'),
                    ponto_coleta_id=row.get('PontoColeta_idPontoColeta'),
                    voluntario_coleta_id=row.get('VoluntarioColeta_idVoluntario'),
                    data_criacao=row['DataCriacao'],
                    data_entrega=row.get('DataEntrega'),
                    tipo_doacao=row.get('TipoDoacao', 'Outros'),
                    descricao_item=row.get('DescricaoItem', 'Item não especificado'),
                    quantidade=float(row.get('Quantidade', 1.0)),
                    unidade=row.get('Unidade', 'Unidades'),
                    observacoes=row.get('Observacoes'),
                    status=row.get('Status', 'Recebida')
                )
                for row in results
            ]
    
    def to_dict(self) -> Dict:
        """Converte a doação para dicionário"""
        return {
            'idDoacao': self.idDoacao,
            'doador_id': self.doador_id,
            'campanha_id': self.campanha_id,
            'ponto_coleta_id': self.ponto_coleta_id,
            'voluntario_coleta_id': self.voluntario_coleta_id,
            'data_criacao': str(self.data_criacao) if self.data_criacao else None,
            'data_entrega': str(self.data_entrega) if self.data_entrega else None,
            'tipo_doacao': self.tipo_doacao,
            'descricao_item': self.descricao_item,
            'quantidade': self.quantidade,
            'unidade': self.unidade,
            'observacoes': self.observacoes,
            'status': self.status
        }


if __name__ == "__main__":
    print("\n=== TESTE MODELO DOACAO CORRIGIDO ===\n")
    
    # Criar doação de teste
    doacao = Doacao(
        doador_id=1,
        ponto_coleta_id=1,
        voluntario_coleta_id=1,
        tipo_doacao="Alimentos",
        descricao_item="Arroz integral - 5kg",
        quantidade=5.0,
        unidade="Kg",
        observacoes="Doação em bom estado",
        status="Recebida"
    )
    
    print(f"Doação criada: {doacao}")
    print(f"Dicionário: {doacao.to_dict()}")
    
    # Testar validação
    valido, erro = doacao.validate()
    print(f"\nValidação: {'✓ Válido' if valido else f'✗ {erro}'}")