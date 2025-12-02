# 🧪 Guia de Testes - Somos DaRua

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Estratégia de Testes](#estratégia-de-testes)
- [Configuração do Ambiente de Testes](#configuração-do-ambiente-de-testes)
- [Testes Unitários](#testes-unitários)
- [Testes de Integração](#testes-de-integração)
- [Testes End-to-End](#testes-end-to-end)
- [Cobertura de Código](#cobertura-de-código)
- [Boas Práticas](#boas-práticas)

---

## 🎯 Visão Geral

O sistema Somos DaRua deve ter uma cobertura de testes robusta para garantir qualidade e confiabilidade. Esta documentação define a estratégia de testes e fornece exemplos práticos.

### Por que Testar?

✅ **Confiabilidade**: Garantir que o código funciona como esperado
✅ **Manutenibilidade**: Facilitar refatorações sem quebrar funcionalidades
✅ **Documentação**: Testes servem como documentação viva do sistema
✅ **Prevenção**: Detectar bugs antes de chegarem à produção
✅ **Confiança**: Permitir mudanças com segurança

---

## 📐 Estratégia de Testes

### Pirâmide de Testes

```
        ┌─────────────┐
        │     E2E     │  ← Poucos e lentos
        │   (Manual)  │
        ├─────────────┤
        │ Integração  │  ← Alguns
        │   (DB+API)  │
        ├─────────────┤
        │  Unitários  │  ← Muitos e rápidos
        │   (Models)  │
        └─────────────┘
```

### Tipos de Testes

| Tipo           | O que testa                 | Ferramentas     | Quantidade |
| -------------- | --------------------------- | --------------- | ---------- |
| **Unitários**  | Funções e métodos isolados  | pytest          | 70%        |
| **Integração** | Interação entre componentes | pytest + MySQL  | 20%        |
| **E2E**        | Fluxos completos do usuário | Manual/Selenium | 10%        |

---

## ⚙️ Configuração do Ambiente de Testes

### Instalar Dependências de Teste

```bash
pip install pytest pytest-cov pytest-mock
```

### Estrutura de Diretórios

```
somos-darua/
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Fixtures compartilhadas
│   │
│   ├── unit/                    # Testes unitários
│   │   ├── __init__.py
│   │   ├── test_doador.py
│   │   ├── test_beneficiario.py
│   │   ├── test_doacao.py
│   │   ├── test_campanha.py
│   │   └── ...
│   │
│   ├── integration/             # Testes de integração
│   │   ├── __init__.py
│   │   ├── test_database.py
│   │   ├── test_doacao_flow.py
│   │   └── ...
│   │
│   └── e2e/                     # Testes end-to-end
│       ├── __init__.py
│       └── test_fluxo_completo.py
│
└── pytest.ini                   # Configuração do pytest
```

### Configuração do pytest

Criar `pytest.ini` na raiz:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --tb=short
    --strict-markers
    --disable-warnings
markers =
    unit: Testes unitários
    integration: Testes de integração
    slow: Testes que demoram mais de 1 segundo
```

### Banco de Dados de Teste

Criar banco separado para testes:

```sql
CREATE DATABASE somos_darua_test
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

Configurar `.env.test`:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha
DB_NAME=somos_darua_test
DB_PORT=3306
```

---

## 🔬 Testes Unitários

Testam componentes isolados (métodos, funções).

### Estrutura Básica

```python
# tests/unit/test_doador.py
import pytest
from backend.models.doador import Doador


class TestDoador:
    """Testes unitários do model Doador"""

    def test_criar_doador_valido(self):
        """Deve criar doador com dados válidos"""
        doador = Doador(
            nome="João Silva",
            email="joao@email.com",
            telefone="(31) 99999-9999"
        )

        assert doador.nome == "João Silva"
        assert doador.email == "joao@email.com"

    def test_validacao_nome_obrigatorio(self):
        """Deve falhar se nome não for fornecido"""
        doador = Doador(nome="")

        valido, erro = doador.validate()

        assert not valido
        assert "Nome é obrigatório" in erro

    def test_validacao_email_formato(self):
        """Deve validar formato do email"""
        doador = Doador(
            nome="João Silva",
            email="emailinvalido"
        )

        valido, erro = doador.validate()

        assert not valido
        assert "Email inválido" in erro

    def test_validacao_estado_tamanho(self):
        """Estado deve ter exatamente 2 caracteres"""
        doador = Doador(
            nome="João Silva",
            estado="SP"
        )

        valido, _ = doador.validate()
        assert valido

        doador.estado = "São Paulo"
        valido, erro = doador.validate()
        assert not valido
        assert "2 caracteres" in erro
```

### Testando Validações

```python
# tests/unit/test_validacoes.py
import pytest
from backend.models.doacao import Doacao
from datetime import date, timedelta


class TestValidacoesDoacao:

    def test_quantidade_positiva(self):
        """Quantidade deve ser maior que zero"""
        doacao = Doacao(
            doador_id=1,
            ponto_coleta_id=1,
            voluntario_coleta_id=1,
            tipo_doacao="Alimentos",
            descricao_item="Arroz",
            quantidade=0,
            unidade="Kg"
        )

        valido, erro = doacao.validate()
        assert not valido
        assert "maior que zero" in erro

    def test_data_entrega_posterior(self):
        """Data de entrega deve ser após data de criação"""
        doacao = Doacao(
            doador_id=1,
            ponto_coleta_id=1,
            voluntario_coleta_id=1,
            tipo_doacao="Alimentos",
            descricao_item="Arroz",
            quantidade=5,
            unidade="Kg",
            data_criacao=date.today(),
            data_entrega=date.today() - timedelta(days=1)
        )

        valido, erro = doacao.validate()
        assert not valido
        assert "anterior" in erro
```

### Testando Métodos Estáticos

```python
# tests/unit/test_doador_queries.py
import pytest
from unittest.mock import Mock, patch
from backend.models.doador import Doador


class TestDoadorQueries:

    @patch('backend.models.doador.DatabaseConnection')
    def test_get_all_retorna_lista(self, mock_db):
        """get_all() deve retornar lista de doadores"""
        # Configurar mock
        mock_db_instance = Mock()
        mock_db.return_value.__enter__.return_value = mock_db_instance
        mock_db_instance.fetch_all.return_value = [
            {
                'idDoador': 1,
                'Nome': 'João',
                'Email': 'joao@email.com',
                'Telefone': None,
                'Logradouro': None,
                'Numero': None,
                'Complemento': None,
                'Bairro': None,
                'Cidade': None,
                'Estado': None,
                'CEP': None
            }
        ]

        # Executar
        doadores = Doador.get_all()

        # Verificar
        assert len(doadores) == 1
        assert doadores[0].nome == 'João'
        mock_db_instance.fetch_all.assert_called_once()
```

### Executar Testes Unitários

```bash
# Todos os testes unitários
pytest tests/unit/

# Arquivo específico
pytest tests/unit/test_doador.py

# Teste específico
pytest tests/unit/test_doador.py::TestDoador::test_criar_doador_valido

# Com verbose
pytest tests/unit/ -v

# Com saída detalhada
pytest tests/unit/ -vv
```

---

## 🔗 Testes de Integração

Testam a interação entre componentes (Model + Database).

### Fixtures Compartilhadas

```python
# tests/conftest.py
import pytest
import os
from dotenv import load_dotenv
from backend.database.connection import DatabaseConnection
from backend.models.doador import Doador


# Carregar variáveis de teste
load_dotenv('.env.test')


@pytest.fixture(scope='session')
def db():
    """Fixture de conexão com banco de teste"""
    with DatabaseConnection() as database:
        yield database


@pytest.fixture(scope='function')
def clean_db(db):
    """Limpa banco antes de cada teste"""
    # Desabilitar foreign key checks
    db.execute_query("SET FOREIGN_KEY_CHECKS = 0")

    # Truncar tabelas
    tables = [
        'Recebe', 'Possui', 'Contem', 'Promove', 'Associa',
        'Doacao', 'Doador', 'Beneficiario', 'CampanhaDoacao',
        'PontoColeta', 'ObjetoDoavel', 'Voluntario', 'Necessidade'
    ]

    for table in tables:
        db.execute_query(f"TRUNCATE TABLE {table}")

    # Reabilitar foreign key checks
    db.execute_query("SET FOREIGN_KEY_CHECKS = 1")

    yield db


@pytest.fixture
def doador_exemplo():
    """Cria um doador de exemplo"""
    doador = Doador(
        nome="João Silva",
        email="joao@email.com",
        telefone="(31) 99999-9999",
        cidade="Belo Horizonte",
        estado="MG"
    )
    return doador
```

### Teste de CRUD Completo

```python
# tests/integration/test_doador_crud.py
import pytest
from backend.models.doador import Doador


class TestDoadorCRUD:
    """Testa operações CRUD do Doador com banco real"""

    def test_criar_doador(self, clean_db, doador_exemplo):
        """Deve criar doador no banco"""
        # Salvar
        assert doador_exemplo.save()
        assert doador_exemplo.idDoador is not None

        # Verificar no banco
        result = clean_db.fetch_one(
            "SELECT * FROM Doador WHERE idDoador = %s",
            (doador_exemplo.idDoador,)
        )
        assert result is not None
        assert result['Nome'] == "João Silva"

    def test_buscar_doador_por_id(self, clean_db, doador_exemplo):
        """Deve buscar doador por ID"""
        # Criar doador
        doador_exemplo.save()

        # Buscar
        encontrado = Doador.get_by_id(doador_exemplo.idDoador)

        assert encontrado is not None
        assert encontrado.nome == doador_exemplo.nome
        assert encontrado.email == doador_exemplo.email

    def test_atualizar_doador(self, clean_db, doador_exemplo):
        """Deve atualizar doador no banco"""
        # Criar
        doador_exemplo.save()

        # Atualizar
        doador_exemplo.email = "novo_email@email.com"
        doador_exemplo.telefone = "(31) 88888-8888"
        assert doador_exemplo.update()

        # Verificar
        atualizado = Doador.get_by_id(doador_exemplo.idDoador)
        assert atualizado.email == "novo_email@email.com"
        assert atualizado.telefone == "(31) 88888-8888"

    def test_deletar_doador(self, clean_db, doador_exemplo):
        """Deve deletar doador do banco"""
        # Criar
        doador_exemplo.save()
        doador_id = doador_exemplo.idDoador

        # Deletar
        assert doador_exemplo.delete()

        # Verificar
        deletado = Doador.get_by_id(doador_id)
        assert deletado is None

    def test_listar_todos_doadores(self, clean_db):
        """Deve listar todos os doadores"""
        # Criar 3 doadores
        for i in range(3):
            doador = Doador(
                nome=f"Doador {i}",
                email=f"doador{i}@email.com"
            )
            doador.save()

        # Listar
        todos = Doador.get_all()

        assert len(todos) == 3

    def test_buscar_por_nome(self, clean_db):
        """Deve buscar doadores por nome"""
        # Criar doadores
        Doador(nome="João Silva").save()
        Doador(nome="Maria Silva").save()
        Doador(nome="Pedro Santos").save()

        # Buscar por "Silva"
        resultados = Doador.search_by_name("Silva")

        assert len(resultados) == 2
        assert all("Silva" in d.nome for d in resultados)
```

### Teste de Fluxo de Doação

```python
# tests/integration/test_fluxo_doacao.py
import pytest
from datetime import date
from backend.models.doador import Doador
from backend.models.beneficiario import Beneficiario
from backend.models.doacao import Doacao
from backend.models.voluntario import Voluntario
from backend.models.ponto_coleta import PontoColeta


class TestFluxoDoacao:
    """Testa fluxo completo de doação"""

    @pytest.fixture
    def setup_completo(self, clean_db):
        """Configura dados necessários para doação"""
        # Criar doador
        doador = Doador(nome="João Silva")
        doador.save()

        # Criar beneficiário
        beneficiario = Beneficiario(nome="Maria Costa", idade=30)
        beneficiario.save()

        # Criar ponto de coleta
        ponto = PontoColeta(responsavel="Carlos")
        ponto.save()

        # Criar voluntário
        voluntario = Voluntario(nome="Ana", email="ana@email.com")
        voluntario.save()

        return {
            'doador': doador,
            'beneficiario': beneficiario,
            'ponto': ponto,
            'voluntario': voluntario
        }

    def test_ciclo_completo_doacao(self, setup_completo):
        """Testa ciclo completo: criar → distribuir → verificar"""
        dados = setup_completo

        # 1. CRIAR DOAÇÃO (Status: Recebida)
        doacao = Doacao(
            doador_id=dados['doador'].idDoador,
            ponto_coleta_id=dados['ponto'].idPontoColeta,
            voluntario_coleta_id=dados['voluntario'].idVoluntario,
            tipo_doacao="Alimentos",
            descricao_item="Arroz 5kg",
            quantidade=5.0,
            unidade="Kg"
        )

        assert doacao.save()
        assert doacao.status == "Recebida"

        # 2. DISTRIBUIR DOAÇÃO
        sucesso, msg = Doacao.distribuir(
            doacao_id=doacao.idDoacao,
            beneficiarios_ids=[dados['beneficiario'].idBeneficiario],
            voluntarios_ids=[dados['voluntario'].idVoluntario],
            data_entrega=date.today()
        )

        assert sucesso

        # 3. VERIFICAR STATUS ATUALIZADO
        doacao_atualizada = Doacao.get_by_id(doacao.idDoacao)
        assert doacao_atualizada.status == "Distribuída"

        # 4. VERIFICAR BENEFICIÁRIOS ASSOCIADOS
        beneficiarios = Doacao.listar_beneficiarios(doacao.idDoacao)
        assert len(beneficiarios) == 1
        assert beneficiarios[0]['idBeneficiario'] == dados['beneficiario'].idBeneficiario
```

### Executar Testes de Integração

```bash
# Todos os testes de integração
pytest tests/integration/

# Com marcador
pytest -m integration

# Específico
pytest tests/integration/test_doador_crud.py -v
```

---

## 🌐 Testes End-to-End

Testam fluxos completos do ponto de vista do usuário.

### Testes Manuais

Criar checklist de testes:

```markdown
# Checklist de Testes E2E

## Fluxo 1: Cadastro de Doador

- [ ] Abrir página "Doadores"
- [ ] Clicar em aba "Cadastrar Novo"
- [ ] Preencher nome (obrigatório)
- [ ] Preencher email válido
- [ ] Preencher endereço completo
- [ ] Clicar em "Cadastrar"
- [ ] Verificar mensagem de sucesso
- [ ] Verificar doador na lista

## Fluxo 2: Registro de Doação

- [ ] Ir para página "Doações"
- [ ] Aba "Nova Doação"
- [ ] Selecionar doador
- [ ] Selecionar ponto de coleta
- [ ] Selecionar voluntário
- [ ] Preencher tipo e descrição
- [ ] Informar quantidade e unidade
- [ ] Clicar em "Registrar"
- [ ] Verificar mensagem de sucesso

## Fluxo 3: Distribuição de Doação

- [ ] Ir para aba "Distribuir Doação"
- [ ] Selecionar doação com status "Recebida"
- [ ] Marcar beneficiários
- [ ] Selecionar voluntários distribuidores
- [ ] Definir data de entrega
- [ ] Clicar em "Confirmar Distribuição"
- [ ] Verificar status atualizado para "Distribuída"
```

---

## 📊 Cobertura de Código

### Gerar Relatório de Cobertura

```bash
# Rodar testes com cobertura
pytest --cov=backend --cov-report=html

# Ver relatório
open htmlcov/index.html  # Mac
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Meta de Cobertura

- **Mínimo**: 70%
- **Ideal**: 85%+
- **Models críticos**: 90%+

### Configurar Coverage

Criar `.coveragerc`:

```ini
[run]
source = backend
omit =
    */tests/*
    */venv/*
    */__pycache__/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
```

---

## ✅ Boas Práticas

### 1. Nomenclatura Clara

```python
# ✅ BOM
def test_criar_doador_com_dados_validos():
    pass

def test_validacao_falha_quando_nome_vazio():
    pass

# ❌ EVITAR
def test_1():
    pass

def test_doador():
    pass
```

### 2. Arrange-Act-Assert

```python
def test_criar_doador():
    # Arrange (Preparar)
    nome = "João Silva"
    email = "joao@email.com"

    # Act (Agir)
    doador = Doador(nome=nome, email=email)
    resultado = doador.save()

    # Assert (Verificar)
    assert resultado is True
    assert doador.idDoador is not None
```

### 3. Um Conceito por Teste

```python
# ✅ BOM
def test_validacao_email_obrigatorio():
    doador = Doador(nome="João")
    valido, erro = doador.validate()
    assert not valido

def test_validacao_email_formato():
    doador = Doador(nome="João", email="invalido")
    valido, erro = doador.validate()
    assert not valido

# ❌ EVITAR: Testar múltiplas coisas
def test_validacao_email():
    # Testa obrigatório E formato
    pass
```

### 4. Isolar Efeitos Colaterais

```python
# ✅ BOM: Usar fixtures que limpam o banco
def test_criar_doador(clean_db):
    doador = Doador(nome="João")
    doador.save()
    # clean_db garante que não afeta outros testes

# ❌ EVITAR: Deixar dados no banco
def test_criar_doador():
    doador = Doador(nome="João")
    doador.save()
    # Pode afetar testes seguintes
```

### 5. Testes Rápidos

```python
# ✅ BOM: Mock para evitar IO
@patch('backend.database.connection.DatabaseConnection')
def test_get_all_rapido(mock_db):
    # Não acessa banco real
    pass

# ⚠️ LENTO: Usa banco real (só em testes de integração)
def test_get_all_lento(clean_db):
    # Acessa banco real
    pass
```

---

## 🔄 CI/CD

### GitHub Actions

Criar `.github/workflows/tests.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_ROOT_PASSWORD: test_password
          MYSQL_DATABASE: somos_darua_test
        ports:
          - 3306:3306
        options: >-
          --health-cmd="mysqladmin ping"
          --health-interval=10s
          --health-timeout=5s
          --health-retries=3

    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Setup database
        run: |
          mysql -h 127.0.0.1 -u root -ptest_password < database/schema/create_database.sql
        env:
          DB_HOST: 127.0.0.1
          DB_USER: root
          DB_PASSWORD: test_password
          DB_NAME: somos_darua_test

      - name: Run tests
        run: |
          pytest tests/ --cov=backend --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v2
        with:
          file: ./coverage.xml
```

---

## 📚 Recursos Adicionais

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest Coverage](https://pytest-cov.readthedocs.io/)
- [Testing Best Practices](https://testdriven.io/blog/testing-best-practices/)

---

[⬅️ Voltar ao Índice](./INDEX.md) | [➡️ Próximo: Deploy](./DEPLOY.md)
