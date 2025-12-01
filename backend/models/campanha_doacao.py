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
                 meta: Optional[float] = 0.0, arrecadado: Optional[float] = 0.0,
                 tipo_meta: Optional[str] = "R$", idCampanhaDoacao: Optional[int] = None):
        self.idCampanhaDoacao = idCampanhaDoacao
        self.nome = nome
        self.data_inicio = data_inicio
        self.data_termino = data_termino
        self.descricao = descricao
        self.meta = meta or 0.0
        self.arrecadado = arrecadado or 0.0
        self.tipo_meta = tipo_meta or "R$"
    
    def __repr__(self):
        return f"CampanhaDoacao(id={self.idCampanhaDoacao}, nome={self.nome})"
    
    def validate(self) -> tuple[bool, str]:
        """Valida dados da campanha"""
        if not self.nome or not self.nome.strip():
            return False, "Nome é obrigatório"
        if self.data_inicio and self.data_termino:
            if self.data_termino < self.data_inicio:
                return False, "Data de término deve ser após data de início"
        if self.meta < 0:
            return False, "Meta não pode ser negativa"
        if self.arrecadado < 0:
            return False, "Arrecadado não pode ser negativo"
        return True, ""
    
    def save(self) -> bool:
        """Salva nova campanha"""
        valido, erro = self.validate()
        if not valido:
            print(f"✗ Validação falhou: {erro}")
            return False
        
        query = """
            INSERT INTO CampanhaDoacao (Nome, DataInicio, DataTermino, Descricao, Meta, Arrecadado, TipoMeta)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (self.nome, self.data_inicio, self.data_termino, self.descricao, 
                 self.meta, self.arrecadado, self.tipo_meta)
        
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
                                     DataTermino = %s, Descricao = %s,
                                     Meta = %s, Arrecadado = %s, TipoMeta = %s
            WHERE idCampanhaDoacao = %s
        """
        params = (self.nome, self.data_inicio, self.data_termino, 
                 self.descricao, self.meta, self.arrecadado, self.tipo_meta,
                 self.idCampanhaDoacao)
        
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
                    descricao=result['Descricao'],
                    meta=float(result.get('Meta', 0.0)),
                    arrecadado=float(result.get('Arrecadado', 0.0)),
                    tipo_meta=result.get('TipoMeta', 'R$')
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
                    descricao=row['Descricao'],
                    meta=float(row.get('Meta', 0.0)),
                    arrecadado=float(row.get('Arrecadado', 0.0)),
                    tipo_meta=row.get('TipoMeta', 'R$')
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
                    descricao=row['Descricao'],
                    meta=float(row.get('Meta', 0.0)),
                    arrecadado=float(row.get('Arrecadado', 0.0)),
                    tipo_meta=row.get('TipoMeta', 'R$')
                )
                for row in results
            ]
    
    def calcular_progresso(self) -> float:
        """Calcula o progresso da campanha em porcentagem"""
        if self.meta <= 0:
            return 0.0
        progresso = (self.arrecadado / self.meta) * 100
        return min(progresso, 100.0)  # Limita a 100%
    
    def to_dict(self) -> Dict:
        """Converte para dicionário"""
        return {
            'idCampanhaDoacao': self.idCampanhaDoacao,
            'nome': self.nome,
            'data_inicio': str(self.data_inicio) if self.data_inicio else None,
            'data_termino': str(self.data_termino) if self.data_termino else None,
            'descricao': self.descricao,
            'meta': self.meta,
            'arrecadado': self.arrecadado,
            'tipo_meta': self.tipo_meta,
            'progresso': self.calcular_progresso()
        }


if __name__ == "__main__":
    print("\n=== TESTE MODELO CAMPANHA ===\n")
    
    from datetime import date, timedelta
    
    campanha = CampanhaDoacao(
        nome="Campanha de Inverno 2025",
        data_inicio=date.today(),
        data_termino=date.today() + timedelta(days=90),
        descricao="Arrecadação de roupas e cobertores",
        meta=10000.00,
        arrecadado=2500.00,
        tipo_meta="R$"
    )
    
    if campanha.save():
        print(f"✓ Criado: {campanha}")
        print(f"✓ Progresso: {campanha.calcular_progresso():.1f}%")