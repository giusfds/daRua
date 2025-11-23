-- =====================================================
-- Script de Criação do Banco de Dados - Somos DaRua
-- =====================================================
-- Remove banco anterior se existir
DROP DATABASE IF EXISTS somos_darua;

-- Cria banco com UTF-8
CREATE DATABASE somos_darua
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE somos_darua;

-- =====================================================
-- TABELAS PRINCIPAIS
-- =====================================================

-- Tabela: Doador
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

-- Tabela: Beneficiario
CREATE TABLE Beneficiario (
    idBeneficiario INT PRIMARY KEY AUTO_INCREMENT,
    Nome VARCHAR(255) NOT NULL,
    Idade INT,
    Genero CHAR(1),
    Descricao VARCHAR(255),
    INDEX idx_nome_beneficiario (Nome),
    CHECK (Idade IS NULL OR Idade >= 0)
) ENGINE=InnoDB;

-- Tabela: PontoColeta
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

-- Tabela: ObjetoDoavel
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

-- Tabela: CampanhaDoacao
CREATE TABLE CampanhaDoacao (
    idCampanhaDoacao INT PRIMARY KEY AUTO_INCREMENT,
    Nome VARCHAR(255) NOT NULL,
    DataInicio DATE,
    DataTermino DATE,
    Descricao VARCHAR(255),
    INDEX idx_data_campanha (DataInicio, DataTermino),
    CHECK (DataTermino IS NULL OR DataInicio IS NULL OR DataTermino >= DataInicio)
) ENGINE=InnoDB;

-- Tabela: Voluntario
CREATE TABLE Voluntario (
    idVoluntario INT PRIMARY KEY AUTO_INCREMENT,
    Nome VARCHAR(255) NOT NULL,
    Email VARCHAR(255),
    Telefone VARCHAR(20),
    INDEX idx_nome_voluntario (Nome)
) ENGINE=InnoDB;

-- Tabela: Necessidade
CREATE TABLE Necessidade (
    idNecessidade INT PRIMARY KEY AUTO_INCREMENT,
    Descricao VARCHAR(255) NOT NULL,
    INDEX idx_descricao_necessidade (Descricao)
) ENGINE=InnoDB;

-- Tabela: Doacao
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

-- =====================================================
-- TABELAS DE RELACIONAMENTO N:N
-- =====================================================

-- Relacionamento: Doacao CONTEM ObjetoDoavel
CREATE TABLE Contem (
    Doacao_idDoacao INT,
    ObjetoDoavel_idObjetoDoavel INT,
    PRIMARY KEY (Doacao_idDoacao, ObjetoDoavel_idObjetoDoavel),
    FOREIGN KEY (Doacao_idDoacao) 
        REFERENCES Doacao(idDoacao)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (ObjetoDoavel_idObjetoDoavel) 
        REFERENCES ObjetoDoavel(idObjetoDoavel)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- Relacionamento: Beneficiario RECEBE Doacao
CREATE TABLE Recebe (
    Beneficiario_idBeneficiario INT,
    Doacao_idDoacao INT,
    PRIMARY KEY (Beneficiario_idBeneficiario, Doacao_idDoacao),
    FOREIGN KEY (Beneficiario_idBeneficiario) 
        REFERENCES Beneficiario(idBeneficiario)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (Doacao_idDoacao) 
        REFERENCES Doacao(idDoacao)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- Relacionamento: Doacao POSSUI Voluntario
CREATE TABLE Possui (
    Doacao_idDoacao INT,
    Voluntario_idVoluntario INT,
    PRIMARY KEY (Doacao_idDoacao, Voluntario_idVoluntario),
    FOREIGN KEY (Doacao_idDoacao) 
        REFERENCES Doacao(idDoacao)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (Voluntario_idVoluntario) 
        REFERENCES Voluntario(idVoluntario)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- Relacionamento: CampanhaDoacao PROMOVE Necessidade
CREATE TABLE Promove (
    CampanhaDoacao_idCampanhaDoacao INT,
    Necessidade_idNecessidade INT,
    PRIMARY KEY (CampanhaDoacao_idCampanhaDoacao, Necessidade_idNecessidade),
    FOREIGN KEY (CampanhaDoacao_idCampanhaDoacao) 
        REFERENCES CampanhaDoacao(idCampanhaDoacao)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (Necessidade_idNecessidade) 
        REFERENCES Necessidade(idNecessidade)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- Relacionamento: ObjetoDoavel ASSOCIA CampanhaDoacao
CREATE TABLE Associa (
    ObjetoDoavel_idObjetoDoavel INT,
    CampanhaDoacao_idCampanhaDoacao INT,
    PRIMARY KEY (ObjetoDoavel_idObjetoDoavel, CampanhaDoacao_idCampanhaDoacao),
    FOREIGN KEY (ObjetoDoavel_idObjetoDoavel) 
        REFERENCES ObjetoDoavel(idObjetoDoavel)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (CampanhaDoacao_idCampanhaDoacao) 
        REFERENCES CampanhaDoacao(idCampanhaDoacao)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- =====================================================
-- Mensagem de Sucesso
-- =====================================================
SELECT 'Banco criado com 13 tabelas!' AS Status;