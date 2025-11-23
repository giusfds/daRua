# ⚡ Instalação Rápida - Somos DaRua

Guia rápido para rodar o projeto localmente em **menos de 10 minutos**.

---

## ✅ Checklist Pré-requisitos

- [ ] Python 3.10+ instalado
- [ ] MySQL 8.0+ instalado e rodando
- [ ] Git instalado

---

## 🚀 Instalação em 6 Passos

### 1. Clonar Repositório
```bash
git clone https://github.com/seu-usuario/somos-darua.git
cd somos-darua
```

### 2. Criar Ambiente Virtual
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar .env
```bash
# Criar arquivo .env
echo "DB_HOST=localhost
DB_USER=root
DB_PASSWORD=SUA_SENHA_AQUI
DB_NAME=somos_darua
DB_PORT=3306" > .env

# ⚠️ Editar e colocar sua senha:
nano .env
```

### 5. Criar Banco de Dados
```bash
python3 backend/database/setup.py
# Escolha opção 1 e confirme com 's'
```

### 6. Rodar Sistema
```bash
streamlit run app/main.py
```

**Pronto! Acesse:** http://localhost:8501

---

## 🧪 Teste Rápido

1. Dashboard deve abrir automaticamente
2. Clique em "Doadores" no menu lateral
3. Cadastre um doador teste
4. Verifique se aparece na lista

✅ Se funcionou, está tudo pronto!

---

## 🐛 Problemas?

**Erro de senha MySQL:**
```bash
nano .env  # Corrigir DB_PASSWORD
```

**Porta 8501 ocupada:**
```bash
streamlit run app/main.py --server.port 8502
```

**Banco não criado:**
```bash
python3 backend/database/setup.py
```

---

**Documentação completa:** Ver [UltimaAtualizacao.md](UltimaAtualizacao.md)