# 🤝 Somos DaRua - Sistema de Gestão de Doações

Sistema web desenvolvido como projeto extensionista para gerenciar doações, doadores, beneficiários, campanhas e voluntários de organizações sociais.

---

## 👥 Equipe

- **Giuseppe Cordeiro**
- **Pedro Henrique**
- **Pedro Tinoco**
- **Savio Faria**

---

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Arquitetura do Sistema](#arquitetura-do-sistema)
- [O Que Foi Implementado](#o-que-foi-implementado)
- [O Que Falta Implementar](#o-que-falta-implementar)
- [Instalação e Configuração](#instalação-e-configuração)
- [Como Rodar Localmente](#como-rodar-localmente)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Documentação Técnica](#documentação-técnica)
- [Contribuindo](#contribuindo)

---

## 🎯 Sobre o Projeto

O **Somos DaRua** é um sistema de gestão desenvolvido para facilitar o gerenciamento de doações em organizações sociais. O sistema permite:

- Cadastrar e gerenciar doadores
- Registrar beneficiários e suas necessidades
- Criar e acompanhar campanhas de arrecadação
- Gerenciar pontos de coleta
- Organizar equipes de voluntários
- Registrar e rastrear doações

### Problema que Resolve

Organizações sociais enfrentam dificuldades para:
- Rastrear histórico de doações
- Associar doações às necessidades dos beneficiários
- Coordenar logística de entrega
- Gerenciar múltiplas campanhas simultaneamente

Este sistema centraliza todas essas informações em uma plataforma web intuitiva e fácil de usar.

---

## 💻 Tecnologias Utilizadas

### Backend
- **Python 3.10+** - Linguagem principal
- **MySQL 8.0** - Banco de dados relacional
- **mysql-connector-python** - Driver Python para MySQL

### Frontend
- **Streamlit 1.28+** - Framework web para interface
- **Pandas** - Manipulação de dados
- **Plotly** - Visualizações e gráficos

### Outras Ferramentas
- **python-dotenv** - Gerenciamento de variáveis de ambiente
- **Git** - Controle de versão

---

## 🏗️ Arquitetura do Sistema

O projeto segue uma arquitetura de **3 camadas**:
```
┌─────────────────────────────────────────┐
│         FRONTEND (Streamlit)            │
│  - Interface do usuário                 │
│  - Páginas de cadastro e consulta       │
│  - Gráficos e visualizações             │
└──────────────┬──────────────────────────┘
               │
               │ Chamadas de métodos
               ▼
┌─────────────────────────────────────────┐
│       BACKEND (Modelos Python)          │
│  - Lógica de negócio                    │
│  - Validações                           │
│  - Métodos CRUD                         │
└──────────────┬──────────────────────────┘
               │
               │ Queries SQL
               ▼
┌─────────────────────────────────────────┐
│      BANCO DE DADOS (MySQL)             │
│  - 13 tabelas                           │
│  - Relacionamentos N:N                  │
│  - Integridade referencial              │
└─────────────────────────────────────────┘
```

### Fluxo de uma Operação
```
1. Usuário preenche formulário (Streamlit)
2. Frontend chama método do modelo (ex: doador.save())
3. Modelo valida dados
4. Modelo executa query SQL
5. MySQL armazena dados
6. Retorna confirmação
7. Frontend exibe mensagem de sucesso
```

---

## ✅ O Que Foi Implementado

### 📊 Banco de Dados (100%)

**13 Tabelas Criadas:**

#### Tabelas Principais (8)
1. **Doador** - Pessoas/empresas que fazem doações
2. **Beneficiario** - Pessoas que recebem doações
3. **Voluntario** - Pessoas que ajudam na organização
4. **PontoColeta** - Locais de coleta de doações
5. **CampanhaDoacao** - Campanhas de arrecadação
6. **ObjetoDoavel** - Itens que podem ser doados
7. **Necessidade** - Necessidades prioritárias
8. **Doacao** - Registro de doações realizadas

#### Tabelas de Relacionamento N:N (5)
1. **Contem** - Doacao ↔ ObjetoDoavel
2. **Recebe** - Beneficiario ↔ Doacao
3. **Possui** - Doacao ↔ Voluntario
4. **Promove** - CampanhaDoacao ↔ Necessidade
5. **Associa** - ObjetoDoavel ↔ CampanhaDoacao

### 🔧 Backend (100%)

**8 Modelos Completos com CRUD:**

Cada modelo possui:
- ✅ `save()` - Criar novo registro
- ✅ `update()` - Atualizar registro existente
- ✅ `delete()` - Remover registro
- ✅ `get_by_id()` - Buscar por ID
- ✅ `get_all()` - Listar todos
- ✅ `validate()` - Validar dados
- ✅ `to_dict()` - Converter para dicionário

**Recursos Avançados:**
- ✅ Prepared statements (segurança contra SQL Injection)
- ✅ Context managers (gerenciamento automático de conexões)
- ✅ Tratamento de erros robusto
- ✅ Relacionamentos N:N (ex: doacao.adicionar_objeto())

### 🎨 Frontend (80%)

**Páginas Implementadas:**

| Página | Status | Funcionalidades |
|--------|--------|----------------|
| **Dashboard** | ⚠️ Parcial | Gráficos e métricas (dados mockados) |
| **Doadores** | ✅ Completo | Cadastrar, listar, buscar |
| **Beneficiários** | ✅ Completo | Cadastrar, listar, buscar, filtrar |
| **Doações** | ⚠️ Parcial | Cadastrar doação básica |
| **Campanhas** | ✅ Completo | Cadastrar, listar, filtrar |
| **Pontos de Coleta** | ✅ Completo | Cadastrar, listar, buscar |
| **Voluntários** | ✅ Completo | Cadastrar, listar, buscar, filtrar |
| **Relatórios** | ❌ Não iniciado | - |

**Recursos de Interface:**
- ✅ Navegação por sidebar
- ✅ Tema visual consistente (dark theme roxo)
- ✅ Formulários responsivos
- ✅ Mensagens de feedback (sucesso/erro)
- ✅ Busca em tempo real
- ✅ Filtros e ordenação
- ✅ Tabelas formatadas
- ✅ Validações de formulário

---

## 🚧 O Que Falta Implementar

### 🔴 Alta Prioridade

#### 1. Editar Registros (3-4 horas)
**Onde:** Todas as páginas  
**O que falta:** Botão "✏️ Editar" está presente mas não funciona

**Implementação necessária:**
```python
# Carregar dados existentes
doador = Doador.get_by_id(id_selecionado)

# Formulário preenchido com valores atuais
nome = st.text_input("Nome", value=doador.nome)

# Salvar alterações
doador.nome = nome
doador.update()
```

**Páginas afetadas:** Todas

---

#### 2. Deletar Registros (2-3 horas)
**Onde:** Todas as páginas  
**O que falta:** Funcionalidade de exclusão

**Implementação necessária:**
- Confirmação antes de deletar
- Tratar relacionamentos (CASCADE/SET NULL)
- Verificar se pode deletar (não tem dependências)

**Exemplo:**
```python
if st.button("🗑️ Deletar"):
    if confirmar_exclusao():
        doador.delete()
```

---

#### 3. Dashboard com Dados Reais (30 minutos)
**Onde:** `app/main.py`  
**O que falta:** Substituir dados mockados por queries reais

**Implementação necessária:**
```python
# ATUAL (mock)
metricas = get_metricas_dashboard()

# NOVO (real)
total_doadores = len(Doador.get_all())
total_beneficiarios = len(Beneficiario.get_all())
```

---

#### 4. Doações Completas (1-2 horas)
**Onde:** `app/pages/4_doacoes.py`  
**O que falta:** Salvar todos os detalhes da doação

**Campos não salvos:**
- Tipo de doação (Alimentos, Roupas, etc.)
- Item/descrição detalhada
- Quantidade e unidade
- Ponto de coleta
- Objetos doáveis relacionados

**Implementação necessária:**
```python
# Criar objeto doável
objeto = ObjetoDoavel(nome=item, categoria=tipo)
objeto.save()

# Relacionar com doação
doacao.adicionar_objeto(objeto.idObjetoDoavel)
```

---

### 🟡 Média Prioridade

#### 5. Detalhes/Visualização Completa (2-3 horas)
Botão "👁️ Detalhes" presente mas não implementado

**Funcionalidades:**
- Modal ou página com todos os dados
- Histórico de doações (para doadores)
- Lista de campanhas ativas
- Relacionamentos

---

#### 6. Métricas Reais (2 horas)
Várias métricas mostram "-" ou valores fixos

**Exemplos:**
- "Cadastros este mês" (todas páginas)
- "Média de doações por doador"
- Progresso real de campanhas
- Total arrecadado por campanha

---

#### 7. Relatórios (5-6 horas)
Página existe (`8_relatorios.py`) mas não foi implementada

**Funcionalidades necessárias:**
- Relatório de doações por período
- Doadores mais ativos
- Beneficiários atendidos
- Progresso de campanhas
- Exportar PDF/Excel

---

#### 8. Validações Avançadas (2-3 horas)
**Validações necessárias:**
- CPF (formato e dígito verificador)
- Email (regex)
- Telefone (formato brasileiro)
- CEP (consultar API ViaCEP)
- Impedir duplicatas

---

### 🟢 Baixa Prioridade

#### 9. Autenticação (6-8 horas)
Sistema de login e controle de acesso

#### 10. Notificações (4-5 horas)
Email/WhatsApp para eventos importantes

#### 11. Upload de Arquivos (3-4 horas)
Fotos de doadores, documentos, etc.

#### 12. Auditoria (3-4 horas)
Histórico de alterações

---

## 🚀 Instalação e Configuração

### Pré-requisitos

- **Python 3.10 ou superior**
- **MySQL 8.0 ou superior**
- **Git**

### Verificar Instalações
```bash
# Verificar Python
python3 --version

# Verificar MySQL
mysql --version

# Verificar Git
git --version
```

---

## 📥 Como Rodar Localmente

### 1️⃣ Clonar o Repositório
```bash
# Clonar via HTTPS
git clone https://github.com/seu-usuario/somos-darua.git

# OU via SSH
git clone git@github.com:seu-usuario/somos-darua.git

# Entrar na pasta
cd somos-darua
```

---

### 2️⃣ Configurar Ambiente Virtual
```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
# No Linux/Mac:
source venv/bin/activate

# No Windows:
venv\Scripts\activate

# Você deve ver (venv) no início do terminal
```

---

### 3️⃣ Instalar Dependências
```bash
# Instalar todas as dependências
pip install -r requirements.txt

# Verificar instalação
pip list
```

**Dependências principais:**
```
streamlit==1.28.0
pandas==2.0.3
mysql-connector-python==8.2.0
python-dotenv==1.0.0
plotly==5.17.0
```

---

### 4️⃣ Configurar Banco de Dados

#### 4.1 Criar usuário MySQL (se necessário)
```bash
# Conectar ao MySQL como root
mysql -u root -p

# Criar usuário (opcional)
CREATE USER 'darua_user'@'localhost' IDENTIFIED BY 'senha_segura';
GRANT ALL PRIVILEGES ON somos_darua.* TO 'darua_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

#### 4.2 Configurar arquivo .env
```bash
# Criar arquivo .env na raiz do projeto
nano .env
```

**Cole este conteúdo (ajuste com suas credenciais):**
```env
# Configurações do Banco de Dados
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha_aqui
DB_NAME=somos_darua
DB_PORT=3306
```

**⚠️ IMPORTANTE:** Troque `sua_senha_aqui` pela senha do seu MySQL!

#### 4.3 Criar o banco de dados
```bash
# Executar script de setup
python3 backend/database/setup.py
```

**Menu que aparecerá:**
```
1. Criar/Recriar banco de dados
2. Sair

Escolha uma opção: 1
Continuar? (s/n): s
```

**Resultado esperado:**
```
✅ SETUP CONCLUÍDO COM SUCESSO!

📊 Resumo:
   • Banco: somos_darua
   • Tabelas: 13
```

---

### 5️⃣ Testar Conexão
```bash
# Testar se a conexão está funcionando
python3 backend/database/connection.py
```

**Resultado esperado:**
```
✅ CONEXÃO OK!
✓ Banco atual: somos_darua
✓ Versão MySQL: 8.0.xx
```

---

### 6️⃣ Rodar o Sistema
```bash
# Rodar aplicação Streamlit
streamlit run app/main.py
```

**O navegador deve abrir automaticamente em:**
```
http://localhost:8501
```

**Se não abrir, acesse manualmente esse endereço.**

---

### 7️⃣ Testar Funcionalidades

#### Teste Rápido (5 minutos)

1. **Dashboard** - Deve aparecer gráficos (dados mockados)
2. **Doadores** - Cadastre "João Silva"
3. **Beneficiários** - Cadastre "Maria Santos"
4. **Campanhas** - Crie "Natal 2025"
5. **Pontos de Coleta** - Cadastre um ponto
6. **Voluntários** - Cadastre "Ana Costa"
7. **Doações** - Registre uma doação (use doador cadastrado)

#### Verificar no Banco
```bash
# Conectar ao MySQL
mysql -u root -p

# Usar banco
USE somos_darua;

# Ver doadores cadastrados
SELECT * FROM Doador;

# Ver beneficiários
SELECT * FROM Beneficiario;

# Sair
EXIT;
```

---

## 📁 Estrutura do Projeto
```
somos-darua/
│
├── app/                          # Frontend Streamlit
│   ├── pages/                    # Páginas da aplicação
│   │   ├── 2_doadores.py        # Gestão de doadores
│   │   ├── 3_beneficiarios.py   # Gestão de beneficiários
│   │   ├── 4_doacoes.py         # Registro de doações
│   │   ├── 5_campanhas.py       # Gestão de campanhas
│   │   ├── 6_pontos_coleta.py   # Pontos de coleta
│   │   ├── 7_voluntarios.py     # Gestão de voluntários
│   │   └── 8_relatorios.py      # Relatórios (não implementado)
│   │
│   ├── utils/                    # Utilitários
│   │   ├── config.py            # Configurações globais
│   │   └── mock_data.py         # Dados mockados (temporário)
│   │
│   └── main.py                   # Dashboard principal
│
├── backend/                      # Backend Python
│   ├── database/                # Camada de dados
│   │   ├── connection.py        # Gerenciador de conexões
│   │   └── setup.py             # Script de criação do banco
│   │
│   └── models/                  # Modelos de dados (ORM)
│       ├── doador.py            # Modelo Doador
│       ├── beneficiario.py      # Modelo Beneficiario
│       ├── voluntario.py        # Modelo Voluntario
│       ├── ponto_coleta.py      # Modelo PontoColeta
│       ├── campanha_doacao.py   # Modelo CampanhaDoacao
│       ├── objeto_doavel.py     # Modelo ObjetoDoavel
│       ├── necessidade.py       # Modelo Necessidade
│       └── doacao.py            # Modelo Doacao (relacionamentos)
│
├── database/                     # Scripts SQL
│   └── schema/
│       └── create_database.sql  # Schema completo do banco
│
├── venv/                        # Ambiente virtual (não commitado)
│
├── .env                         # Variáveis de ambiente (não commitado)
├── .gitignore                   # Arquivos ignorados pelo Git
├── requirements.txt             # Dependências Python
└── README.md                    # Este arquivo
```

---

## 📚 Documentação Técnica

### Modelos (Backend)

#### Exemplo: Modelo Doador
```python
class Doador:
    """
    Representa um doador no sistema
    
    Atributos:
        idDoador: ID único (auto-incremento)
        nome: Nome completo (obrigatório)
        telefone: Telefone de contato
        email: Email
        logradouro, numero, complemento: Endereço
        bairro, cidade, estado, cep: Localização
    """
    
    def __init__(self, nome, telefone=None, email=None, ...):
        self.nome = nome
        # ... outros atributos
    
    def save(self) -> bool:
        """Salva novo doador no banco"""
        # Validação
        # INSERT no MySQL
        # Retorna True/False
    
    def update(self) -> bool:
        """Atualiza doador existente"""
        # UPDATE no MySQL
    
    def delete(self) -> bool:
        """Remove doador"""
        # DELETE do MySQL
    
    @staticmethod
    def get_all() -> List['Doador']:
        """Retorna todos os doadores"""
        # SELECT * FROM Doador
    
    @staticmethod
    def get_by_id(id) -> Doador:
        """Busca doador por ID"""
        # SELECT WHERE idDoador = ?
```

### Relacionamentos N:N

#### Exemplo: Doação com Objetos
```python
# 1. Criar doação
doacao = Doacao(doador_id=1, data_criacao=date.today())
doacao.save()

# 2. Adicionar objetos à doação
doacao.adicionar_objeto(objeto_id=5)  # Arroz
doacao.adicionar_objeto(objeto_id=8)  # Feijão

# 3. Buscar objetos da doação
objetos = doacao.get_objetos()
```

**SQL gerado:**
```sql
-- Tabela de relacionamento
INSERT INTO Contem (Doacao_idDoacao, ObjetoDoavel_idObjetoDoavel)
VALUES (1, 5), (1, 8);
```

---

## 🐛 Troubleshooting

### Erro: "Access denied for user"
```bash
# Verificar senha no .env
cat .env

# Testar conexão direta
mysql -u root -p
```

**Solução:** Corrigir senha no arquivo `.env`

---

### Erro: "ModuleNotFoundError: No module named 'streamlit'"
```bash
# Verificar se venv está ativado
which python3

# Deve mostrar: .../somos-darua/venv/bin/python3

# Se não, ativar:
source venv/bin/activate

# Reinstalar:
pip install -r requirements.txt
```

---

### Erro: "Database doesn't exist"
```bash
# Recriar banco
python3 backend/database/setup.py

# Escolher opção 1
```

---

### Erro: "Address already in use"
```bash
# Matar processos Streamlit
pkill -f streamlit

# Ou especificar porta diferente
streamlit run app/main.py --server.port 8502
```

---

### Banco não aparece no MySQL Workbench
```bash
# Conectar via terminal
mysql -u root -p

# Ver bancos
SHOW DATABASES;

# Se não aparecer, rodar setup novamente
```

---

## 🤝 Contribuindo

### Fluxo de Trabalho

1. **Criar branch para sua funcionalidade**
```bash
git checkout -b feature/nome-funcionalidade
```

2. **Fazer alterações**
```bash
# Editar arquivos
# Testar localmente
```

3. **Commitar mudanças**
```bash
git add .
git commit -m "Adiciona funcionalidade X"
```

4. **Push para repositório**
```bash
git push origin feature/nome-funcionalidade
```

5. **Criar Pull Request**
- Ir no GitHub
- Criar Pull Request da sua branch para main
- Descrever o que foi feito
- Solicitar review dos colegas

---

### Padrões de Código

#### Commits
```bash
# Bons exemplos:
git commit -m "Adiciona validação de CPF no cadastro de doadores"
git commit -m "Corrige bug na busca de beneficiários"
git commit -m "Implementa edição de campanhas"

# Evitar:
git commit -m "fix"
git commit -m "alterações"
```

#### Nomenclatura
- **Variáveis:** snake_case (`nome_completo`, `data_cadastro`)
- **Classes:** PascalCase (`Doador`, `CampanhaDoacao`)
- **Funções:** snake_case (`get_all()`, `calcular_total()`)
- **Constantes:** UPPER_CASE (`DB_HOST`, `MAX_RETRIES`)

---

## 📞 Contato e Suporte

### Membros do Grupo

- **Giuseppe Cordeiro** - [email/contato]
- **Pedro Henrique** - [email/contato]
- **Pedro Tinoco** - [email/contato]
- **Savio Faria** - [email/contato]

### Reportar Problemas

1. **Verificar se já não foi reportado** - Ver Issues no GitHub
2. **Criar nova Issue** - Descrever problema detalhadamente
3. **Incluir:**
   - Mensagem de erro completa
   - Passos para reproduzir
   - Sistema operacional
   - Versão do Python

---

## 📄 Licença

Este projeto foi desenvolvido como trabalho acadêmico para fins educacionais.

---

## 🎓 Agradecimentos

- Professores e orientadores do curso
- Comunidade open-source (Streamlit, Python, MySQL)
- Organização "Somos DaRua" (fictícia) que inspirou o projeto

---

## 📊 Status do Projeto
```
Progresso Geral: ████████░░ 80%

✅ Banco de Dados:     ██████████ 100%
✅ Backend:            ██████████ 100%
⚠️  Frontend:          ████████░░  80%
❌ Relatórios:         ░░░░░░░░░░   0%
⚠️  Testes:            ██░░░░░░░░  20%
```

**Última atualização:** Novembro 2025

---

## 🚀 Roadmap

### Versão 1.0 (MVP) - ✅ Concluída
- [x] Banco de dados completo
- [x] Modelos backend com CRUD
- [x] Interface básica funcional
- [x] Cadastros e listagens

### Versão 1.1 (Em Desenvolvimento)
- [ ] Dashboard com dados reais
- [ ] Edição de registros
- [ ] Deleção de registros
- [ ] Doações completas

### Versão 2.0 (Futuro)
- [ ] Sistema de relatórios
- [ ] Autenticação e permissões
- [ ] Notificações por email
- [ ] Upload de arquivos
- [ ] API REST

---

**Desenvolvido com ❤️ pela equipe Somos DaRua**