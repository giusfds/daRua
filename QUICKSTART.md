# 🚀 INÍCIO RÁPIDO - Somos DaRua

## ⚡ Execução Rápida (3 passos)

### Linux/Mac:

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Executar (opção fácil)
./run.sh

# OU executar manualmente:
cd app
streamlit run main.py
```

### Windows:

```batch
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Executar (opção fácil)
run.bat

# OU executar manualmente:
cd app
streamlit run main.py
```

### Acesso:

```
http://localhost:8501
```

---

## 📱 Páginas Disponíveis

| Página | Arquivo | Descrição |
|--------|---------|-----------|
| 🏠 Dashboard | `main.py` | Página inicial com métricas |
| 👤 Doadores | `2_doadores.py` | Gestão de doadores |
| 🤝 Beneficiários | `3_beneficiarios.py` | Gestão de beneficiários |
| 📦 Doações | `4_doacoes.py` | Registro de doações |
| 📢 Campanhas | `5_campanhas.py` | Gestão de campanhas |
| 📍 Pontos de Coleta | `6_pontos_coleta.py` | Pontos de coleta |
| 🙋 Voluntários | `7_voluntarios.py` | Cadastro de voluntários |
| 📊 Relatórios | `8_relatorios.py` | Estatísticas e relatórios |

---

## 🎯 Funcionalidades Principais

### Dashboard
- ✅ 4 cards de métricas
- ✅ 3 gráficos interativos
- ✅ Tabela de últimas doações

### Doadores
- ✅ Lista completa
- ✅ Busca por nome/email/telefone
- ✅ Formulário de cadastro

### Beneficiários
- ✅ Lista com filtros
- ✅ Gráficos de análise
- ✅ Cadastro detalhado

### Doações
- ✅ Registro de novas doações
- ✅ Histórico com filtros
- ✅ Estatísticas por período

### Campanhas
- ✅ Cards visuais
- ✅ Barras de progresso
- ✅ Criação de campanhas

### Pontos de Coleta
- ✅ Lista de pontos
- ✅ Informações completas
- ✅ Cadastro de locais

### Voluntários
- ✅ Gestão de voluntários
- ✅ Filtros por área
- ✅ Análises gráficas

### Relatórios
- ✅ Múltiplos gráficos
- ✅ Tabelas detalhadas
- ✅ Comparações

---

## 🎨 Recursos Visuais

- Cores: Roxo (#8B5CF6) e Azul (#3B82F6)
- Gráficos interativos com Plotly
- Cards responsivos
- Formulários validados
- Busca em tempo real
- Filtros funcionais

---

## 📦 Dados Mockados

- 30 doadores
- 40 beneficiários
- 120+ doações
- 12 campanhas
- 15 pontos de coleta
- 30 voluntários

---

## ⚙️ Tecnologias

- Python 3.8+
- Streamlit 1.31.0
- Pandas 2.2.0
- Plotly 5.18.0
- Numpy 1.26.3

---

## 🐛 Problemas?

### Erro de módulo:
```bash
pip install -r requirements.txt
```

### Porta ocupada:
```bash
streamlit run main.py --server.port 8502
```

### Cache:
```bash
streamlit cache clear
```

---

## 📖 Documentação Completa

- `FRONTEND_GUIDE.md` - Guia completo do frontend
- `README.md` - Documentação do projeto
- `/docs` - Documentação adicional

---

## ✅ Checklist de Verificação

- [ ] Python 3.8+ instalado
- [ ] Dependências instaladas
- [ ] Navegador aberto em localhost:8501
- [ ] Dashboard carregou
- [ ] Navegação funciona
- [ ] Formulários abrem

---

## 🎉 Pronto!

O sistema está completo e funcional!

**Dúvidas?** Consulte `FRONTEND_GUIDE.md`
