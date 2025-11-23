"""
Script de Setup do Banco de Dados

O que faz:
1. Conecta ao MySQL (sem especificar banco)
2. Lê o script SQL
3. Executa todos os comandos
4. Verifica se tabelas foram criadas
"""

import os
import sys
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()


def read_sql_file(filepath: str) -> str:
    """Lê o conteúdo de um arquivo SQL"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"✗ Erro: Arquivo não encontrado: {filepath}")
        return None
    except Exception as e:
        print(f"✗ Erro ao ler arquivo: {e}")
        return None


def execute_sql_script(cursor, script: str):
    """Executa um script SQL com múltiplos comandos"""
    # Remove comentários de linha
    lines = [line for line in script.split('\n') 
             if not line.strip().startswith('--')]
    script = '\n'.join(lines)
    
    # Divide em comandos individuais
    commands = [cmd.strip() for cmd in script.split(';') if cmd.strip()]
    
    print(f"\n📝 Executando {len(commands)} comandos SQL...\n")
    
    for i, command in enumerate(commands, 1):
        if not command or command.isspace():
            continue
        
        try:
            cursor.execute(command)
            
            # Consumir resultados pendentes (importante!)
            # Isso evita o erro "Unread result found"
            try:
                cursor.fetchall()
            except:
                pass
            
            print(f"✓ Comando {i}/{len(commands)} executado")
        except Error as e:
            print(f"✗ Erro no comando {i}: {e}")
            print(f"   Comando: {command[:100]}...")
            raise

def setup_database():
    """Função principal de setup"""
    print("\n" + "="*60)
    print(" SETUP DO BANCO DE DADOS - SOMOS DARUA")
    print("="*60)
    
    connection = None
    cursor = None
    
    try:
        # Passo 1: Conectar ao MySQL (sem database)
        print("\n📌 Passo 1: Conectando ao MySQL...")
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            port=int(os.getenv('DB_PORT', 3306))
        )
        cursor = connection.cursor()
        print(f"✓ Conectado ao MySQL")
        
        # Passo 2: Ler script SQL
        print("\n📌 Passo 2: Lendo script SQL...")
        
        # Caminho relativo ao arquivo setup.py
        script_path = os.path.join(
            os.path.dirname(__file__),
            '../../database/schema/create_database.sql'
        )
        script_path = os.path.normpath(script_path)
        
        if not os.path.exists(script_path):
            print(f"✗ Erro: Arquivo não encontrado: {script_path}")
            print(f"   Caminho atual: {os.getcwd()}")
            return False
        
        sql_script = read_sql_file(script_path)
        if not sql_script:
            return False
        
        print(f"✓ Script carregado ({len(sql_script)} caracteres)")
        
        # Passo 3: Executar script
        print("\n📌 Passo 3: Executando script...")
        execute_sql_script(cursor, sql_script)
        connection.commit()
        print("\n✓ Script executado com sucesso!")
        
        # Passo 4: Verificar tabelas
        print("\n📌 Passo 4: Verificando tabelas...")
        cursor.execute(f"USE {os.getenv('DB_NAME', 'somos_darua')}")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        if tables:
            print(f"\n✓ Banco criado com {len(tables)} tabelas:")
            print("\n" + "-"*40)
            for i, (table_name,) in enumerate(tables, 1):
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"  {i:2d}. {table_name:25s} ({count} registros)")
            print("-"*40)
        else:
            print("⚠ Nenhuma tabela encontrada!")
            return False
        
        # Resumo
        print("\n" + "="*60)
        print(" ✅ SETUP CONCLUÍDO COM SUCESSO!")
        print("="*60)
        print(f"\n📊 Resumo:")
        print(f"   • Banco: {os.getenv('DB_NAME', 'somos_darua')}")
        print(f"   • Host: {os.getenv('DB_HOST', 'localhost')}")
        print(f"   • Tabelas: {len(tables)}")
        print(f"\n💡 Próximo passo:")
        print(f"   Testar conexão: python3 backend/database/connection.py\n")
        
        return True
        
    except Error as e:
        print(f"\n✗ Erro durante setup: {e}")
        if connection:
            connection.rollback()
        return False
        
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("\n✓ Conexão fechada\n")


def main():
    """Menu principal"""
    print("\n" + "="*60)
    print(" GERENCIADOR DE BANCO DE DADOS")
    print("="*60)
    print("\n1. Criar/Recriar banco de dados")
    print("2. Sair")
    
    opcao = input("\nEscolha uma opção: ").strip()
    
    if opcao == '1':
        print("\n⚠️  Isso irá recriar o banco (apagando dados existentes)")
        confirmar = input("Continuar? (s/n): ").lower()
        if confirmar == 's':
            setup_database()
    elif opcao == '2':
        print("\n👋 Até logo!")
    else:
        print("\n✗ Opção inválida")


if __name__ == "__main__":
    main()