# 🚀 Como Executar o Frontend - Somos DaRua

## ✅ Sistema Completo Criado!

Todas as 8 páginas do sistema foram desenvolvidas com sucesso:

### 📄 Páginas Criadas

1. ✅ **Dashboard (main.py)** - Página inicial com métricas e gráficos
2. ✅ **Doadores (2_doadores.py)** - Gerenciamento de doadores
3. ✅ **Beneficiários (3_beneficiarios.py)** - Gestão de beneficiários
4. ✅ **Doações (4_doacoes.py)** - Registro e histórico de doações
5. ✅ **Campanhas (5_campanhas.py)** - Criação e gestão de campanhas
6. ✅ **Pontos de Coleta (6_pontos_coleta.py)** - Cadastro de pontos
7. ✅ **Voluntários (7_voluntarios.py)** - Gestão de voluntários
8. ✅ **Relatórios (8_relatorios.py)** - Estatísticas e relatórios

### 📦 Arquivo de Dados Mockados

✅ **mock_data.py** - Contém todos os dados fictícios para demonstração

---

## 🎯 Características do Sistema

### ✨ Funcionalidades Implementadas

- 🎨 Interface moderna com cores roxo (#8B5CF6) e azul (#3B82F6)
- 📊 Gráficos interativos com Plotly (pizza, barras, linhas, área)
- 📝 Formulários completos de cadastro
- 🔍 Sistema de busca e filtros funcionais
- 📈 Métricas e estatísticas em tempo real
- 🗂️ Tabelas interativas com pandas
- 🎨 Cards visuais para campanhas e pontos de coleta
- 📱 Design responsivo
- 🧭 Navegação intuitiva entre páginas

### 🎭 Dados Mockados Disponíveis

- **30 doadores** fictícios com dados completos
- **40 beneficiários** com informações detalhadas
- **120+ doações** dos últimos 6 meses
- **12 campanhas** (ativas e concluídas)
- **15 pontos de coleta** em São Paulo
- **30 voluntários** cadastrados
- **Métricas do dashboard** completas

---

## 🚀 Como Executar

### Passo 1: Instalar as Dependências

```bash
# Navegue até o diretório do projeto
cd /DaRua

# Instale as dependências
pip install -r requirements.txt
```

### Passo 2: Executar o Sistema

```bash
# Entre no diretório app
cd app

# Execute o Streamlit
streamlit run main.py
```

### Passo 3: Acessar o Sistema

O sistema abrirá automaticamente no navegador. Se não abrir, acesse:

```
http://localhost:8501
```

---

## 📁 Estrutura Final

```
DaRua/
├── app/
│   ├── main.py                    ✅ Dashboard principal
│   ├── pages/
│   │   ├── 2_doadores.py         ✅ Gestão de doadores
│   │   ├── 3_beneficiarios.py    ✅ Gestão de beneficiários
│   │   ├── 4_doacoes.py          ✅ Registro de doações
│   │   ├── 5_campanhas.py        ✅ Gestão de campanhas
│   │   ├── 6_pontos_coleta.py    ✅ Pontos de coleta
│   │   ├── 7_voluntarios.py      ✅ Cadastro de voluntários
│   │   └── 8_relatorios.py       ✅ Relatórios e estatísticas
│   └── utils/
│       └── mock_data.py           ✅ Dados mockados
├── requirements.txt               ✅ Atualizado
└── README.md                      ✅ Documentação completa
```

---

## 🎨 Preview das Páginas

### 1. 🏠 Dashboard
- 4 cards de métricas principais
- Gráfico de pizza: Doações por categoria
- Gráfico de barras: Doações mensais
- Gráfico de linha: Tendência de doadores
- Tabela: Últimas 10 doações

### 2. 👤 Doadores
- Busca por nome, email ou telefone
- Tabela com todos os doadores
- Formulário de cadastro
- Estatísticas rápidas

### 3. 🤝 Beneficiários
- Lista de beneficiários
- Filtros por status
- Formulário completo
- Gráficos de distribuição

### 4. 📦 Doações
- **Aba 1**: Formulário de nova doação
- **Aba 2**: Histórico com filtros de data e tipo
- Estatísticas por período
- Tabela detalhada

### 5. 📢 Campanhas
- Cards visuais de campanhas
- Barras de progresso
- Filtros por status
- Formulário de nova campanha
- Gráfico de desempenho

### 6. 📍 Pontos de Coleta
- Cards com informações completas
- Endereço, horário, responsável
- Formulário de cadastro
- Filtros e busca

### 7. 🙋 Voluntários
- Tabela de voluntários
- Filtros por status e área
- Formulário com disponibilidade
- Gráficos de análise

### 8. 📊 Relatórios
- Métricas com comparações
- 4 gráficos diferentes
- 3 tabelas detalhadas
- Opções de exportação (simuladas)

---

## ⚠️ IMPORTANTE

### ✅ O que ESTÁ implementado:

- ✅ Toda a interface visual (frontend)
- ✅ Navegação entre páginas
- ✅ Formulários interativos
- ✅ Gráficos e tabelas
- ✅ Busca e filtros funcionais
- ✅ Dados mockados para demonstração
- ✅ Layout responsivo

### ❌ O que NÃO está implementado:

- ❌ Conexão com banco de dados
- ❌ Salvamento real de dados
- ❌ Autenticação de usuários
- ❌ Backend/API
- ❌ Exportação real (PDF, Excel)
- ❌ Envio de emails
- ❌ Upload de arquivos

**Motivo**: Conforme solicitado, este é um **frontend apenas para visualização**, sem conexão com banco de dados ou backend.

---

## 🎯 Próximos Passos (Opcional)

Se quiser transformar em um sistema completo:

### 1. Conectar ao Banco de Dados

```python
# No arquivo de cada página, substituir:
from utils.mock_data import get_doadores_mockados

# Por:
from backend.models.doador import Doador
doadores = Doador.find_all()
```

### 2. Implementar Salvamento Real

```python
# No formulário, substituir a mensagem de sucesso por:
if submit:
    Doador.create({
        'nome': nome,
        'cpf': cpf,
        'email': email,
        # ...
    })
    st.success("Doador salvo no banco de dados!")
```

### 3. Adicionar Autenticação

```python
# Adicionar no main.py:
import streamlit_authenticator as stauth

if st.session_state.get('authentication_status'):
    # Mostrar conteúdo
else:
    # Mostrar login
```

---

## 🐛 Resolução de Problemas

### Erro: "Module not found: streamlit"

```bash
pip install streamlit pandas plotly numpy
```

### Erro: "No module named 'utils'"

```bash
# Certifique-se de estar no diretório app/
cd app
streamlit run main.py
```

### Erro: Página não carrega

```bash
# Limpe o cache do Streamlit
streamlit cache clear
streamlit run main.py
```

### Erro: Gráficos não aparecem

```bash
# Reinstale o plotly
pip uninstall plotly
pip install plotly==5.18.0
```

---

## 📊 Testando o Sistema

### Teste 1: Dashboard
1. Execute `streamlit run main.py`
2. Verifique se aparecem os 4 cards de métricas
3. Veja se os gráficos são exibidos
4. Confira a tabela de últimas doações

### Teste 2: Navegação
1. Use a sidebar para navegar
2. Acesse cada página (Doadores, Beneficiários, etc.)
3. Verifique se a navegação funciona

### Teste 3: Formulários
1. Em Doadores, clique em "Cadastrar Novo Doador"
2. Preencha os campos
3. Clique em "Salvar"
4. Veja a mensagem de sucesso

### Teste 4: Busca e Filtros
1. Em Doadores, use a barra de busca
2. Digite um nome (ex: "João")
3. Veja os resultados filtrados

### Teste 5: Gráficos Interativos
1. Acesse Relatórios
2. Passe o mouse sobre os gráficos
3. Veja as informações detalhadas
4. Teste zoom e pan

---

## 💡 Dicas de Uso

### Para Apresentação:

1. **Comece pelo Dashboard** - Mostre a visão geral
2. **Demonstre a navegação** - Use a sidebar
3. **Mostre um cadastro** - Use o formulário de Doadores
4. **Exiba os gráficos** - Vá para Relatórios
5. **Demonstre filtros** - Use busca em Beneficiários

### Para Desenvolvimento:

1. **Use o modo desenvolvedor** do Streamlit:
   ```bash
   streamlit run main.py --server.runOnSave true
   ```
2. **Ative o cache** para melhor performance
3. **Use st.session_state** para persistir dados temporariamente

---

## 🎨 Customização

### Alterar Cores:

No arquivo de cada página, procure por:

```python
st.markdown("""
    <style>
    .stButton>button {
        background-color: #8B5CF6;  # Altere aqui
    }
    </style>
""", unsafe_allow_html=True)
```

### Adicionar Novos Dados Mockados:

Edite o arquivo `app/utils/mock_data.py`:

```python
def get_doadores_mockados():
    # Adicione mais doadores aqui
    return [...]
```

---

## 📝 Checklist de Implementação

- [x] Criar arquivo mock_data.py com todos os dados
- [x] Criar main.py (Dashboard)
- [x] Criar página de Doadores
- [x] Criar página de Beneficiários
- [x] Criar página de Doações
- [x] Criar página de Campanhas
- [x] Criar página de Pontos de Coleta
- [x] Criar página de Voluntários
- [x] Criar página de Relatórios
- [x] Atualizar requirements.txt
- [x] Adicionar navegação em todas as páginas
- [x] Implementar busca e filtros
- [x] Adicionar gráficos interativos
- [x] Criar formulários de cadastro
- [x] Adicionar validações visuais
- [x] Implementar cards e estatísticas

## ✅ STATUS: COMPLETO!

---

**Desenvolvido para**: Projeto Somos DaRua  
**Curso**: Banco de Dados - 2025/2  
**Tipo**: Frontend (apenas visualização)  
**Tecnologia**: Python + Streamlit  
**Status**: ✅ **COMPLETO E PRONTO PARA USO**

---

🎉 **Parabéns! O sistema frontend está 100% funcional e pronto para demonstração!**
