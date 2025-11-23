"""
Modelo ObjetoDoavel - Itens que podem ser doados
"""

from typing import Optional, List, Dict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import DatabaseConnection


class ObjetoDoavel:
    """Representa um objeto doável no sistema"""
    
    def __init__(self, nome: str, descricao: Optional[str] = None,
                 categoria: Optional[str] = None, ponto_coleta_id: Optional[int] = None,
                 idObjetoDoavel: Optional[int] = None):
        self.idObjetoDoavel = idObjetoDoavel
        self.nome = nome
        self.descricao = descricao
        self.categoria = categoria
        self.ponto_coleta_id = ponto_coleta_id
    
    def __repr__(self):
        return f"ObjetoDoavel(id={self.idObjetoDoavel}, nome={self.nome})"
    
    def validate(self) -> tuple[bool, str]:
        """Valida dados do objeto"""
        if not self.nome or not self.nome.strip():
            return False, "Nome é obrigatório"
        return True, ""
    
    def save(self) -> bool:
        """Salva novo objeto doável"""
        valido, erro = self.validate()
        if not valido:
            print(f"✗ Validação falhou: {erro}")
            return False
        
        query = """
            INSERT INTO ObjetoDoavel (Nome, Descricao, Categoria, PontoColeta_idPontoColeta)
            VALUES (%s, %s, %s, %s)
        """
        params = (self.nome, self.descricao, self.categoria, self.ponto_coleta_id)
        
        with DatabaseConnection() as db:
            if db.execute_query(query, params):
                self.idObjetoDoavel = db.get_last_insert_id()
                return True
        return False
    
    def update(self) -> bool:
        """Atualiza objeto existente"""
        if not self.idObjetoDoavel:
            print("✗ Objeto não possui ID")
            return False
        
        valido, erro = self.validate()
        if not valido:
            print(f"✗ Validação falhou: {erro}")
            return False
        
        query = """
            UPDATE ObjetoDoavel SET Nome = %s, Descricao = %s, 
                                   Categoria = %s, PontoColeta_idPontoColeta = %s
            WHERE idObjetoDoavel = %s
        """
        params = (self.nome, self.descricao, self.categoria, 
                 self.ponto_coleta_id, self.idObjetoDoavel)
        
        with DatabaseConnection() as db:
            return db.execute_query(query, params)
    
    def delete(self) -> bool:
        """Remove objeto"""
        if not self.idObjetoDoavel:
            print("✗ Objeto não possui ID")
            return False
        
        query = "DELETE FROM ObjetoDoavel WHERE idObjetoDoavel = %s"
        with DatabaseConnection() as db:
            return db.execute_query(query, (self.idObjetoDoavel,))
    
    @staticmethod
    def get_by_id(objeto_id: int) -> Optional['ObjetoDoavel']:
        """Busca objeto por ID"""
        query = "SELECT * FROM ObjetoDoavel WHERE idObjetoDoavel = %s"
        with DatabaseConnection() as db:
            result = db.fetch_one(query, (objeto_id,))
            if result:
                return ObjetoDoavel(
                    idObjetoDoavel=result['idObjetoDoavel'],
                    nome=result['Nome'],
                    descricao=result['Descricao'],
                    categoria=result['Categoria'],
                    ponto_coleta_id=result['PontoColeta_idPontoColeta']
                )
        return None
    
    @staticmethod
    def get_all() -> List['ObjetoDoavel']:
        """Retorna todos os objetos"""
        query = "SELECT * FROM ObjetoDoavel ORDER BY Nome"
        with DatabaseConnection() as db:
            results = db.fetch_all(query)
            return [
                ObjetoDoavel(
                    idObjetoDoavel=row['idObjetoDoavel'],
                    nome=row['Nome'],
                    descricao=row['Descricao'],
                    categoria=row['Categoria'],
                    ponto_coleta_id=row['PontoColeta_idPontoColeta']
                )
                for row in results
            ]
    
    @staticmethod
    def get_by_categoria(categoria: str) -> List['ObjetoDoavel']:
        """Busca objetos por categoria"""
        query = "SELECT * FROM ObjetoDoavel WHERE Categoria = %s ORDER BY Nome"
        with DatabaseConnection() as db:
            results = db.fetch_all(query, (categoria,))
            return [
                ObjetoDoavel(
                    idObjetoDoavel=row['idObjetoDoavel'],
                    nome=row['Nome'],
                    descricao=row['Descricao'],
                    categoria=row['Categoria'],
                    ponto_coleta_id=row['PontoColeta_idPontoColeta']
                )
                for row in results
            ]
    
    def to_dict(self) -> Dict:
        """Converte para dicionário"""
        return {
            'idObjetoDoavel': self.idObjetoDoavel,
            'nome': self.nome,
            'descricao': self.descricao,
            'categoria': self.categoria,
            'ponto_coleta_id': self.ponto_coleta_id
        }


if __name__ == "__main__":
    print("\n=== TESTE MODELO OBJETO DOAVEL ===\n")
    
    objeto = ObjetoDoavel(
        nome="Cobertor de lã",
        descricao="Cobertor novo, cor azul",
        categoria="Roupas de cama"
    )
    
    if objeto.save():
        print(f"✓ Criado: {objeto}")