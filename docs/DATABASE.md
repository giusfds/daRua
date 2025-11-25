# 🗄️ Banco de Dados - Somos DaRua

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Modelo Conceitual](#modelo-conceitual)
- [Diagrama ER](#diagrama-er)
- [Tabelas Principais](#tabelas-principais)
- [Tabelas de Relacionamento](#tabelas-de-relacionamento)
- [Relacionamentos](#relacionamentos)
- [Índices e Performance](#índices-e-performance)
- [Constraints e Validações](#constraints-e-validações)
- [Queries Comuns](#queries-comuns)
- [Migrations](#migrations)
- [Backup e Restore](#backup-e-restore)

---

## 🎯 Visão Geral

### Especificações Técnicas

- **SGBD**: MySQL 8.0
- **Charset**: `utf8mb4`
- **Collation**: `utf8mb4_unicode_ci`
- **Engine**: InnoDB (transações ACID)
- **Total de Tabelas**: 13
  - 8 Tabelas principais (entidades)
  - 5 Tabelas de relacionamento (N:N)

### Características

✅ **Integridade Referencial**: Foreign keys com CASCADE/RESTRICT
✅ **Performance**: Índices em colunas de busca e join
✅ **Validação**: Constraints e checks
✅ **UTF-8**: Suporte completo a caracteres especiais
✅ **Transações**: Suporte ACID completo

---

## 🏗️ Modelo Conceitual

### Entidades Principais

```
┌─────────────┐         ┌─────────────┐         ┌──────────────┐
│   DOADOR    │────►────│   DOAÇÃO    │────►────│ BENEFICIÁRIO │
└─────────────┘         └─────────────┘         └──────────────┘
                              │
                              │
                              ↓
                        ┌─────────────┐
                        │  CAMPANHA   │
                        └─────────────┘
                              │
                              │
                        ┌─────┴─────┐
                        ↓           ↓
                 ┌─────────────┐  ┌──────────────┐
                 │ NECESSIDADE │  │OBJETO DOÁVEL │
                 └─────────────┘  └──────────────┘
                                         │
                                         ↓
                                  ┌──────────────┐
                                  │PONTO COLETA  │
                                  └──────────────┘
```

---

## 📊 Diagrama ER (Entidade-Relacionamento)

### Versão Simplificada

```
┌───────────────────────┐
│       Doador          │
├───────────────────────┤
│ PK idDoador          │
│    Nome              │
│    Telefone          │
│    Email             │
│    Endereço...       │
└───────┬───────────────┘
        │
        │ 1:N
        │
        ↓
┌───────────────────────┐
│       Doacao          │
├───────────────────────┤
│ PK idDoacao          │
│    DataCriacao       │
│    DataEntrega       │
│ FK Doador_idDoador   │
│ FK Campanha_id       │
└───┬───────────┬───────┘
    │           │
    │ N:M       │ N:M
    │           │
    ↓           ↓
┌───────────┐   ┌────────────────┐
│ Benefic.  │   │ ObjetoDoavel   │
└───────────┘   └────────────────┘
```

### Versão Completa

```
                                    ┌──────────────────────┐
                                    │    CampanhaDoacao    │
                                    ├──────────────────────┤
                                    │ PK idCampanhaDoacao │
                                    │    Nome             │
                                    │    DataInicio       │
                                    │    DataTermino      │
                                    │    Descricao        │
                                    └──────┬──────┬────────┘
                                           │      │
                                    ┌──────┘      └──────┐
                                    │ N:M          N:M   │
                                    ↓                    ↓
┌───────────────────┐         ┌────────────┐      ┌──────────────┐
│      Doador       │         │Necessidade │      │ObjetoDoavel  │
├───────────────────┤         └────────────┘      ├──────────────┤
│ PK idDoador      │                              │PK idObjeto   │
│    Nome          │                              │  Nome        │
│    Telefone      │                              │  Descricao   │
│    Email         │                              │  Categoria   │
│    Logradouro    │                              │FK PontoColeta│
│    Numero        │                              └──────┬───────┘
│    Complemento   │                                     │
│    Bairro        │                                     │ N:1
│    Cidade        │                                     ↓
│    Estado        │                              ┌──────────────┐
│    CEP           │                              │ PontoColeta  │
└─────────┬─────────┘                             ├──────────────┤
          │                                       │PK idPonto    │
          │ 1:N                                   │  Responsavel │
          ↓                                       │  Logradouro  │
┌─────────────────────┐                          │  Numero      │
│       Doacao        │                          │  ...         │
├─────────────────────┤                          └──────────────┘
│ PK idDoacao        │
│    DataCriacao     │
│    DataEntrega     │
│ FK Doador_id       │
│ FK Campanha_id     │
└────┬──────┬──────┬──┘
     │      │      │
     │N:M   │N:M   │N:M
     │      │      │
     ↓      ↓      ↓
┌──────┐ ┌────────┐ ┌──────────┐
│Benef.│ │Objeto  │ │Voluntario│
└──────┘ └────────┘ └──────────┘
```

---

## 📋 Tabelas Principais

### 1. 👤 Doador

Pessoas ou empresas que fazem doações.

```sql
CREATE TABLE Doador (
    idDoador INT PRIMARY KEY AUTO_INCREMENT,
    Nome VARCHAR(255) NOT NULL,
    Telefone VARCHAR(20),
    Email VARCHAR(255),
    Logradouro VARCHAR(255),
    Numero VARCHAR(10),
    Complemento VARCHAR(80),
    Bairro VARCHAR(80),
    Cidade VARCHAR(80),
    Estado CHAR(2),
    CEP VARCHAR(9),
    INDEX idx_nome_doador (Nome)
) ENGINE=InnoDB;
```

**Campos:**

- `idDoador` (PK): Identificador único
- `Nome` (NOT NULL): Nome completo ou razão social
- `Telefone`: Contato telefônico
- `Email`: Email para comunicação
- `Endereço`: Logradouro, número, complemento, bairro, cidade, estado, CEP

**Índices:**

- `PRIMARY KEY` em `idDoador`
- `INDEX` em `Nome` (buscas por nome)

**Validações:**

- Nome obrigatório
- Estado deve ter 2 caracteres
- CEP deve ter 8 dígitos

---

### 2. 🤝 Beneficiario

Pessoas que recebem as doações.

```sql
CREATE TABLE Beneficiario (
    idBeneficiario INT PRIMARY KEY AUTO_INCREMENT,
    Nome VARCHAR(255) NOT NULL,
    Idade INT,
    Genero CHAR(1),
    Descricao VARCHAR(255),
    INDEX idx_nome_beneficiario (Nome),
    CHECK (Idade IS NULL OR Idade >= 0)
) ENGINE=InnoDB;
```

**Campos:**

- `idBeneficiario` (PK): Identificador único
- `Nome` (NOT NULL): Nome completo
- `Idade`: Idade (opcional)
- `Genero`: M/F/O (opcional)
- `Descricao`: Observações sobre o beneficiário

**Constraints:**

- `CHECK`: Idade não pode ser negativa

---

### 3. 📦 Doacao

Registro de doações realizadas.

```sql
CREATE TABLE Doacao (
    idDoacao INT PRIMARY KEY AUTO_INCREMENT,
    DataCriacao DATE NOT NULL DEFAULT (CURRENT_DATE),
    DataEntrega DATE,
    Doador_idDoador INT NOT NULL,
    CampanhaDoacao_idCampanhaDoacao INT,
    FOREIGN KEY (Doador_idDoador)
        REFERENCES Doador(idDoador)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (CampanhaDoacao_idCampanhaDoacao)
        REFERENCES CampanhaDoacao(idCampanhaDoacao)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    INDEX idx_doador (Doador_idDoador),
    INDEX idx_campanha (CampanhaDoacao_idCampanhaDoacao),
    INDEX idx_data_criacao (DataCriacao)
) ENGINE=InnoDB;
```

**Campos:**

- `idDoacao` (PK): Identificador único
- `DataCriacao` (NOT NULL, DEFAULT): Data de registro
- `DataEntrega`: Data de entrega ao beneficiário
- `Doador_idDoador` (FK, NOT NULL): Quem fez a doação
- `CampanhaDoacao_idCampanhaDoacao` (FK): Campanha relacionada (opcional)

**Foreign Keys:**

- `Doador_idDoador` → `Doador(idDoador)`
  - `ON DELETE RESTRICT`: Não permite excluir doador com doações
  - `ON UPDATE CASCADE`: Atualiza ID se o doador for alterado
- `CampanhaDoacao_idCampanhaDoacao` → `CampanhaDoacao(idCampanhaDoacao)`
  - `ON DELETE SET NULL`: Se campanha for excluída, doação permanece
  - `ON UPDATE CASCADE`: Atualiza ID se a campanha for alterada

---

### 4. 📢 CampanhaDoacao

Campanhas de arrecadação.

```sql
CREATE TABLE CampanhaDoacao (
    idCampanhaDoacao INT PRIMARY KEY AUTO_INCREMENT,
    Nome VARCHAR(255) NOT NULL,
    DataInicio DATE,
    DataTermino DATE,
    Descricao VARCHAR(255),
    INDEX idx_data_campanha (DataInicio, DataTermino),
    CHECK (DataTermino IS NULL OR DataInicio IS NULL
           OR DataTermino >= DataInicio)
) ENGINE=InnoDB;
```

**Campos:**

- `idCampanhaDoacao` (PK): Identificador único
- `Nome` (NOT NULL): Nome da campanha
- `DataInicio`: Início da campanha
- `DataTermino`: Término da campanha
- `Descricao`: Detalhes da campanha

**Constraints:**

- `CHECK`: DataTermino deve ser >= DataInicio

---

### 5. 📍 PontoColeta

Locais para recebimento de doações.

```sql
CREATE TABLE PontoColeta (
    idPontoColeta INT PRIMARY KEY AUTO_INCREMENT,
    Responsavel VARCHAR(255) NOT NULL,
    Logradouro VARCHAR(255),
    Numero VARCHAR(10),
    Complemento VARCHAR(80),
    Bairro VARCHAR(80),
    Cidade VARCHAR(80),
    Estado CHAR(2),
    CEP VARCHAR(9),
    INDEX idx_cidade_ponto (Cidade)
) ENGINE=InnoDB;
```

**Campos:**

- `idPontoColeta` (PK): Identificador único
- `Responsavel` (NOT NULL): Nome do responsável
- `Endereço`: Completo

---

### 6. 📦 ObjetoDoavel

Itens que podem ser doados.

```sql
CREATE TABLE ObjetoDoavel (
    idObjetoDoavel INT PRIMARY KEY AUTO_INCREMENT,
    Nome VARCHAR(255) NOT NULL,
    Descricao VARCHAR(255),
    Categoria VARCHAR(80),
    PontoColeta_idPontoColeta INT,
    FOREIGN KEY (PontoColeta_idPontoColeta)
        REFERENCES PontoColeta(idPontoColeta)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    INDEX idx_categoria (Categoria),
    INDEX idx_ponto_coleta (PontoColeta_idPontoColeta)
) ENGINE=InnoDB;
```

**Categorias Comuns:**

- Alimentos
- Roupas
- Calçados
- Móveis
- Eletrônicos
- Livros
- Brinquedos
- Higiene

---

### 7. 🙋 Voluntario

Pessoas que auxiliam nas ações.

```sql
CREATE TABLE Voluntario (
    idVoluntario INT PRIMARY KEY AUTO_INCREMENT,
    Nome VARCHAR(255) NOT NULL,
    Email VARCHAR(255),
    Telefone VARCHAR(20),
    INDEX idx_nome_voluntario (Nome)
) ENGINE=InnoDB;
```

---

### 8. 📝 Necessidade

Necessidades promovidas pelas campanhas.

```sql
CREATE TABLE Necessidade (
    idNecessidade INT PRIMARY KEY AUTO_INCREMENT,
    Descricao VARCHAR(255) NOT NULL,
    INDEX idx_descricao_necessidade (Descricao)
) ENGINE=InnoDB;
```

---

## 🔗 Tabelas de Relacionamento (N:N)

### 1. Contem (Doacao ↔ ObjetoDoavel)

Uma doação contém múltiplos objetos.

```sql
CREATE TABLE Contem (
    Doacao_idDoacao INT,
    ObjetoDoavel_idObjetoDoavel INT,
    PRIMARY KEY (Doacao_idDoacao, ObjetoDoavel_idObjetoDoavel),
    FOREIGN KEY (Doacao_idDoacao)
        REFERENCES Doacao(idDoacao) ON DELETE CASCADE,
    FOREIGN KEY (ObjetoDoavel_idObjetoDoavel)
        REFERENCES ObjetoDoavel(idObjetoDoavel) ON DELETE CASCADE
) ENGINE=InnoDB;
```

---

### 2. Recebe (Beneficiario ↔ Doacao)

Um beneficiário recebe múltiplas doações.

```sql
CREATE TABLE Recebe (
    Beneficiario_idBeneficiario INT,
    Doacao_idDoacao INT,
    PRIMARY KEY (Beneficiario_idBeneficiario, Doacao_idDoacao),
    FOREIGN KEY (Beneficiario_idBeneficiario)
        REFERENCES Beneficiario(idBeneficiario) ON DELETE CASCADE,
    FOREIGN KEY (Doacao_idDoacao)
        REFERENCES Doacao(idDoacao) ON DELETE CASCADE
) ENGINE=InnoDB;
```

---

### 3. Possui (Doacao ↔ Voluntario)

Uma doação pode ter múltiplos voluntários.

```sql
CREATE TABLE Possui (
    Doacao_idDoacao INT,
    Voluntario_idVoluntario INT,
    PRIMARY KEY (Doacao_idDoacao, Voluntario_idVoluntario),
    FOREIGN KEY (Doacao_idDoacao)
        REFERENCES Doacao(idDoacao) ON DELETE CASCADE,
    FOREIGN KEY (Voluntario_idVoluntario)
        REFERENCES Voluntario(idVoluntario) ON DELETE CASCADE
) ENGINE=InnoDB;
```

---

### 4. Promove (CampanhaDoacao ↔ Necessidade)

Uma campanha promove múltiplas necessidades.

```sql
CREATE TABLE Promove (
    CampanhaDoacao_idCampanhaDoacao INT,
    Necessidade_idNecessidade INT,
    PRIMARY KEY (CampanhaDoacao_idCampanhaDoacao, Necessidade_idNecessidade),
    FOREIGN KEY (CampanhaDoacao_idCampanhaDoacao)
        REFERENCES CampanhaDoacao(idCampanhaDoacao) ON DELETE CASCADE,
    FOREIGN KEY (Necessidade_idNecessidade)
        REFERENCES Necessidade(idNecessidade) ON DELETE CASCADE
) ENGINE=InnoDB;
```

---

### 5. Associa (ObjetoDoavel ↔ CampanhaDoacao)

Objetos associados a campanhas.

```sql
CREATE TABLE Associa (
    ObjetoDoavel_idObjetoDoavel INT,
    CampanhaDoacao_idCampanhaDoacao INT,
    PRIMARY KEY (ObjetoDoavel_idObjetoDoavel, CampanhaDoacao_idCampanhaDoacao),
    FOREIGN KEY (ObjetoDoavel_idObjetoDoavel)
        REFERENCES ObjetoDoavel(idObjetoDoavel) ON DELETE CASCADE,
    FOREIGN KEY (CampanhaDoacao_idCampanhaDoacao)
        REFERENCES CampanhaDoacao(idCampanhaDoacao) ON DELETE CASCADE
) ENGINE=InnoDB;
```

---

## 🔗 Relacionamentos

### Cardinalidade

| Relacionamento                | Tipo | Descrição                            |
| ----------------------------- | ---- | ------------------------------------ |
| Doador → Doacao               | 1:N  | Um doador faz várias doações         |
| Doacao ↔ Beneficiario         | N:M  | Uma doação para vários beneficiários |
| Doacao ↔ ObjetoDoavel         | N:M  | Uma doação contém vários objetos     |
| Doacao ↔ Voluntario           | N:M  | Voluntários atuam em várias doações  |
| CampanhaDoacao → Doacao       | 1:N  | Uma campanha tem várias doações      |
| CampanhaDoacao ↔ Necessidade  | N:M  | Campanha promove várias necessidades |
| CampanhaDoacao ↔ ObjetoDoavel | N:M  | Objetos associados a campanhas       |
| PontoColeta → ObjetoDoavel    | 1:N  | Ponto tem vários objetos             |

### Políticas de Deleção

| Foreign Key                | ON DELETE | Motivo                                 |
| -------------------------- | --------- | -------------------------------------- |
| Doacao → Doador            | RESTRICT  | Não pode excluir doador com doações    |
| Doacao → Campanha          | SET NULL  | Doação permanece sem campanha          |
| ObjetoDoavel → PontoColeta | SET NULL  | Objeto fica sem ponto                  |
| Tabelas N:N                | CASCADE   | Remove relacionamentos automaticamente |

---

## 🚀 Índices e Performance

### Índices Criados

```sql
-- Índices em Primary Keys (automático)
-- Todos os IDs têm índice clustered

-- Índices em Foreign Keys
CREATE INDEX idx_doador ON Doacao(Doador_idDoador);
CREATE INDEX idx_campanha ON Doacao(CampanhaDoacao_idCampanhaDoacao);
CREATE INDEX idx_ponto_coleta ON ObjetoDoavel(PontoColeta_idPontoColeta);

-- Índices em campos de busca
CREATE INDEX idx_nome_doador ON Doador(Nome);
CREATE INDEX idx_nome_beneficiario ON Beneficiario(Nome);
CREATE INDEX idx_nome_voluntario ON Voluntario(Nome);
CREATE INDEX idx_descricao_necessidade ON Necessidade(Descricao);

-- Índices em campos de filtro
CREATE INDEX idx_categoria ON ObjetoDoavel(Categoria);
CREATE INDEX idx_cidade_ponto ON PontoColeta(Cidade);
CREATE INDEX idx_data_criacao ON Doacao(DataCriacao);

-- Índice composto
CREATE INDEX idx_data_campanha ON CampanhaDoacao(DataInicio, DataTermino);
```

### Otimizações de Query

```sql
-- ✅ Usa índice (RÁPIDO)
SELECT * FROM Doador WHERE Nome LIKE 'João%';

-- ❌ Não usa índice (LENTO)
SELECT * FROM Doador WHERE UPPER(Nome) = 'JOÃO';

-- ✅ Usa índice composto
SELECT * FROM CampanhaDoacao
WHERE DataInicio >= '2024-01-01'
  AND DataTermino <= '2024-12-31';
```

---

## ✅ Constraints e Validações

### Check Constraints

```sql
-- Idade não negativa
ALTER TABLE Beneficiario
ADD CONSTRAINT chk_idade CHECK (Idade IS NULL OR Idade >= 0);

-- Data de término após início
ALTER TABLE CampanhaDoacao
ADD CONSTRAINT chk_datas CHECK (
    DataTermino IS NULL OR DataInicio IS NULL
    OR DataTermino >= DataInicio
);
```

### Not Null Constraints

Campos obrigatórios:

- `Doador.Nome`
- `Beneficiario.Nome`
- `Doacao.DataCriacao`
- `Doacao.Doador_idDoador`
- `CampanhaDoacao.Nome`
- `PontoColeta.Responsavel`
- `ObjetoDoavel.Nome`
- `Voluntario.Nome`
- `Necessidade.Descricao`

### Unique Constraints (Futuro)

```sql
-- Evitar emails duplicados
ALTER TABLE Doador ADD UNIQUE (Email);
ALTER TABLE Voluntario ADD UNIQUE (Email);
```

---

## 📝 Queries Comuns

### 1. Listar Doações com Doador

```sql
SELECT
    d.idDoacao,
    d.DataCriacao,
    d.DataEntrega,
    do.Nome AS Doador,
    c.Nome AS Campanha
FROM Doacao d
INNER JOIN Doador do ON d.Doador_idDoador = do.idDoador
LEFT JOIN CampanhaDoacao c ON d.CampanhaDoacao_idCampanhaDoacao = c.idCampanhaDoacao
ORDER BY d.DataCriacao DESC;
```

### 2. Objetos de uma Doação

```sql
SELECT
    o.Nome,
    o.Descricao,
    o.Categoria
FROM ObjetoDoavel o
INNER JOIN Contem c ON o.idObjetoDoavel = c.ObjetoDoavel_idObjetoDoavel
WHERE c.Doacao_idDoacao = ?;
```

### 3. Beneficiários de uma Doação

```sql
SELECT
    b.Nome,
    b.Idade,
    b.Genero
FROM Beneficiario b
INNER JOIN Recebe r ON b.idBeneficiario = r.Beneficiario_idBeneficiario
WHERE r.Doacao_idDoacao = ?;
```

### 4. Top 10 Doadores

```sql
SELECT
    d.Nome,
    COUNT(do.idDoacao) AS TotalDoacoes
FROM Doador d
INNER JOIN Doacao do ON d.idDoador = do.Doador_idDoador
GROUP BY d.idDoador, d.Nome
ORDER BY TotalDoacoes DESC
LIMIT 10;
```

### 5. Doações por Período

```sql
SELECT
    DATE_FORMAT(DataCriacao, '%Y-%m') AS Mes,
    COUNT(*) AS TotalDoacoes
FROM Doacao
WHERE DataCriacao BETWEEN '2024-01-01' AND '2024-12-31'
GROUP BY Mes
ORDER BY Mes;
```

### 6. Campanhas Ativas

```sql
SELECT
    Nome,
    DataInicio,
    DataTermino,
    Descricao
FROM CampanhaDoacao
WHERE CURRENT_DATE BETWEEN DataInicio AND DataTermino
ORDER BY DataInicio;
```

### 7. Objetos por Categoria

```sql
SELECT
    Categoria,
    COUNT(*) AS Quantidade
FROM ObjetoDoavel
WHERE Categoria IS NOT NULL
GROUP BY Categoria
ORDER BY Quantidade DESC;
```

---

## 🔄 Migrations

### Estrutura de Migrations

```
database/
└── migrations/
    ├── 001_initial_schema.sql
    ├── 002_add_indexes.sql
    ├── 003_add_constraints.sql
    └── ...
```

### Exemplo de Migration

```sql
-- migrations/002_add_email_unique.sql

-- Adicionar constraint UNIQUE em email
ALTER TABLE Doador
ADD CONSTRAINT uk_doador_email UNIQUE (Email);

ALTER TABLE Voluntario
ADD CONSTRAINT uk_voluntario_email UNIQUE (Email);
```

### Executar Migration

```bash
mysql -u root -p somos_darua < database/migrations/002_add_email_unique.sql
```

---

## 💾 Backup e Restore

### Backup Completo

```bash
# Backup do banco inteiro
mysqldump -u root -p somos_darua > backup_$(date +%Y%m%d).sql

# Backup apenas estrutura
mysqldump -u root -p --no-data somos_darua > schema_only.sql

# Backup apenas dados
mysqldump -u root -p --no-create-info somos_darua > data_only.sql
```

### Restore

```bash
# Restaurar backup
mysql -u root -p somos_darua < backup_20241125.sql

# Recriar banco e restaurar
mysql -u root -p -e "DROP DATABASE IF EXISTS somos_darua; CREATE DATABASE somos_darua;"
mysql -u root -p somos_darua < backup_20241125.sql
```

### Backup Automático (Cron)

```bash
# Adicionar ao crontab
0 2 * * * /usr/bin/mysqldump -u root -pSENHA somos_darua > /backups/somos_darua_$(date +\%Y\%m\%d).sql
```

---

## 📊 Estatísticas do Banco

### Tamanho das Tabelas

```sql
SELECT
    table_name AS Tabela,
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Tamanho (MB)',
    table_rows AS 'Linhas (Aprox.)'
FROM information_schema.tables
WHERE table_schema = 'somos_darua'
ORDER BY (data_length + index_length) DESC;
```

### Informações de Índices

```sql
SELECT
    TABLE_NAME AS Tabela,
    INDEX_NAME AS Indice,
    COLUMN_NAME AS Coluna,
    SEQ_IN_INDEX AS Ordem,
    INDEX_TYPE AS Tipo
FROM information_schema.STATISTICS
WHERE TABLE_SCHEMA = 'somos_darua'
ORDER BY TABLE_NAME, INDEX_NAME, SEQ_IN_INDEX;
```

---

## 🔧 Manutenção

### Otimizar Tabelas

```sql
-- Otimizar todas as tabelas
OPTIMIZE TABLE Doador, Beneficiario, Doacao, CampanhaDoacao,
               PontoColeta, ObjetoDoavel, Voluntario, Necessidade,
               Contem, Recebe, Possui, Promove, Associa;
```

### Analisar Tabelas

```sql
-- Atualizar estatísticas
ANALYZE TABLE Doador, Beneficiario, Doacao;
```

### Verificar Integridade

```sql
CHECK TABLE Doador, Beneficiario, Doacao;
```

---

## 📚 Referências

- [MySQL 8.0 Reference Manual](https://dev.mysql.com/doc/refman/8.0/en/)
- [MySQL Performance Tuning](https://dev.mysql.com/doc/refman/8.0/en/optimization.html)
- [InnoDB Storage Engine](https://dev.mysql.com/doc/refman/8.0/en/innodb-storage-engine.html)

---

[⬅️ Voltar ao Índice](./INDEX.md) | [➡️ Próximo: Desenvolvimento](./DESENVOLVIMENTO.md)
