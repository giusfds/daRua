# 📚 Documentação Completa - Somos DaRua

<div align="center">

![Status](https://img.shields.io/badge/status-ativo-success.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.31.0-red.svg)
![MySQL](https://img.shields.io/badge/mysql-8.0-blue.svg)

**Sistema de Gestão de Doações para Organizações Sociais**

[🚀 Início Rápido](#-início-rápido) • [📖 Documentação](#-documentação-completa) • [👥 Equipe](#-equipe)

</div>

---

## 📋 Índice

### 🎯 Visão Geral

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades Principais](#funcionalidades-principais)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)

### 🚀 Começando

- [Guia de Instalação](./INSTALACAO.md)
- [Configuração do Ambiente](./INSTALACAO.md#configuração-do-ambiente)
- [Primeiro Uso](./INSTALACAO.md#primeiro-uso)

### 🏗️ Arquitetura

- [Arquitetura do Sistema](./ARQUITETURA.md)
- [Estrutura de Diretórios](./ARQUITETURA.md#estrutura-de-diretórios)
- [Fluxo de Dados](./ARQUITETURA.md#fluxo-de-dados)
- [Padrões de Projeto](./ARQUITETURA.md#padrões-de-projeto)

### 🗄️ Banco de Dados

- [Modelo de Dados](./DATABASE.md)
- [Diagrama ER](./DATABASE.md#diagrama-er)
- [Tabelas e Relacionamentos](./DATABASE.md#tabelas-e-relacionamentos)
- [Migrations e Seeds](./DATABASE.md#migrations-e-seeds)

### 💻 Desenvolvimento

- [Guia de Desenvolvimento](./DESENVOLVIMENTO.md)
- [Estrutura de Código](./DESENVOLVIMENTO.md#estrutura-de-código)
- [Padrões de Código](./DESENVOLVIMENTO.md#padrões-de-código)
- [Boas Práticas](./DESENVOLVIMENTO.md#boas-práticas)

### 🔌 API & Models

- [Documentação de Models](./API.md)
- [CRUD Operations](./API.md#crud-operations)
- [Validações](./API.md#validações)
- [Exemplos de Uso](./API.md#exemplos-de-uso)

### 🎨 Frontend

- [Componentes Streamlit](./FRONTEND.md)
- [Páginas](./FRONTEND.md#páginas)
- [Componentes Reutilizáveis](./FRONTEND.md#componentes-reutilizáveis)
- [Estilização](./FRONTEND.md#estilização)

### 🧪 Testes

- [Estratégia de Testes](./TESTES.md)
- [Testes Unitários](./TESTES.md#testes-unitários)
- [Testes de Integração](./TESTES.md#testes-de-integração)

### 🚢 Deploy

- [Deploy em Produção](./DEPLOY.md)
- [Configurações de Servidor](./DEPLOY.md#configurações)
- [Monitoramento](./DEPLOY.md#monitoramento)

---

## 🎯 Sobre o Projeto

O **Somos DaRua** é um sistema completo de gestão de doações desenvolvido para organizações sociais que atendem pessoas em situação de vulnerabilidade social. O sistema conecta:

- 👤 **Doadores**: Pessoas ou empresas que doam itens
- 🤝 **Beneficiários**: Pessoas que recebem as doações
- 📦 **Doações**: Registro e rastreamento de itens doados
- 📢 **Campanhas**: Organização de campanhas de arrecadação
- 📍 **Pontos de Coleta**: Locais de recebimento de doações
- 🙋 **Voluntários**: Pessoas que ajudam nas ações

### 🎯 Objetivos

1. **Facilitar a gestão** de doações de forma eficiente
2. **Conectar** doadores e beneficiários de forma transparente
3. **Organizar** campanhas e pontos de coleta
4. **Gerar relatórios** para análise e tomada de decisão
5. **Proporcionar visibilidade** das ações sociais

---

## ✨ Funcionalidades Principais

### 📊 Dashboard

- Métricas em tempo real
- Gráficos de análise de doações
- Visão geral do sistema
- Indicadores de performance

### 👥 Gestão de Doadores

- Cadastro completo com endereço
- Histórico de doações
- Perfil e estatísticas
- Busca e filtros avançados

### 🤝 Gestão de Beneficiários

- Cadastro de pessoas atendidas
- Registro de necessidades
- Histórico de recebimentos
- Análise demográfica

### 📦 Gestão de Doações

- Registro de doações com múltiplos itens
- Rastreamento de status (pendente/entregue)
- Vinculação com campanhas
- Relatórios detalhados

### 📢 Campanhas

- Criação e gestão de campanhas
- Período de duração
- Metas e objetivos
- Análise de resultados

### 📍 Pontos de Coleta

- Cadastro de locais de recebimento
- Endereços completos
- Objetos disponíveis
- Mapa de localização

### 🙋 Voluntários

- Cadastro de colaboradores
- Informações de contato
- Vínculo com campanhas
- Histórico de participação

### 📈 Relatórios

- Relatórios de doações por período
- Análise de doadores mais ativos
- Itens mais doados
- Performance de campanhas
- Exportação de dados (Excel/CSV)

---

## 🛠️ Tecnologias Utilizadas

### Backend

- **Python 3.10+**: Linguagem principal
- **MySQL 8.0**: Banco de dados relacional
- **mysql-connector-python**: Driver MySQL
- **python-dotenv**: Gerenciamento de variáveis de ambiente

### Frontend

- **Streamlit 1.31.0**: Framework web para Python
- **Plotly 5.18.0**: Gráficos interativos
- **Pandas 2.2.0**: Manipulação de dados
- **NumPy 1.26.3**: Computação numérica

### Desenvolvimento

- **Git**: Controle de versão
- **pip**: Gerenciador de pacotes Python
- **Virtual Environment**: Isolamento de dependências

### Design

- **Figma**: Prototipação de interfaces

---

## 🚀 Início Rápido

### Pré-requisitos

```bash
- Python 3.10 ou superior
- MySQL 8.0 ou superior
- pip (gerenciador de pacotes Python)
- Git
```

### Instalação Rápida

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/somos-darua.git
cd somos-darua

# 2. Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# 3. Instale dependências
pip install -r requirements.txt

# 4. Configure o banco de dados
# Edite .env com suas credenciais MySQL
cp .env.example .env

# 5. Execute o sistema
./run.sh  # No Windows: run.bat
```

### Acesso

```
🌐 http://localhost:8501
```

Para instruções detalhadas, consulte o [Guia de Instalação](./INSTALACAO.md).

---

## 📖 Documentação Completa

### 📚 Guias Principais

| Documento                                  | Descrição                                  | Público                  |
| ------------------------------------------ | ------------------------------------------ | ------------------------ |
| [📦 Instalação](./INSTALACAO.md)           | Guia completo de instalação e configuração | Todos                    |
| [🏗️ Arquitetura](./ARQUITETURA.md)         | Estrutura e design do sistema              | Desenvolvedores          |
| [🗄️ Banco de Dados](./DATABASE.md)         | Modelo de dados e schemas                  | Desenvolvedores/DBAs     |
| [💻 Desenvolvimento](./DESENVOLVIMENTO.md) | Padrões e práticas de código               | Desenvolvedores          |
| [🔌 API/Models](./API.md)                  | Documentação dos models                    | Desenvolvedores          |
| [🎨 Frontend](./FRONTEND.md)               | Componentes e páginas Streamlit            | Desenvolvedores Frontend |

### 🔍 Referência Rápida

- **Criando um novo Model**: [API.md → Criando Models](./API.md#criando-models)
- **Adicionando uma página**: [Frontend.md → Nova Página](./FRONTEND.md#adicionando-páginas)
- **Executando Migrations**: [Database.md → Migrations](./DATABASE.md#migrations)
- **Padrões de Código**: [Desenvolvimento.md → Padrões](./DESENVOLVIMENTO.md#padrões-de-código)

---

## 👥 Equipe

<table>
  <tr>
    <td align="center">
      <strong>Giuseppe Cordeiro</strong><br>
      Desenvolvedor Backend
    </td>
    <td align="center">
      <strong>Pedro Henrique</strong><br>
      Desenvolvedor Backend
    </td>
  </tr>
  <tr>
    <td align="center">
      <strong>Pedro Tinoco</strong><br>
      Desenvolvedor Full Stack
    </td>
    <td align="center">
      <strong>Savio Faria</strong><br>
      Database Frontend
    </td>
  </tr>
</table>

---

## 📞 Suporte e Contribuição

### 🐛 Encontrou um Bug?

Abra uma [issue](https://github.com/giusfds/darua/issues) descrevendo:

- O que aconteceu
- O que deveria acontecer
- Passos para reproduzir

### 💡 Tem uma Sugestão?

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença especificada no arquivo [LICENSE](../LICENSE).

---

## 🗺️ Roadmap

### ✅ Versão 1.0 (Atual)

- [x] CRUD completo de todas entidades
- [x] Dashboard com métricas
- [x] Sistema de relatórios
- [x] Interface Streamlit

### 🚧 Versão 1.1 (Em Desenvolvimento)

- [ ] Autenticação de usuários
- [ ] Sistema de permissões
- [ ] Notificações por email
- [ ] Exportação de relatórios PDF

### 📋 Versão 2.0 (Planejado)

- [ ] API REST
- [ ] App mobile
- [ ] Integração com redes sociais
- [ ] Sistema de gamificação

---

## 🌟 Agradecimentos

Agradecemos a todos que contribuíram para este projeto e às organizações sociais que inspiraram sua criação.

---

<div align="center">

[⬆ Voltar ao topo](#-documentação-completa---somos-darua)

</div>
