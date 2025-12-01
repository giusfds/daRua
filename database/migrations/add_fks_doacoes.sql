-- ============================================================================
-- MIGRATION: Adicionar campos de Ponto de Coleta e Voluntário Responsável
-- Data: 2024
-- Descrição: Adiciona FKs obrigatórias para registrar onde a doação foi 
--            recebida e quem foi o voluntário responsável pelo registro
-- ============================================================================

USE somos_darua;

-- ============================================================================
-- PASSO 1: Adicionar as colunas (inicialmente NULL para compatibilidade)
-- ============================================================================

ALTER TABLE Doacao 
ADD COLUMN PontoColeta_idPontoColeta INT NULL COMMENT 'Ponto de coleta onde a doação foi recebida'
AFTER CampanhaDoacao_idCampanhaDoacao;

ALTER TABLE Doacao 
ADD COLUMN VoluntarioColeta_idVoluntario INT NULL COMMENT 'Voluntário responsável pelo registro da doação'
AFTER PontoColeta_idPontoColeta;

-- ============================================================================
-- PASSO 2: Adicionar índices para melhorar performance
-- ============================================================================

ALTER TABLE Doacao 
ADD INDEX idx_ponto_coleta (PontoColeta_idPontoColeta);

ALTER TABLE Doacao 
ADD INDEX idx_voluntario_coleta (VoluntarioColeta_idVoluntario);

-- ============================================================================
-- PASSO 3: Adicionar Foreign Keys
-- ============================================================================

ALTER TABLE Doacao 
ADD CONSTRAINT fk_doacao_ponto_coleta
    FOREIGN KEY (PontoColeta_idPontoColeta) 
    REFERENCES PontoColeta(idPontoColeta)
    ON DELETE RESTRICT 
    ON UPDATE CASCADE;

ALTER TABLE Doacao 
ADD CONSTRAINT fk_doacao_voluntario_coleta
    FOREIGN KEY (VoluntarioColeta_idVoluntario) 
    REFERENCES Voluntario(idVoluntario)
    ON DELETE RESTRICT 
    ON UPDATE CASCADE;

-- ============================================================================
-- VERIFICAÇÃO
-- ============================================================================

-- Verificar estrutura atualizada
DESCRIBE Doacao;

SELECT 'Campos PontoColeta_idPontoColeta e VoluntarioColeta_idVoluntario adicionados com sucesso!' AS Status;

-- ============================================================================
-- ROLLBACK (se necessário desfazer)
-- ============================================================================
-- Execute os comandos abaixo EM ORDEM se precisar reverter:

-- ALTER TABLE Doacao DROP FOREIGN KEY fk_doacao_voluntario_coleta;
-- ALTER TABLE Doacao DROP FOREIGN KEY fk_doacao_ponto_coleta;
-- ALTER TABLE Doacao DROP INDEX idx_voluntario_coleta;
-- ALTER TABLE Doacao DROP INDEX idx_ponto_coleta;
-- ALTER TABLE Doacao DROP COLUMN VoluntarioColeta_idVoluntario;
-- ALTER TABLE Doacao DROP COLUMN PontoColeta_idPontoColeta;