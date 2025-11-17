# 📚 Guia do Repositório - Somos DaRua

**Bem-vindo ao repositório do projeto Somos DaRua!**  
Este guia vai te ajudar a entender a organização do projeto e como trabalhar nele.

---

## 👥 Equipe
- Giuseppe Cordeiro
- Pedro Henrique  
- Pedro Tinoco
- Savio Faria

---

## 🎯 Sobre o Projeto

Sistema de gestão de doações para organizações sociais que atendem pessoas em situação de vulnerabilidade. O projeto conecta doadores, beneficiários, voluntários e campanhas de forma eficiente.

### Tecnologias Utilizadas
- **Frontend**: Streamlit (Python)
- **Backend**: Python 3.10+
- **Banco de Dados**: MySQL 8.0
- **Prototipação**: Figma

---

## 📁 Estrutura do Repositório

```
somos-darua/
│
├── 📱 app/                          → INTERFACE DO USUÁRIO (STREAMLIT)
│   ├── main.py                      → Arquivo principal da aplicação
│   ├── pages/                       → Páginas específicas (doadores, campanhas, etc)
│   └── components/                  → Componentes reutilizáveis (formulários, cards, etc)
│
├── 🔧 backend/                      → LÓGICA DE NEGÓCIO E DADOS
│   ├── models/                      → Classes que representam as tabelas do BD
│   │   ├── base_model.py           → Classe base com operações CRUD
│   │   ├── doador.py               → Model de Doador
│   │   ├── beneficiario.py         → Model de Beneficiário
│   │   └── ...                     → Outros models
│   │
│   ├── services/                    → Regras de negócio complexas
│   │   └── doacao_service.py       → Ex: Criar doação com múltiplos objetos
│   │
│   └── database/                    → Configuração do banco de dados
│       ├── connection.py            → Gerenciador de conexões MySQL
│       └── setup.py                 → Script para criar/resetar o banco
│
├── 🗄️ database/                     → SCRIPTS SQL
│   ├── schema/                      → DDL - Criação de tabelas
│   │   └── 01_create_tables.sql    → Script principal de criação
│   │
│   ├── seeds/                       → Dados iniciais/exemplo
│   │   └── 01_sample_data.sql      → Inserts de exemplo
│   │
│   └── migrations/                  → Alterações futuras no schema
│       └── [versões futuras]
│
├── 📖 docs/                         → DOCUMENTAÇÃO
│   ├── QUICKSTART.md               → Como começar rapidamente
│   ├── DEVELOPMENT.md              → Guia de desenvolvimento
│   ├── diagramas/                  → ER, Relacional, etc
│   └── figma/                      → Links e referências do Figma
│
├── ⚙️ config/                       → ARQUIVOS DE CONFIGURAÇÃO
│   └── [configs futuras]
│
├── 🧪 tests/                        → TESTES AUTOMATIZADOS
│   └── [testes futuros]
│
├── 🎨 assets/                       → RECURSOS (IMAGENS, ÍCONES)
│   ├── images/
│   └── icons/
│
├── 📄 .env.example                  → Exemplo de variáveis de ambiente
├── 📄 .gitignore                    → Arquivos ignorados pelo Git
├── 📄 requirements.txt              → Dependências Python
└── 📄 README.md                     → Documentação principal do projeto
```

---

## 🗂️ Entendendo Cada Diretório

### 📱 `/app` - Interface do Usuário

**Responsável por**: Tudo que o usuário vê e interage

**Principais arquivos**:
- `main.py`: Ponto de entrada da aplicação, dashboard principal
- `pages/`: Cada arquivo aqui é uma página do sistema
  - `doadores.py`: Gestão de doadores
  - `beneficiarios.py`: Gestão de beneficiários
  - `doacoes.py`: Registro de doações
  - etc.
- `components/`: Elementos reutilizáveis
  - `forms.py`: Formulários padronizados
  - `charts.py`: Gráficos personalizados

**Quando trabalhar aqui**: Criando ou modificando interfaces visuais

---

### 🔧 `/backend` - Lógica de Negócio

**Responsável por**: Processar dados, conectar com o banco, regras de negócio

#### 📊 `/backend/models` - Representação dos Dados

Cada arquivo representa uma tabela do banco de dados.

