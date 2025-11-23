"""
Modelo PontoColeta - Locais de coleta de doações
"""

from typing import Optional, List, Dict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import DatabaseConnection


class PontoColeta:
    """Representa um ponto de coleta no sistema"""
    
    def __init__(self, responsavel: str, logradouro: Optional[str] = None,
                 numero: Optional[str] = None, complemento: Optional[str] = None,
                 bairro: Optional[str] = None, cidade: Optional[str] = None,
                 estado: Optional[str] = None, cep: Optional[str] = None,
                 idPontoColeta: Optional[int] = None):
        self.idPontoColeta = idPontoColeta
        self.responsavel = responsavel
        self.logradouro = logradouro
        self.numero = numero
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.cep = cep
    
    def __repr__(self):
        return f"PontoColeta(id={self.idPontoColeta}, responsavel={self.responsavel})"
    
    def validate(self) -> tuple[bool, str]:
        """Valida dados do ponto de coleta"""
        if not self.responsavel or not self.responsavel.strip():
            return False, "Responsável é obrigatório"
        if self.estado and len(self.estado) != 2:
            return False, "Estado deve ter 2 caracteres (UF)"
        return True, ""
    
    def save(self) -> bool:
        """Salva novo ponto de coleta"""
        valido, erro = self.validate()
        if not valido:
            print(f"✗ Validação falhou: {erro}")
            return False
        
        query = """
            INSERT INTO PontoColeta (Responsavel, Logradouro, Numero,
                                    Complemento, Bairro, Cidade, Estado, CEP)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (self.responsavel, self.logradouro, self.numero,
                 self.complemento, self.bairro, self.cidade, self.estado, self.cep)
        
        with DatabaseConnection() as db:
            if db.execute_query(query, params):
                self.idPontoColeta = db.get_last_insert_id()
                return True
        return False
    
    def update(self) -> bool:
        """Atualiza ponto de coleta existente"""
        if not self.idPontoColeta:
            print("✗ Ponto de coleta não possui ID")
            return False
        
        valido, erro = self.validate()
        if not valido:
            print(f"✗ Validação falhou: {erro}")
            return False
        
        query = """
            UPDATE PontoColeta SET Responsavel = %s, Logradouro = %s, Numero = %s,
                                  Complemento = %s, Bairro = %s, Cidade = %s,
                                  Estado = %s, CEP = %s
            WHERE idPontoColeta = %s
        """
        params = (self.responsavel, self.logradouro, self.numero,
                 self.complemento, self.bairro, self.cidade, self.estado,
                 self.cep, self.idPontoColeta)
        
        with DatabaseConnection() as db:
            return db.execute_query(query, params)
    
    def delete(self) -> bool:
        """Remove ponto de coleta"""
        if not self.idPontoColeta:
            print("✗ Ponto de coleta não possui ID")
            return False
        
        query = "DELETE FROM PontoColeta WHERE idPontoColeta = %s"
        with DatabaseConnection() as db:
            return db.execute_query(query, (self.idPontoColeta,))
    
    @staticmethod
    def get_by_id(ponto_id: int) -> Optional['PontoColeta']:
        """Busca ponto de coleta por ID"""
        query = "SELECT * FROM PontoColeta WHERE idPontoColeta = %s"
        with DatabaseConnection() as db:
            result = db.fetch_one(query, (ponto_id,))
            if result:
                return PontoColeta(
                    idPontoColeta=result['idPontoColeta'],
                    responsavel=result['Responsavel'],
                    logradouro=result['Logradouro'],
                    numero=result['Numero'],
                    complemento=result['Complemento'],
                    bairro=result['Bairro'],
                    cidade=result['Cidade'],
                    estado=result['Estado'],
                    cep=result['CEP']
                )
        return None
    
    @staticmethod
    def get_all() -> List['PontoColeta']:
        """Retorna todos os pontos de coleta"""
        query = "SELECT * FROM PontoColeta ORDER BY Responsavel"
        with DatabaseConnection() as db:
            results = db.fetch_all(query)
            return [
                PontoColeta(
                    idPontoColeta=row['idPontoColeta'],
                    responsavel=row['Responsavel'],
                    logradouro=row['Logradouro'],
                    numero=row['Numero'],
                    complemento=row['Complemento'],
                    bairro=row['Bairro'],
                    cidade=row['Cidade'],
                    estado=row['Estado'],
                    cep=row['CEP']
                )
                for row in results
            ]
    
    def to_dict(self) -> Dict:
        """Converte para dicionário"""
        return {
            'idPontoColeta': self.idPontoColeta,
            'responsavel': self.responsavel,
            'logradouro': self.logradouro,
            'numero': self.numero,
            'complemento': self.complemento,
            'bairro': self.bairro,
            'cidade': self.cidade,
            'estado': self.estado,
            'cep': self.cep
        }


if __name__ == "__main__":
    print("\n=== TESTE MODELO PONTO COLETA ===\n")
    
    ponto = PontoColeta(
        responsavel="Carlos Mendes",
        cidade="Belo Horizonte",
        estado="MG"
    )
    
    if ponto.save():
        print(f"✓ Criado: {ponto}")