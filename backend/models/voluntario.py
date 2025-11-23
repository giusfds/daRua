"""
Modelo Voluntario - Pessoas que ajudam nas doações
"""

from typing import Optional, List, Dict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import DatabaseConnection


class Voluntario:
    """Representa um voluntário no sistema"""
    
    def __init__(self, nome: str, email: Optional[str] = None,
                 telefone: Optional[str] = None, idVoluntario: Optional[int] = None):
        self.idVoluntario = idVoluntario
        self.nome = nome
        self.email = email
        self.telefone = telefone
    
    def __repr__(self):
        return f"Voluntario(id={self.idVoluntario}, nome={self.nome})"
    
    def validate(self) -> tuple[bool, str]:
        """Valida dados do voluntário"""
        if not self.nome or not self.nome.strip():
            return False, "Nome é obrigatório"
        if self.email and '@' not in self.email:
            return False, "Email inválido"
        return True, ""
    
    def save(self) -> bool:
        """Salva novo voluntário"""
        valido, erro = self.validate()
        if not valido:
            print(f"✗ Validação falhou: {erro}")
            return False
        
        query = "INSERT INTO Voluntario (Nome, Email, Telefone) VALUES (%s, %s, %s)"
        params = (self.nome, self.email, self.telefone)
        
        with DatabaseConnection() as db:
            if db.execute_query(query, params):
                self.idVoluntario = db.get_last_insert_id()
                return True
        return False
    
    def update(self) -> bool:
        """Atualiza voluntário existente"""
        if not self.idVoluntario:
            print("✗ Voluntário não possui ID")
            return False
        
        valido, erro = self.validate()
        if not valido:
            print(f"✗ Validação falhou: {erro}")
            return False
        
        query = "UPDATE Voluntario SET Nome = %s, Email = %s, Telefone = %s WHERE idVoluntario = %s"
        params = (self.nome, self.email, self.telefone, self.idVoluntario)
        
        with DatabaseConnection() as db:
            return db.execute_query(query, params)
    
    def delete(self) -> bool:
        """Remove voluntário"""
        if not self.idVoluntario:
            print("✗ Voluntário não possui ID")
            return False
        
        query = "DELETE FROM Voluntario WHERE idVoluntario = %s"
        with DatabaseConnection() as db:
            return db.execute_query(query, (self.idVoluntario,))
    
    @staticmethod
    def get_by_id(voluntario_id: int) -> Optional['Voluntario']:
        """Busca voluntário por ID"""
        query = "SELECT * FROM Voluntario WHERE idVoluntario = %s"
        with DatabaseConnection() as db:
            result = db.fetch_one(query, (voluntario_id,))
            if result:
                return Voluntario(
                    idVoluntario=result['idVoluntario'],
                    nome=result['Nome'],
                    email=result['Email'],
                    telefone=result['Telefone']
                )
        return None
    
    @staticmethod
    def get_all() -> List['Voluntario']:
        """Retorna todos os voluntários"""
        query = "SELECT * FROM Voluntario ORDER BY Nome"
        with DatabaseConnection() as db:
            results = db.fetch_all(query)
            return [
                Voluntario(
                    idVoluntario=row['idVoluntario'],
                    nome=row['Nome'],
                    email=row['Email'],
                    telefone=row['Telefone']
                )
                for row in results
            ]
    
    def to_dict(self) -> Dict:
        """Converte para dicionário"""
        return {
            'idVoluntario': self.idVoluntario,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone
        }


if __name__ == "__main__":
    print("\n=== TESTE MODELO VOLUNTARIO ===\n")
    
    voluntario = Voluntario(
        nome="Ana Paula",
        email="ana@email.com",
        telefone="(31) 98888-8888"
    )
    
    if voluntario.save():
        print(f"✓ Criado: {voluntario}")