**Exemplo - `doador.py`**:
```python
from backend.models.base_model import BaseModel

class Doador(BaseModel):
    table_name = "Doador"
    
    # Herda métodos:
    # - find_all()      → Lista todos
    # - find_by_id(id)  → Busca por ID
    # - create(data)    → Cria novo
    # - update(id, data)→ Atualiza
    # - delete(id)      → Remove
```

**Quando trabalhar aqui**: 
- Adicionando novos métodos de busca
- Criando novas entidades
- Modificando queries SQL

#### 🎯 `/backend/services` - Lógica Complexa

Operações que envolvem múltiplas tabelas ou regras de negócio.

**Exemplo**: Criar uma doação completa (doação + objetos + voluntários)

**Quando trabalhar aqui**: Implementando funcionalidades complexas

#### 🔌 `/backend/database` - Conexão com BD

- `connection.py`: Gerencia conexões MySQL
- `setup.py`: Cria/reseta o banco de dados

**Quando trabalhar aqui**: Raramente. Só se precisar ajustar a conexão.

---

### 🗄️ `/database` - Scripts SQL

#### 📋 `/database/schema` - Estrutura do Banco

Scripts DDL (Data Definition Language) - CREATE TABLE, ALTER TABLE, etc.

**Arquivo principal**: `01_create_tables.sql`

**Quando trabalhar aqui**: 
- Criando novas tabelas
- Modificando estrutura existente
- **IMPORTANTE**: Sempre versione (02_, 03_, etc.)

#### 🌱 `/database/seeds` - Dados Iniciais

Scripts DML (Data Manipulation Language) - INSERT, UPDATE, etc.

**Arquivo principal**: `01_sample_data.sql`

**Quando trabalhar aqui**: Adicionando dados de exemplo/teste

#### 🔄 `/database/migrations` - Versionamento

Histórico de mudanças no banco de dados.

**Quando trabalhar aqui**: Alterando tabelas em produção

---

### 📖 `/docs` - Documentação

- `QUICKSTART.md`: Para começar rapidamente
- `DEVELOPMENT.md`: Guia detalhado de desenvolvimento
- `diagramas/`: ER, Relacional, Fluxogramas
- `figma/`: Referências dos protótipos

**Quando trabalhar aqui**: Sempre que criar algo novo, documente!

---

### 🎨 `/assets` - Recursos Visuais

Imagens, ícones, logos, etc.

**Organização**:
- `images/`: Fotos, banners
- `icons/`: Ícones do sistema

---

## 🚀 Fluxo de Trabalho

### 1️⃣ Primeira Vez no Projeto

```bash
# 1. Clone o repositório
git clone [url-do-repo]
cd somos-darua

# 2. Crie o ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure o .env
cp .env.example .env
# Edite o .env com sua senha do MySQL

# 5. Crie o banco de dados
python backend/database/setup.py
# Escolha opção 1 e confirme inserção de dados de exemplo

# 6. Execute a aplicação
streamlit run app/main.py
```

### 2️⃣ Trabalhando no Projeto

```bash
# Sempre que voltar ao projeto:
source venv/bin/activate  # Ativar ambiente virtual

# Para rodar a aplicação:
streamlit run app/main.py

# Para testar a conexão com o banco:
python backend/database/connection.py
```

### 3️⃣ Adicionando uma Nova Funcionalidade

**Exemplo: Criar página de Campanhas**

1. **Crie o arquivo da página**:
   ```bash
   # Criar: app/pages/campanhas.py
   ```

2. **Implemente a interface**:
   ```python
   import streamlit as st
   from backend.models.campanha_doacao import CampanhaDoacao
   
   def show():
       st.title("🎪 Gestão de Campanhas")
       
       # Listar campanhas
       campanhas = CampanhaDoacao.find_all()
       st.dataframe(campanhas)
   
   if __name__ == "__main__":
       show()
   ```

3. **Teste**:
   ```bash
   streamlit run app/pages/campanhas.py
   ```

4. **Commit**:
   ```bash
   git add app/pages/campanhas.py
   git commit -m "feat: adiciona página de gestão de campanhas"
   git push
   ```

---

## 📝 Convenções do Projeto

### Nomenclatura de Arquivos

- **Python**: `snake_case.py` 
  - ✅ `doacao_service.py`
  - ❌ `DoacaoService.py`

