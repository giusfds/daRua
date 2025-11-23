"""
Modelo CampanhaDoacao - Campanhas organizadas
"""

from typing import Optional, List, Dict
from datetime import date
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import DatabaseConnection


class CampanhaDoacao:
    """Representa uma campanha de doação no sistema"""
    
    def __init__(self, nome: str, data_inicio: Optional[date] = None,
                 data_termino: Optional[date] = None, descricao: Optional[str] = None,
                 idCampanhaDoacao: Optional[int] = None):
        self.idCampanhaDoacao = idCampanhaDoacao
        self.nome = nome
        self.data_inicio = data_inicio
        self.data_termino = data_termino
        self.descricao = descricao
    
    def __repr__(self):
        return f"CampanhaDoacao(id={self.idCampanhaDoacao}, nome={self.nome})"
    
    def validate(self) -> tuple[bool, str]:
        """Valida dados da campanha"""
        if not self.nome or not self.nome.strip():
            return False, "Nome é obrigatório"
        if self.data_inicio and self.data_termino:
            if self.data_termino < self.data_inicio:
                return False, "Data de término deve ser após data de início"
        return True, ""
    
    def save(self) -> bool:
        """Salva nova campanha"""
        valido, erro = self.validate()
        if not valido:
            print(f"✗ Validação falhou: {erro}")
            return False
        
        query = """
            INSERT INTO CampanhaDoacao (Nome, DataInicio, DataTermino, Descricao)
            VALUES (%s, %s, %s, %s)
        """
        params = (self.nome, self.data_inicio, self.data_termino, self.descricao)
        
        with DatabaseConnection() as db:
            if db.execute_query(query, params):
                self.idCampanhaDoacao = db.get_last_insert_id()
                return True
        return False
    
    def update(self) -> bool:
        """Atualiza campanha existente"""
        if not self.idCampanhaDoacao:
            print("✗ Campanha não possui ID")
            return False
        
        valido, erro = self.validate()
        if not valido:
            print(f"✗ Validação falhou: {erro}")
            return False
        
        query = """
            UPDATE CampanhaDoacao SET Nome = %s, DataInicio = %s, 
                                     DataTermino = %s, Descricao = %s
            WHERE idCampanhaDoacao = %s
        """
        params = (self.nome, self.data_inicio, self.data_termino, 
                 self.descricao, self.idCampanhaDoacao)
        
        with DatabaseConnection() as db:
            return db.execute_query(query, params)
    
    def delete(self) -> bool:
        """Remove campanha"""
        if not self.idCampanhaDoacao:
            print("✗ Campanha não possui ID")
            return False
        
        query = "DELETE FROM CampanhaDoacao WHERE idCampanhaDoacao = %s"
        with DatabaseConnection() as db:
            return db.execute_query(query, (self.idCampanhaDoacao,))
    
    @staticmethod
    def get_by_id(campanha_id: int) -> Optional['CampanhaDoacao']:
        """Busca campanha por ID"""
        query = "SELECT * FROM CampanhaDoacao WHERE idCampanhaDoacao = %s"
        with DatabaseConnection() as db:
            result = db.fetch_one(query, (campanha_id,))
            if result:
                return CampanhaDoacao(
                    idCampanhaDoacao=result['idCampanhaDoacao'],
                    nome=result['Nome'],
                    data_inicio=result['DataInicio'],
                    data_termino=result['DataTermino'],
                    descricao=result['Descricao']
                )
        return None
    
    @staticmethod
    def get_all() -> List['CampanhaDoacao']:
        """Retorna todas as campanhas"""
        query = "SELECT * FROM CampanhaDoacao ORDER BY DataInicio DESC"
        with DatabaseConnection() as db:
            results = db.fetch_all(query)
            return [
                CampanhaDoacao(
                    idCampanhaDoacao=row['idCampanhaDoacao'],
                    nome=row['Nome'],
                    data_inicio=row['DataInicio'],
                    data_termino=row['DataTermino'],
                    descricao=row['Descricao']
                )
                for row in results
            ]
    
    @staticmethod
    def get_campanhas_ativas() -> List['CampanhaDoacao']:
        """Retorna campanhas ativas (sem data de término ou futuras)"""
        query = """
            SELECT * FROM CampanhaDoacao 
            WHERE DataTermino IS NULL OR DataTermino >= CURDATE()
            ORDER BY DataInicio DESC
        """
        with DatabaseConnection() as db:
            results = db.fetch_all(query)
            return [
                CampanhaDoacao(
                    idCampanhaDoacao=row['idCampanhaDoacao'],
                    nome=row['Nome'],
                    data_inicio=row['DataInicio'],
                    data_termino=row['DataTermino'],
                    descricao=row['Descricao']
                )
                for row in results
            ]
    
    def to_dict(self) -> Dict:
        """Converte para dicionário"""
        return {
            'idCampanhaDoacao': self.idCampanhaDoacao,
            'nome': self.nome,
            'data_inicio': str(self.data_inicio) if self.data_inicio else None,
            'data_termino': str(self.data_termino) if self.data_termino else None,
            'descricao': self.descricao
        }


if __name__ == "__main__":
    print("\n=== TESTE MODELO CAMPANHA ===\n")
    
    from datetime import date, timedelta
    
    campanha = CampanhaDoacao(
        nome="Campanha de Inverno 2025",
        data_inicio=date.today(),
        data_termino=date.today() + timedelta(days=90),
        descricao="Arrecadação de roupas e cobertores"
    )
    
    if campanha.save():
        print(f"✓ Criado: {campanha}")