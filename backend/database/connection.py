"""
Módulo de Conexão com MySQL
"""

import os
import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Optional, Tuple
from dotenv import load_dotenv

load_dotenv()


class DatabaseConnection:
    """Gerenciador de conexões com MySQL"""
    
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': os.getenv('DB_NAME', 'somos_darua'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'charset': 'utf8mb4'
        }
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection and self.connection.is_connected():
            if exc_type is not None:
                self.connection.rollback()
        self.disconnect()
        return False
    
    def connect(self) -> bool:
        try:
            self.connection = mysql.connector.connect(**self.config)
            
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                db_info = self.connection.get_server_info()
                print(f"✓ Conectado ao MySQL versão {db_info}")
                return True
            else:
                print("✗ Falha ao conectar")
                return False
        except Error as e:
            print(f"✗ Erro ao conectar: {e}")
            return False
    
    def disconnect(self):
        if self.connection and self.connection.is_connected():
            if self.cursor:
                self.cursor.close()
            self.connection.close()
            print("✓ Conexão fechada")
    
    def execute_query(self, query: str, params: Optional[Tuple] = None) -> bool:
        try:
            self.cursor.execute(query, params or ())
            self.connection.commit()
            print(f"✓ Query executada ({self.cursor.rowcount} linhas afetadas)")
            return True
        except Error as e:
            print(f"✗ Erro ao executar query: {e}")
            self.connection.rollback()
            return False
    
    def fetch_all(self, query: str, params: Optional[Tuple] = None) -> List[Dict]:
        try:
            self.cursor.execute(query, params or ())
            results = self.cursor.fetchall()
            print(f"✓ Encontrados {len(results)} resultados")
            return results
        except Error as e:
            print(f"✗ Erro ao buscar dados: {e}")
            return []
    
    def fetch_one(self, query: str, params: Optional[Tuple] = None) -> Optional[Dict]:
        try:
            self.cursor.execute(query, params or ())
            result = self.cursor.fetchone()
            if result:
                print("✓ Resultado encontrado")
            else:
                print("ℹ Nenhum resultado encontrado")
            return result
        except Error as e:
            print(f"✗ Erro ao buscar dados: {e}")
            return None
    
    def get_last_insert_id(self) -> Optional[int]:
        return self.cursor.lastrowid if self.cursor else None


def test_connection():
    print("\n" + "="*60)
    print("TESTE DE CONEXÃO MySQL")
    print("="*60 + "\n")
    
    try:
        with DatabaseConnection() as db:
            result = db.fetch_one("SELECT DATABASE() as db_name, VERSION() as version")
            
            if result:
                print(f"✓ Banco atual: {result['db_name']}")
                print(f"✓ Versão MySQL: {result['version']}")
                print("\n✅ CONEXÃO OK!\n")
                return True
            else:
                print("\n❌ Falha no teste\n")
                return False
    except Exception as e:
        print(f"\n❌ Erro: {e}\n")
        return False


if __name__ == "__main__":
    test_connection()