- **Classes**: `PascalCase`
  - ✅ `class DoacaoService:`
  - ❌ `class doacao_service:`

- **Funções**: `snake_case`
  - ✅ `def criar_doacao():`
  - ❌ `def CriarDoacao():`

### Estrutura de Commits

Use commits semânticos:

- `feat:` - Nova funcionalidade
  - `feat: adiciona cadastro de voluntários`

- `fix:` - Correção de bug
  - `fix: corrige erro ao salvar doador`

- `docs:` - Documentação
  - `docs: atualiza README com instruções`

- `style:` - Formatação
  - `style: formata código com black`

- `refactor:` - Refatoração
  - `refactor: melhora estrutura do model Doacao`

- `test:` - Testes
  - `test: adiciona testes para Doador`

### Branches

- `main`: Código estável, pronto para produção
- `develop`: Desenvolvimento ativo
- `feature/nome-da-feature`: Nova funcionalidade
- `fix/nome-do-bug`: Correção de bug

**Fluxo**:
```bash
# Criar nova feature
git checkout -b feature/pagina-voluntarios

# Trabalhar...
git add .
git commit -m "feat: implementa listagem de voluntários"

# Enviar para revisão
git push origin feature/pagina-voluntarios
# Criar Pull Request no GitHub
```

---

## 🤝 Divisão de Tarefas

### Sugestão de Divisão

**Giuseppe**: Backend e Banco de Dados
- Models
- Queries SQL
- Services

**Pedro Henrique**: Frontend Principal
- Dashboard
- Páginas de Doadores/Beneficiários
- Componentes visuais

**Pedro Tinoco**: Frontend Complementar
- Páginas de Campanhas/Voluntários
- Relatórios e gráficos

**Savio Faria**: Integração e Documentação
- Conectar frontend com backend
- Testes
- Documentação

> **Nota**: Isso é apenas uma sugestão! Ajustem conforme preferirem.

---

## 🆘 Problemas Comuns

### "Module not found"
```bash
# Certifique-se de estar no ambiente virtual
source venv/bin/activate
pip install -r requirements.txt
```

### "Can't connect to MySQL"
1. Verifique se o MySQL está rodando
2. Confira o arquivo `.env`
3. Teste: `python backend/database/connection.py`

### "Table doesn't exist"
```bash
# Recrie o banco
python backend/database/setup.py
# Escolha opção 2 (reset)
```

### Conflitos no Git
```bash
# Atualize seu branch antes de começar
git pull origin main

# Se houver conflitos, resolva e:
git add .
git commit -m "merge: resolve conflitos"
```

---

## 📞 Comunicação

- **Issues**: Use o GitHub Issues para reportar bugs ou sugerir features
- **Pull Requests**: Para revisão de código
- **Discussões**: Use GitHub Discussions para dúvidas gerais

---

## ✅ Checklist Antes de Fazer Push

- [ ] Código testado localmente
- [ ] Sem erros no console
- [ ] Arquivo `.env` NÃO foi commitado
- [ ] Código comentado onde necessário
- [ ] Commit message descritiva
- [ ] Branch correta

---

## 📚 Recursos Úteis

- [Documentação Streamlit](https://docs.streamlit.io)
- [MySQL Connector Python](https://dev.mysql.com/doc/connector-python/en/)
- [Protótipos no Figma](https://www.figma.com/design/d6OHKROYes1IFtyfAiAGUd/Projeto-BD)
- [Guia de Markdown](https://www.markdownguide.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

## 🎓 Dicas para Iniciantes

1. **Não tenha medo de errar**: Git permite reverter mudanças
2. **Peça ajuda**: Use as Issues ou pergunte à equipe
3. **Comece pequeno**: Faça uma página simples primeiro
4. **Use os exemplos**: Os models já têm exemplos de código
5. **Commit frequentemente**: Melhor muitos commits pequenos que um gigante
6. **Teste antes de commitar**: Execute o código localmente

---

## 🎯 Próximos Passos

1. **Configurar ambiente** (siga as instruções acima)
2. **Explorar o código** existente
3. **Escolher uma tarefa** pequena para começar
4. **Fazer o primeiro commit**
5. **Criar seu primeiro Pull Request**

---

**Dúvidas?** Abra uma Issue ou pergunte no grupo!

**Boa sorte com o desenvolvimento! 🚀**

---

*Última atualização: Novembro 2025*
