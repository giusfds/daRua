"""
Modelo Doacao - Registro de doações realizadas
"""

from typing import Optional, List, Dict
from datetime import date
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import DatabaseConnection


class Doacao:
    """Representa uma doação no sistema"""
    
    def __init__(self, doador_id: int, data_criacao: Optional[date] = None,
                 data_entrega: Optional[date] = None, campanha_id: Optional[int] = None,
                 idDoacao: Optional[int] = None):
        self.idDoacao = idDoacao
        self.data_criacao = data_criacao or date.today()
        self.data_entrega = data_entrega
        self.doador_id = doador_id
        self.campanha_id = campanha_id
    
    def __repr__(self):
        return f"Doacao(id={self.idDoacao}, doador_id={self.doador_id})"
    
    def validate(self) -> tuple[bool, str]:
        """Valida dados da doação"""
        if not self.doador_id:
            return False, "Doador é obrigatório"
        if self.data_entrega and self.data_criacao:
            if self.data_entrega < self.data_criacao:
                return False, "Data de entrega não pode ser antes da criação"
        return True, ""
    
    def save(self) -> bool:
        """Salva nova doação"""
        valido, erro = self.validate()
        if not valido:
            print(f"✗ Validação falhou: {erro}")
            return False
        
        query = """
            INSERT INTO Doacao (DataCriacao, DataEntrega, Doador_idDoador, 
                               CampanhaDoacao_idCampanhaDoacao)
            VALUES (%s, %s, %s, %s)
        """
        params = (self.data_criacao, self.data_entrega, self.doador_id, self.campanha_id)
        
        with DatabaseConnection() as db:
            if db.execute_query(query, params):
                self.idDoacao = db.get_last_insert_id()
                return True
        return False
    
    def update(self) -> bool:
        """Atualiza doação existente"""
        if not self.idDoacao:
            print("✗ Doação não possui ID")
            return False
        
        valido, erro = self.validate()
        if not valido:
            print(f"✗ Validação falhou: {erro}")
            return False
        
        query = """
            UPDATE Doacao SET DataCriacao = %s, DataEntrega = %s, 
                             Doador_idDoador = %s, CampanhaDoacao_idCampanhaDoacao = %s
            WHERE idDoacao = %s
        """
        params = (self.data_criacao, self.data_entrega, self.doador_id, 
                 self.campanha_id, self.idDoacao)
        
        with DatabaseConnection() as db:
            return db.execute_query(query, params)
    
    def delete(self) -> bool:
        """Remove doação"""
        if not self.idDoacao:
            print("✗ Doação não possui ID")
            return False
        
        query = "DELETE FROM Doacao WHERE idDoacao = %s"
        with DatabaseConnection() as db:
            return db.execute_query(query, (self.idDoacao,))
    
    @staticmethod
    def get_by_id(doacao_id: int) -> Optional['Doacao']:
        """Busca doação por ID"""
        query = "SELECT * FROM Doacao WHERE idDoacao = %s"
        with DatabaseConnection() as db:
            result = db.fetch_one(query, (doacao_id,))
            if result:
                return Doacao(
                    idDoacao=result['idDoacao'],
                    data_criacao=result['DataCriacao'],
                    data_entrega=result['DataEntrega'],
                    doador_id=result['Doador_idDoador'],
                    campanha_id=result['CampanhaDoacao_idCampanhaDoacao']
                )
        return None
    
    @staticmethod
    def get_all() -> List['Doacao']:
        """Retorna todas as doações"""
        query = "SELECT * FROM Doacao ORDER BY DataCriacao DESC"
        with DatabaseConnection() as db:
            results = db.fetch_all(query)
            return [
                Doacao(
                    idDoacao=row['idDoacao'],
                    data_criacao=row['DataCriacao'],
                    data_entrega=row['DataEntrega'],
                    doador_id=row['Doador_idDoador'],
                    campanha_id=row['CampanhaDoacao_idCampanhaDoacao']
                )
                for row in results
            ]
    
    # Métodos para relacionamentos N:N
    
    def adicionar_objeto(self, objeto_id: int) -> bool:
        """Adiciona um objeto à doação"""
        if not self.idDoacao:
            print("✗ Doação não possui ID")
            return False
        
        query = "INSERT INTO Contem (Doacao_idDoacao, ObjetoDoavel_idObjetoDoavel) VALUES (%s, %s)"
        with DatabaseConnection() as db:
            return db.execute_query(query, (self.idDoacao, objeto_id))
    
    def adicionar_beneficiario(self, beneficiario_id: int) -> bool:
        """Adiciona um beneficiário à doação"""
        if not self.idDoacao:
            print("✗ Doação não possui ID")
            return False
        
        query = "INSERT INTO Recebe (Beneficiario_idBeneficiario, Doacao_idDoacao) VALUES (%s, %s)"
        with DatabaseConnection() as db:
            return db.execute_query(query, (beneficiario_id, self.idDoacao))
    
    def adicionar_voluntario(self, voluntario_id: int) -> bool:
        """Adiciona um voluntário à doação"""
        if not self.idDoacao:
            print("✗ Doação não possui ID")
            return False
        
        query = "INSERT INTO Possui (Doacao_idDoacao, Voluntario_idVoluntario) VALUES (%s, %s)"
        with DatabaseConnection() as db:
            return db.execute_query(query, (self.idDoacao, voluntario_id))
    
    def get_objetos(self) -> List[Dict]:
        """Retorna objetos da doação"""
        if not self.idDoacao:
            return []
        
        query = """
            SELECT o.* FROM ObjetoDoavel o
            INNER JOIN Contem c ON o.idObjetoDoavel = c.ObjetoDoavel_idObjetoDoavel
            WHERE c.Doacao_idDoacao = %s
        """
        with DatabaseConnection() as db:
            return db.fetch_all(query, (self.idDoacao,))
    
    def get_beneficiarios(self) -> List[Dict]:
        """Retorna beneficiários da doação"""
        if not self.idDoacao:
            return []
        
        query = """
            SELECT b.* FROM Beneficiario b
            INNER JOIN Recebe r ON b.idBeneficiario = r.Beneficiario_idBeneficiario
            WHERE r.Doacao_idDoacao = %s
        """
        with DatabaseConnection() as db:
            return db.fetch_all(query, (self.idDoacao,))
    
    def get_voluntarios(self) -> List[Dict]:
        """Retorna voluntários da doação"""
        if not self.idDoacao:
            return []
        
        query = """
            SELECT v.* FROM Voluntario v
            INNER JOIN Possui p ON v.idVoluntario = p.Voluntario_idVoluntario
            WHERE p.Doacao_idDoacao = %s
        """
        with DatabaseConnection() as db:
            return db.fetch_all(query, (self.idDoacao,))
    
    def to_dict(self) -> Dict:
        """Converte para dicionário"""
        return {
            'idDoacao': self.idDoacao,
            'data_criacao': str(self.data_criacao) if self.data_criacao else None,
            'data_entrega': str(self.data_entrega) if self.data_entrega else None,
            'doador_id': self.doador_id,
            'campanha_id': self.campanha_id
        }


if __name__ == "__main__":
    print("\n=== TESTE MODELO DOACAO ===\n")
    
    # Precisaria ter um doador criado para testar
    doacao = Doacao(doador_id=1)
    
    if doacao.save():
        print(f"✓ Criado: {doacao}")