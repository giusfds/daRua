"""
Modelo Beneficiario - Pessoas que recebem doações
"""

from typing import Optional, List, Dict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import DatabaseConnection


class Beneficiario:
    """Representa um beneficiário no sistema"""
    
    def __init__(self, nome: str, idade: Optional[int] = None,
                 genero: Optional[str] = None, descricao: Optional[str] = None,
                 idBeneficiario: Optional[int] = None):
        self.idBeneficiario = idBeneficiario
        self.nome = nome
        self.idade = idade
        self.genero = genero
        self.descricao = descricao
    
    def __repr__(self):
        return f"Beneficiario(id={self.idBeneficiario}, nome={self.nome})"
    
    def validate(self) -> tuple[bool, str]:
        """Valida dados do beneficiário"""
        if not self.nome or not self.nome.strip():
            return False, "Nome é obrigatório"
        if self.idade is not None and self.idade < 0:
            return False, "Idade não pode ser negativa"
        if self.genero and self.genero not in ['M', 'F', 'O', 'N']:
            return False, "Gênero deve ser M, F, O ou N"
        return True, ""
    
    def save(self) -> bool:
        """Salva novo beneficiário"""
        valido, erro = self.validate()
        if not valido:
            print(f"✗ Validação falhou: {erro}")
            return False
        
        query = """
            INSERT INTO Beneficiario (Nome, Idade, Genero, Descricao)
            VALUES (%s, %s, %s, %s)
        """
        params = (self.nome, self.idade, self.genero, self.descricao)
        
        with DatabaseConnection() as db:
            if db.execute_query(query, params):
                self.idBeneficiario = db.get_last_insert_id()
                return True
        return False
    
    def update(self) -> bool:
        """Atualiza beneficiário existente"""
        if not self.idBeneficiario:
            print("✗ Beneficiário não possui ID")
            return False
        
        valido, erro = self.validate()
        if not valido:
            print(f"✗ Validação falhou: {erro}")
            return False
        
        query = """
            UPDATE Beneficiario SET Nome = %s, Idade = %s, Genero = %s, Descricao = %s
            WHERE idBeneficiario = %s
        """
        params = (self.nome, self.idade, self.genero, self.descricao, self.idBeneficiario)
        
        with DatabaseConnection() as db:
            return db.execute_query(query, params)
    
    def delete(self) -> bool:
        """Remove beneficiário"""
        if not self.idBeneficiario:
            print("✗ Beneficiário não possui ID")
            return False
        
        query = "DELETE FROM Beneficiario WHERE idBeneficiario = %s"
        with DatabaseConnection() as db:
            return db.execute_query(query, (self.idBeneficiario,))
    
    @staticmethod
    def get_by_id(beneficiario_id: int) -> Optional['Beneficiario']:
        """Busca beneficiário por ID"""
        query = "SELECT * FROM Beneficiario WHERE idBeneficiario = %s"
        with DatabaseConnection() as db:
            result = db.fetch_one(query, (beneficiario_id,))
            if result:
                return Beneficiario(
                    idBeneficiario=result['idBeneficiario'],
                    nome=result['Nome'],
                    idade=result['Idade'],
                    genero=result['Genero'],
                    descricao=result['Descricao']
                )
        return None
    
    @staticmethod
    def get_all() -> List['Beneficiario']:
        """Retorna todos os beneficiários"""
        query = "SELECT * FROM Beneficiario ORDER BY Nome"
        with DatabaseConnection() as db:
            results = db.fetch_all(query)
            return [
                Beneficiario(
                    idBeneficiario=row['idBeneficiario'],
                    nome=row['Nome'],
                    idade=row['Idade'],
                    genero=row['Genero'],
                    descricao=row['Descricao']
                )
                for row in results
            ]
    
    def to_dict(self) -> Dict:
        """Converte para dicionário"""
        return {
            'idBeneficiario': self.idBeneficiario,
            'nome': self.nome,
            'idade': self.idade,
            'genero': self.genero,
            'descricao': self.descricao
        }


if __name__ == "__main__":
    print("\n=== TESTE MODELO BENEFICIARIO ===\n")
    
    beneficiario = Beneficiario(
        nome="Maria Santos",
        idade=35,
        genero="F",
        descricao="Mãe de 3 filhos"
    )
    
    if beneficiario.save():
        print(f"✓ Criado: {beneficiario}")