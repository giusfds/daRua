# 📦 Guia de Instalação - Somos DaRua

## 📋 Índice

- [Pré-requisitos](#pré-requisitos)
- [Instalação Rápida](#instalação-rápida)
- [Instalação Detalhada](#instalação-detalhada)
  - [1. Python](#1-instalando-python)
  - [2. MySQL](#2-instalando-mysql)
  - [3. Git](#3-instalando-git)
  - [4. Projeto](#4-clonando-o-projeto)
  - [5. Dependências](#5-instalando-dependências)
  - [6. Banco de Dados](#6-configurando-banco-de-dados)
  - [7. Variáveis de Ambiente](#7-configurando-variáveis-de-ambiente)
- [Executando o Sistema](#executando-o-sistema)
- [Troubleshooting](#troubleshooting)
- [Ambientes](#ambientes)

---

## 📋 Pré-requisitos

Antes de começar, você precisará ter instalado em seu computador:

| Software   | Versão Mínima       | Download                                        |
| ---------- | ------------------- | ----------------------------------------------- |
| **Python** | 3.10+               | [python.org](https://www.python.org/downloads/) |
| **MySQL**  | 8.0+                | [mysql.com](https://dev.mysql.com/downloads/)   |
| **Git**    | 2.0+                | [git-scm.com](https://git-scm.com/downloads)    |
| **pip**    | Incluído com Python | -                                               |

### Verificar Instalações

```bash
# Python
python --version
# ou
python3 --version

# pip
pip --version
# ou
pip3 --version

# MySQL
mysql --version

# Git
git --version
```

---

## 🚀 Instalação Rápida

Para usuários experientes:

```bash
# 1. Clone o repositório
git clone https://github.com/giusfds/DaRua.git
cd DaRua

# 2. Crie e ative ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Instale dependências
pip install -r requirements.txt

# 4. Configure .env
cp .env.example .env
# Edite .env com suas credenciais

# 5. Configure banco de dados
mysql -u root -p < database/schema/create_database.sql

# 6. Execute
cd app
streamlit run main.py
```

Acesse: `http://localhost:8501`

---

## 📖 Instalação Detalhada

### 1. Instalando Python

#### Windows

1. Baixe o instalador em [python.org](https://www.python.org/downloads/)
2. Execute o instalador
3. ✅ **IMPORTANTE**: Marque "Add Python to PATH"
4. Clique em "Install Now"
5. Verifique a instalação:

```cmd
python --version
pip --version
```

#### macOS

```bash
# Usando Homebrew (recomendado)
brew install python@3.10

# Verificar
python3 --version
pip3 --version
```

#### Linux (Ubuntu/Debian)

```bash
# Atualizar repositórios
sudo apt update

# Instalar Python
sudo apt install python3.10 python3-pip python3-venv

# Verificar
python3 --version
pip3 --version
```

---

### 2. Instalando MySQL

#### Windows

1. Baixe o MySQL Installer em [mysql.com](https://dev.mysql.com/downloads/installer/)
2. Execute o instalador
3. Escolha "Developer Default"
4. Configure:
   - **Root Password**: Escolha uma senha forte
   - **Port**: 3306 (padrão)
5. Verifique:

```cmd
mysql --version
```

#### macOS

```bash
# Usando Homebrew
brew install mysql@8.0

# Iniciar o MySQL
brew services start mysql

# Configurar senha root
mysql_secure_installation

# Verificar
mysql --version
```

#### Linux (Ubuntu/Debian)

```bash
# Instalar
sudo apt update
sudo apt install mysql-server

# Iniciar serviço
sudo systemctl start mysql
sudo systemctl enable mysql

# Configurar
sudo mysql_secure_installation

# Verificar
mysql --version
```

#### Testar Conexão MySQL

```bash
# Conectar ao MySQL
mysql -u root -p

# No prompt do MySQL:
SHOW DATABASES;
EXIT;
```

---

### 3. Instalando Git

#### Windows

1. Baixe em [git-scm.com](https://git-scm.com/downloads)
2. Execute o instalador
3. Use as opções padrão
4. Verifique:

```cmd
git --version
```

#### macOS

```bash
# Usando Homebrew
brew install git

# Verificar
git --version
```

#### Linux

```bash
# Ubuntu/Debian
sudo apt install git

# Verificar
git --version
```

---

### 4. Clonando o Projeto

```bash
# Navegue até onde deseja clonar o projeto
cd ~/Projects  # Exemplo

# Clone o repositório
git clone https://github.com/giusfds/DaRua.git

# Entre no diretório
cd DaRua

# Verifique os arquivos
ls -la  # Linux/Mac
dir     # Windows
```

---

### 5. Instalando Dependências

#### Criar Ambiente Virtual

```bash
# Criar ambiente virtual (dentro do diretório DaRua)
python -m venv venv

# Ativar ambiente virtual

# Linux/Mac:
source venv/bin/activate

# Windows (CMD):
venv\Scripts\activate

# Windows (PowerShell):
venv\Scripts\Activate.ps1

# Verificar ativação (deve mostrar (venv) no prompt)
```

#### Instalar Pacotes Python

```bash
# Com o ambiente virtual ativado:
pip install -r requirements.txt

# Verificar instalação
pip list
```

#### Dependências Instaladas

```
streamlit==1.31.0         # Framework web
pandas==2.2.0             # Manipulação de dados
plotly==5.18.0            # Gráficos interativos
numpy==1.26.3             # Computação numérica
mysql-connector-python==8.2.0  # Driver MySQL
python-dotenv==1.0.0      # Variáveis de ambiente
```

---

### 6. Configurando Banco de Dados

#### Passo 1: Criar o Banco

```bash
# Conectar ao MySQL
mysql -u root -p

# No prompt do MySQL:
```

```sql
-- Criar banco de dados
CREATE DATABASE somos_darua
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Verificar
SHOW DATABASES;

-- Usar o banco
USE somos_darua;

-- Sair
EXIT;
```

#### Passo 2: Executar Script de Criação

```bash
# Opção 1: Via comando direto
mysql -u root -p somos_darua < database/schema/create_database.sql

# Opção 2: Via MySQL CLI
mysql -u root -p
```

```sql
USE somos_darua;
SOURCE /caminho/completo/para/DaRua/database/schema/create_database.sql;
```

#### Passo 3: Verificar Tabelas

```bash
mysql -u root -p somos_darua
```

```sql
-- Listar tabelas
SHOW TABLES;

-- Deve mostrar:
-- +------------------------+
-- | Tables_in_somos_darua  |
-- +------------------------+
-- | Associa                |
-- | Beneficiario           |
-- | CampanhaDoacao         |
-- | Contem                 |
-- | Doacao                 |
-- | Doador                 |
-- | Necessidade            |
-- | ObjetoDoavel           |
-- | PontoColeta            |
-- | Possui                 |
-- | Promove                |
-- | Recebe                 |
-- | Voluntario             |
-- +------------------------+

-- Ver estrutura de uma tabela
DESCRIBE Doador;

EXIT;
```

#### Passo 4: (Opcional) Inserir Dados de Teste

```bash
# Se houver arquivo de seeds
mysql -u root -p somos_darua < database/seeds/sample_data.sql
```

---

### 7. Configurando Variáveis de Ambiente

#### Criar arquivo .env

```bash
# Copiar exemplo
cp .env.example .env

# Editar .env
# Linux/Mac:
nano .env
# ou
vim .env

# Windows:
notepad .env
```

#### Configuração do .env

```env
# Banco de Dados MySQL
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha_aqui
DB_NAME=somos_darua
DB_PORT=3306

# Configurações da Aplicação
APP_ENV=development
DEBUG=True
SECRET_KEY=sua_chave_secreta_aqui

# Configurações Streamlit (opcional)
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
```

#### ⚠️ Importante

- Nunca commite o arquivo `.env` no Git
- Use senhas fortes
- Em produção, use `APP_ENV=production` e `DEBUG=False`

---

## ▶️ Executando o Sistema

### Primeira Execução

```bash
# Certifique-se de estar no diretório raiz do projeto
cd DaRua

# Ative o ambiente virtual
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Navegue até o diretório app
cd app

# Execute o Streamlit
streamlit run main.py
```

### Execução via Script

```bash
# Linux/Mac:
./run.sh

# Windows:
run.bat
```

### Saída Esperada

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.X:8501
```

### Acessar o Sistema

1. Abra seu navegador
2. Acesse: `http://localhost:8501`
3. Você verá o Dashboard do sistema

---

## 🐛 Troubleshooting

### Problema: Python não encontrado

```bash
# Windows
python --version
# Se não funcionar, tente:
py --version

# Linux/Mac
python3 --version
```

**Solução**: Reinstale o Python marcando "Add to PATH"

---

### Problema: pip não encontrado

```bash
# Linux/Mac
python3 -m pip --version

# Windows
python -m pip --version
```

**Solução**:

```bash
python -m ensurepip --upgrade
```

---

### Problema: Erro ao criar venv

```bash
# Linux/Mac - instalar venv
sudo apt install python3-venv

# Windows - usar virtualenv
pip install virtualenv
virtualenv venv
```

---

### Problema: Erro ao conectar MySQL

**Erro**: `Access denied for user 'root'@'localhost'`

**Solução**:

```bash
# Resetar senha do MySQL
mysql -u root

# No MySQL:
ALTER USER 'root'@'localhost' IDENTIFIED BY 'nova_senha';
FLUSH PRIVILEGES;
EXIT;
```

---

### Problema: Banco não existe

**Erro**: `Unknown database 'somos_darua'`

**Solução**:

```bash
mysql -u root -p

# No MySQL:
CREATE DATABASE somos_darua;
EXIT;

# Execute o script novamente
mysql -u root -p somos_darua < database/schema/create_database.sql
```

---

### Problema: Erro ao importar módulos

**Erro**: `ModuleNotFoundError: No module named 'streamlit'`

**Solução**:

```bash
# Certifique-se que o venv está ativado
# Reinstale as dependências
pip install -r requirements.txt
```

---

### Problema: Porta 8501 em uso

**Erro**: `Address already in use`

**Solução**:

```bash
# Opção 1: Usar outra porta
streamlit run main.py --server.port 8502

# Opção 2: Matar processo na porta 8501
# Linux/Mac:
lsof -ti:8501 | xargs kill -9

# Windows:
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

---

### Problema: Erro de codificação

**Erro**: `UnicodeDecodeError`

**Solução**:

```bash
# Certifique-se que o banco está em UTF-8
mysql -u root -p

# No MySQL:
ALTER DATABASE somos_darua
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

---

## 🌍 Ambientes

### Desenvolvimento

```env
APP_ENV=development
DEBUG=True
DB_HOST=localhost
```

```bash
# Executar
streamlit run main.py
```

### Produção

```env
APP_ENV=production
DEBUG=False
DB_HOST=seu_servidor_producao
```

```bash
# Executar com configurações de produção
streamlit run main.py --server.port 80 --server.address 0.0.0.0
```

---

## 📝 Checklist de Instalação

- [ ] Python 3.10+ instalado
- [ ] MySQL 8.0+ instalado e rodando
- [ ] Git instalado
- [ ] Repositório clonado
- [ ] Ambiente virtual criado e ativado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Banco de dados criado
- [ ] Tabelas criadas (script SQL executado)
- [ ] Arquivo `.env` configurado
- [ ] Sistema executado com sucesso
- [ ] Navegador acessando `localhost:8501`

---

## 🎉 Próximos Passos

Após a instalação bem-sucedida:

1. 📖 Leia a [Documentação Completa](./INDEX.md)
2. 🏗️ Entenda a [Arquitetura](./ARQUITETURA.md)
3. 💻 Consulte o [Guia de Desenvolvimento](./DESENVOLVIMENTO.md)
4. 🔌 Explore os [Models](./API.md)

---

## 🆘 Suporte

Se você encontrar problemas:

1. Consulte esta seção de Troubleshooting
2. Verifique a documentação no diretório `docs/`
3. Abra uma [issue no GitHub](https://github.com/giusfds/DaRua/issues)
4. Entre em contato com a equipe

---

## 🔄 Atualizando o Sistema

```bash
# Atualizar código
git pull origin main

# Atualizar dependências
pip install -r requirements.txt --upgrade

# Aplicar migrations (se houver)
mysql -u root -p somos_darua < database/migrations/nova_migration.sql

# Reiniciar aplicação
```

---

[⬅️ Voltar ao Índice](./INDEX.md)
