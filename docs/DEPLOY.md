# 🚀 Guia de Deploy - Somos DaRua

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Pré-requisitos](#pré-requisitos)
- [Ambientes](#ambientes)
- [Deploy em Servidor Linux](#deploy-em-servidor-linux)
- [Deploy com Docker](#deploy-com-docker)
- [Deploy no Streamlit Cloud](#deploy-no-streamlit-cloud)
- [Configurações de Produção](#configurações-de-produção)
- [Segurança](#segurança)
- [Backup e Recuperação](#backup-e-recuperação)
- [Monitoramento](#monitoramento)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Visão Geral

Este guia fornece instruções detalhadas para fazer deploy do sistema Somos DaRua em ambiente de produção.

### Opções de Deploy

| Opção               | Complexidade | Custo      | Recomendado para    |
| ------------------- | ------------ | ---------- | ------------------- |
| **Servidor Linux**  | Média        | $          | Controle total      |
| **Docker**          | Média        | $$         | Portabilidade       |
| **Streamlit Cloud** | Baixa        | Gratuito/$ | Testes/MVP          |
| **AWS/Azure/GCP**   | Alta         | $$$        | Produção enterprise |

---

## ✅ Pré-requisitos

### Infraestrutura

- **Servidor**: VPS ou dedicado com Ubuntu 20.04+ / Debian 11+
- **RAM**: Mínimo 2 GB (recomendado 4 GB+)
- **CPU**: 2 cores ou mais
- **Disco**: 20 GB+ SSD
- **Conexão**: Banda larga estável

### Domínio e SSL

- Domínio registrado (ex: `somos darua.org`)
- Certificado SSL (recomendado: Let's Encrypt gratuito)

### Acesso

- Acesso SSH ao servidor
- Permissões de sudo

---

## 🌍 Ambientes

### Estrutura Recomendada

```
Desenvolvimento (Local)
    ↓
Homologação (Staging)
    ↓
Produção (Production)
```

### Variáveis por Ambiente

| Variável    | Desenvolvimento | Homologação         | Produção         |
| ----------- | --------------- | ------------------- | ---------------- |
| `DB_HOST`   | localhost       | db-staging          | db-prod          |
| `DB_NAME`   | somos_darua     | somos_darua_staging | somos_darua_prod |
| `DEBUG`     | True            | True                | False            |
| `LOG_LEVEL` | DEBUG           | INFO                | WARNING          |

---

## 🐧 Deploy em Servidor Linux

### Passo 1: Preparar Servidor

#### Atualizar Sistema

```bash
sudo apt update && sudo apt upgrade -y
```

#### Instalar Dependências

```bash
# Python 3.10+
sudo apt install python3.10 python3.10-venv python3-pip -y

# MySQL
sudo apt install mysql-server -y

# Nginx (opcional, para proxy reverso)
sudo apt install nginx -y

# Supervisor (para manter Streamlit rodando)
sudo apt install supervisor -y

# Git
sudo apt install git -y
```

---

### Passo 2: Configurar MySQL

```bash
# Secure installation
sudo mysql_secure_installation

# Acessar MySQL
sudo mysql

# Criar usuário e banco
CREATE DATABASE somos_darua_prod CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'somos_darua'@'localhost' IDENTIFIED BY 'senha_forte_aqui';
GRANT ALL PRIVILEGES ON somos_darua_prod.* TO 'somos_darua'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

---

### Passo 3: Clonar Projeto

```bash
# Criar diretório
sudo mkdir -p /var/www
cd /var/www

# Clonar repositório
sudo git clone https://github.com/giusfds/DaRua.git somos-darua
cd somos-darua

# Alterar proprietário
sudo chown -R $USER:$USER /var/www/somos-darua
```

---

### Passo 4: Configurar Ambiente Virtual

```bash
# Criar venv
python3 -m venv venv

# Ativar
source venv/bin/activate

# Instalar dependências
pip install --upgrade pip
pip install -r requirements.txt
```

---

### Passo 5: Configurar Variáveis de Ambiente

```bash
# Criar .env de produção
nano .env.production

# Adicionar variáveis
DB_HOST=localhost
DB_USER=somos_darua
DB_PASSWORD=senha_forte_aqui
DB_NAME=somos_darua_prod
DB_PORT=3306

APP_ENV=production
DEBUG=False
LOG_LEVEL=INFO

# Salvar e sair (Ctrl+O, Enter, Ctrl+X)

# Copiar para .env
cp .env.production .env
```

---

### Passo 6: Criar Banco de Dados

```bash
# Executar script de criação
mysql -u somos_darua -p somos_darua_prod < database/schema/create_database.sql

# Executar migrations
mysql -u somos_darua -p somos_darua_prod < database/migrations/add_doacoes_detalhes.sql
mysql -u somos_darua -p somos_darua_prod < database/migrations/add_fks_doacoes.sql
mysql -u somos_darua -p somos_darua_prod < database/migrations/add_meta_campanhas.sql

# Testar conexão
python backend/database/connection.py
```

---

### Passo 7: Configurar Supervisor

Supervisor mantém o Streamlit rodando como serviço.

```bash
# Criar arquivo de configuração
sudo nano /etc/supervisor/conf.d/somos-darua.conf
```

Adicionar conteúdo:

```ini
[program:somos-darua]
directory=/var/www/somos-darua
command=/var/www/somos-darua/venv/bin/streamlit run app/main.py --server.port=8501 --server.address=0.0.0.0
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/somos-darua/error.log
stdout_logfile=/var/log/somos-darua/access.log
environment=PATH="/var/www/somos-darua/venv/bin"
```

Salvar e sair.

```bash
# Criar diretório de logs
sudo mkdir -p /var/log/somos-darua
sudo chown www-data:www-data /var/log/somos-darua

# Recarregar Supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start somos-darua

# Verificar status
sudo supervisorctl status somos-darua
```

---

### Passo 8: Configurar Nginx (Opcional)

Nginx serve como proxy reverso para o Streamlit.

```bash
# Criar arquivo de configuração
sudo nano /etc/nginx/sites-available/somos-darua
```

Adicionar:

```nginx
server {
    listen 80;
    server_name seudominio.com.br www.seudominio.com.br;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Salvar e sair.

```bash
# Criar link simbólico
sudo ln -s /etc/nginx/sites-available/somos-darua /etc/nginx/sites-enabled/

# Testar configuração
sudo nginx -t

# Reiniciar Nginx
sudo systemctl restart nginx
```

---

### Passo 9: Configurar SSL com Let's Encrypt

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obter certificado
sudo certbot --nginx -d seudominio.com.br -d www.seudominio.com.br

# Renovação automática (já configurada)
sudo certbot renew --dry-run
```

---

## 🐳 Deploy com Docker

### Dockerfile

Criar `Dockerfile` na raiz:

```dockerfile
FROM python:3.10-slim

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Diretório de trabalho
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Porta exposta
EXPOSE 8501

# Comando de inicialização
CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### docker-compose.yml

```yaml
version: "3.8"

services:
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - DB_HOST=db
      - DB_USER=root
      - DB_PASSWORD=${DB_PASSWORD}
      - DB_NAME=somos_darua_prod
      - DB_PORT=3306
    depends_on:
      - db
    restart: unless-stopped
    volumes:
      - ./app:/app/app
      - ./backend:/app/backend

  db:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=${DB_PASSWORD}
      - MYSQL_DATABASE=somos_darua_prod
    ports:
      - "3306:3306"
    volumes:
      - db_data:/var/lib/mysql
      - ./database/schema:/docker-entrypoint-initdb.d
    restart: unless-stopped

volumes:
  db_data:
```

### Executar com Docker

```bash
# Build e iniciar
docker-compose up -d --build

# Ver logs
docker-compose logs -f app

# Parar
docker-compose down

# Parar e remover volumes
docker-compose down -v
```

---

## ☁️ Deploy no Streamlit Cloud

### Passo 1: Preparar Repositório

1. Garantir que o repositório está no GitHub
2. Adicionar `requirements.txt` atualizado
3. Criar `.streamlit/config.toml`:

```toml
[server]
headless = true
port = 8501

[theme]
primaryColor = "#A78BFA"
backgroundColor = "#0F172A"
secondaryBackgroundColor = "#1E293B"
textColor = "#F8FAFC"
```

### Passo 2: Configurar Secrets

No Streamlit Cloud, adicionar secrets:

```toml
[mysql]
host = "seu-host-mysql.com"
port = 3306
database = "somos_darua_prod"
user = "seu_usuario"
password = "sua_senha"
```

### Passo 3: Fazer Deploy

1. Acesse [share.streamlit.io](https://share.streamlit.io/)
2. Conecte sua conta GitHub
3. Selecione o repositório `DaRua`
4. Escolha branch (main) e arquivo principal (`app/main.py`)
5. Clique em "Deploy"

---

## ⚙️ Configurações de Produção

### Otimizações

#### 1. Streamlit Config

Criar `.streamlit/config.toml`:

```toml
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false

[runner]
magicEnabled = false
fastReruns = true
```

#### 2. MySQL Tuning

```sql
-- /etc/mysql/mysql.conf.d/mysqld.cnf
[mysqld]
max_connections = 200
innodb_buffer_pool_size = 1G
innodb_log_file_size = 256M
query_cache_type = 1
query_cache_size = 64M
```

Reiniciar MySQL:

```bash
sudo systemctl restart mysql
```

---

## 🔒 Segurança

### 1. Firewall

```bash
# Configurar UFW
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
sudo ufw status
```

### 2. Senhas Fortes

- MySQL: mínimo 16 caracteres
- Sistema: mínimo 16 caracteres
- Usar gerenciador de senhas

### 3. Atualizações Automáticas

```bash
# Instalar unattended-upgrades
sudo apt install unattended-upgrades -y

# Configurar
sudo dpkg-reconfigure -plow unattended-upgrades
```

### 4. Fail2Ban

```bash
# Instalar
sudo apt install fail2ban -y

# Configurar
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo nano /etc/fail2ban/jail.local

# Reiniciar
sudo systemctl restart fail2ban
```

### 5. Ocultar Informações do Servidor

```nginx
# /etc/nginx/nginx.conf
http {
    server_tokens off;
}
```

---

## 💾 Backup e Recuperação

### Backup Automático de Banco

Criar script `/usr/local/bin/backup-somos-darua.sh`:

```bash
#!/bin/bash

# Configurações
DB_NAME="somos_darua_prod"
DB_USER="somos_darua"
DB_PASS="sua_senha"
BACKUP_DIR="/var/backups/somos-darua"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

# Criar diretório se não existir
mkdir -p $BACKUP_DIR

# Fazer backup
mysqldump -u$DB_USER -p$DB_PASS $DB_NAME | gzip > $BACKUP_DIR/backup_$DATE.sql.gz

# Remover backups antigos
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +$RETENTION_DAYS -delete

echo "Backup completed: backup_$DATE.sql.gz"
```

Tornar executável:

```bash
sudo chmod +x /usr/local/bin/backup-somos-darua.sh
```

Agendar no cron (diário às 2h):

```bash
sudo crontab -e

# Adicionar linha:
0 2 * * * /usr/local/bin/backup-somos-darua.sh >> /var/log/somos-darua/backup.log 2>&1
```

### Restaurar Backup

```bash
# Descompactar e restaurar
gunzip < /var/backups/somos-darua/backup_20240101_020000.sql.gz | mysql -u somos_darua -p somos_darua_prod
```

---

## 📊 Monitoramento

### 1. Logs

```bash
# Logs do Streamlit (Supervisor)
sudo tail -f /var/log/somos-darua/access.log
sudo tail -f /var/log/somos-darua/error.log

# Logs do Nginx
sudo tail -f /var/nginx/access.log
sudo tail -f /var/nginx/error.log

# Logs do MySQL
sudo tail -f /var/log/mysql/error.log
```

### 2. Uptime Monitoring

Usar serviços como:

- [UptimeRobot](https://uptimerobot.com/) (gratuito)
- [Pingdom](https://www.pingdom.com/)
- [StatusCake](https://www.statuscake.com/)

### 3. Performance

```bash
# Instalar htop
sudo apt install htop -y

# Monitorar recursos
htop

# Monitorar MySQL
mysqladmin -u root -p status
mysqladmin -u root -p extended-status
```

---

## 🐛 Troubleshooting

### Problema: Streamlit não inicia

```bash
# Verificar logs
sudo supervisorctl tail somos-darua stderr

# Verificar status
sudo supervisorctl status somos-darua

# Reiniciar
sudo supervisorctl restart somos-darua
```

### Problema: Erro de conexão com MySQL

```bash
# Verificar se MySQL está rodando
sudo systemctl status mysql

# Testar conexão
mysql -u somos_darua -p

# Verificar variáveis de ambiente
cat .env
```

### Problema: Nginx retorna 502

```bash
# Verificar se Streamlit está rodando
curl http://localhost:8501

# Verificar configuração do Nginx
sudo nginx -t

# Reiniciar Nginx
sudo systemctl restart nginx
```

### Problema: SSL não funciona

```bash
# Verificar certificado
sudo certbot certificates

# Renovar manualmente
sudo certbot renew

# Reiniciar Nginx
sudo systemctl restart nginx
```

---

## 📋 Checklist de Deploy

- [ ] Servidor configurado e atualizado
- [ ] MySQL instalado e seguro
- [ ] Banco de dados criado e populado
- [ ] Projeto clonado e dependências instaladas
- [ ] Variáveis de ambiente configuradas
- [ ] Supervisor configurado e rodando
- [ ] Nginx configurado como proxy reverso
- [ ] SSL configurado com Let's Encrypt
- [ ] Firewall ativado
- [ ] Backup automático configurado
- [ ] Monitoramento configurado
- [ ] Logs sendo armazenados
- [ ] Testes em produção realizados
- [ ] Documentação atualizada

---

## 📚 Recursos Adicionais

- [Streamlit Deployment](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Let's Encrypt](https://letsencrypt.org/)
- [Docker Documentation](https://docs.docker.com/)
- [MySQL Performance Tuning](https://dev.mysql.com/doc/refman/8.0/en/optimization.html)

---

[⬅️ Voltar ao Índice](./INDEX.md)
