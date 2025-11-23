"""
Modelo Doador - Pessoas/empresas que fazem doações
"""

from typing import Optional, List, Dict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import DatabaseConnection


class Doador:
    """Representa um doador no sistema"""
    
    def __init__(self, nome: str, telefone: Optional[str] = None,
                 email: Optional[str] = None, logradouro: Optional[str] = None,
                 numero: Optional[str] = None, complemento: Optional[str] = None,
                 bairro: Optional[str] = None, cidade: Optional[str] = None,
                 estado: Optional[str] = None, cep: Optional[str] = None,
                 idDoador: Optional[int] = None):
        self.idDoador = idDoador
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.logradouro = logradouro
        self.numero = numero
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.cep = cep
    
    def __repr__(self):
        return f"Doador(id={self.idDoador}, nome={self.nome})"
    
    def validate(self) -> tuple[bool, str]:
        """Valida dados do doador"""
        if not self.nome or not self.nome.strip():
            return False, "Nome é obrigatório"
        if self.email and '@' not in self.email:
            return False, "Email inválido"
        if self.estado and len(self.estado) != 2:
            return False, "Estado deve ter 2 caracteres (UF)"
        if self.cep:
            cep_limpo = self.cep.replace('-', '').replace('.', '')
            if not cep_limpo.isdigit() or len(cep_limpo) != 8:
                return False, "CEP inválido"
        return True, ""
    
    def save(self) -> bool:
        """Salva novo doador"""
        valido, erro = self.validate()
        if not valido:
            print(f"✗ Validação falhou: {erro}")
            return False
        
        query = """
            INSERT INTO Doador (Nome, Telefone, Email, Logradouro, Numero,
                               Complemento, Bairro, Cidade, Estado, CEP)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (self.nome, self.telefone, self.email, self.logradouro,
                 self.numero, self.complemento, self.bairro, self.cidade,
                 self.estado, self.cep)
        
        with DatabaseConnection() as db:
            if db.execute_query(query, params):
                self.idDoador = db.get_last_insert_id()
                return True
        return False
    
    def update(self) -> bool:
        """Atualiza doador existente"""
        if not self.idDoador:
            print("✗ Doador não possui ID")
            return False
        
        valido, erro = self.validate()
        if not valido:
            print(f"✗ Validação falhou: {erro}")
            return False
        
        query = """
            UPDATE Doador SET Nome = %s, Telefone = %s, Email = %s,
                             Logradouro = %s, Numero = %s, Complemento = %s,
                             Bairro = %s, Cidade = %s, Estado = %s, CEP = %s
            WHERE idDoador = %s
        """
        params = (self.nome, self.telefone, self.email, self.logradouro,
                 self.numero, self.complemento, self.bairro, self.cidade,
                 self.estado, self.cep, self.idDoador)
        
        with DatabaseConnection() as db:
            return db.execute_query(query, params)
    
    def delete(self) -> bool:
        """Remove doador"""
        if not self.idDoador:
            print("✗ Doador não possui ID")
            return False
        
        query = "DELETE FROM Doador WHERE idDoador = %s"
        with DatabaseConnection() as db:
            return db.execute_query(query, (self.idDoador,))
    
    @staticmethod
    def get_by_id(doador_id: int) -> Optional['Doador']:
        """Busca doador por ID"""
        query = "SELECT * FROM Doador WHERE idDoador = %s"
        with DatabaseConnection() as db:
            result = db.fetch_one(query, (doador_id,))
            if result:
                return Doador(
                    idDoador=result['idDoador'],
                    nome=result['Nome'],
                    telefone=result['Telefone'],
                    email=result['Email'],
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
    def get_all() -> List['Doador']:
        """Retorna todos os doadores"""
        query = "SELECT * FROM Doador ORDER BY Nome"
        with DatabaseConnection() as db:
            results = db.fetch_all(query)
            return [
                Doador(
                    idDoador=row['idDoador'],
                    nome=row['Nome'],
                    telefone=row['Telefone'],
                    email=row['Email'],
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
    
    @staticmethod
    def search_by_name(nome: str) -> List['Doador']:
        """Busca doadores por nome"""
        query = "SELECT * FROM Doador WHERE Nome LIKE %s ORDER BY Nome"
        with DatabaseConnection() as db:
            results = db.fetch_all(query, (f"%{nome}%",))
            return [
                Doador(
                    idDoador=row['idDoador'],
                    nome=row['Nome'],
                    telefone=row['Telefone'],
                    email=row['Email'],
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
            'idDoador': self.idDoador,
            'nome': self.nome,
            'telefone': self.telefone,
            'email': self.email,
            'logradouro': self.logradouro,
            'numero': self.numero,
            'complemento': self.complemento,
            'bairro': self.bairro,
            'cidade': self.cidade,
            'estado': self.estado,
            'cep': self.cep
        }


if __name__ == "__main__":
    print("\n=== TESTE MODELO DOADOR ===\n")
    
    # Criar doador
    doador = Doador(
        nome="João Silva",
        email="joao@email.com",
        telefone="(31) 99999-9999",
        cidade="Belo Horizonte",
        estado="MG"
    )
    
    if doador.save():
        print(f"✓ Criado: {doador}")
        
        # Buscar por ID
        encontrado = Doador.get_by_id(doador.idDoador)
        print(f"✓ Buscado: {encontrado}")
        
        # Listar todos
        todos = Doador.get_all()
        print(f"✓ Total: {len(todos)} doadores")