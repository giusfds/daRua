"""
Modelo Necessidade - Itens prioritários
"""

from typing import Optional, List, Dict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import DatabaseConnection


class Necessidade:
    """Representa uma necessidade no sistema"""
    
    def __init__(self, descricao: str, idNecessidade: Optional[int] = None):
        self.idNecessidade = idNecessidade
        self.descricao = descricao
    
    def __repr__(self):
        return f"Necessidade(id={self.idNecessidade}, descricao={self.descricao[:30]}...)"
    
    def validate(self) -> tuple[bool, str]:
        """Valida dados da necessidade"""
        if not self.descricao or not self.descricao.strip():
            return False, "Descrição é obrigatória"
        return True, ""
    
    def save(self) -> bool:
        """Salva nova necessidade"""
        valido, erro = self.validate()
        if not valido:
            print(f"✗ Validação falhou: {erro}")
            return False
        
        query = "INSERT INTO Necessidade (Descricao) VALUES (%s)"
        params = (self.descricao,)
        
        with DatabaseConnection() as db:
            if db.execute_query(query, params):
                self.idNecessidade = db.get_last_insert_id()
                return True
        return False
    
    def update(self) -> bool:
        """Atualiza necessidade existente"""
        if not self.idNecessidade:
            print("✗ Necessidade não possui ID")
            return False
        
        valido, erro = self.validate()
        if not valido:
            print(f"✗ Validação falhou: {erro}")
            return False
        
        query = "UPDATE Necessidade SET Descricao = %s WHERE idNecessidade = %s"
        params = (self.descricao, self.idNecessidade)
        
        with DatabaseConnection() as db:
            return db.execute_query(query, params)
    
    def delete(self) -> bool:
        """Remove necessidade"""
        if not self.idNecessidade:
            print("✗ Necessidade não possui ID")
            return False
        
        query = "DELETE FROM Necessidade WHERE idNecessidade = %s"
        with DatabaseConnection() as db:
            return db.execute_query(query, (self.idNecessidade,))
    
    @staticmethod
    def get_by_id(necessidade_id: int) -> Optional['Necessidade']:
        """Busca necessidade por ID"""
        query = "SELECT * FROM Necessidade WHERE idNecessidade = %s"
        with DatabaseConnection() as db:
            result = db.fetch_one(query, (necessidade_id,))
            if result:
                return Necessidade(
                    idNecessidade=result['idNecessidade'],
                    descricao=result['Descricao']
                )
        return None
    
    @staticmethod
    def get_all() -> List['Necessidade']:
        """Retorna todas as necessidades"""
        query = "SELECT * FROM Necessidade ORDER BY Descricao"
        with DatabaseConnection() as db:
            results = db.fetch_all(query)
            return [
                Necessidade(
                    idNecessidade=row['idNecessidade'],
                    descricao=row['Descricao']
                )
                for row in results
            ]
    
    def to_dict(self) -> Dict:
        """Converte para dicionário"""
        return {
            'idNecessidade': self.idNecessidade,
            'descricao': self.descricao
        }


if __name__ == "__main__":
    print("\n=== TESTE MODELO NECESSIDADE ===\n")
    
    necessidade = Necessidade(descricao="Roupas de inverno")
    
    if necessidade.save():
        print(f"✓ Criado: {necessidade}")