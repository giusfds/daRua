-- ============================================================================
-- MIGRATION: Adicionar campos detalhados de doação
-- Data: 2024
-- Descrição: Adiciona colunas para armazenar informações completas das doações
--            (tipo, item, quantidade, unidade, ponto de coleta, observações)
-- ============================================================================

USE somos_darua;

-- Adicionar colunas na tabela Doacao
ALTER TABLE Doacao
ADD COLUMN TipoDoacao VARCHAR(50) DEFAULT 'Outros' AFTER DataEntrega,
ADD COLUMN DescricaoItem VARCHAR(255) AFTER TipoDoacao,
ADD COLUMN Quantidade DECIMAL(10,2) DEFAULT 1.00 AFTER DescricaoItem,
ADD COLUMN Unidade VARCHAR(20) DEFAULT 'Unidades' AFTER Quantidade,
ADD COLUMN Observacoes TEXT AFTER Unidade,
ADD COLUMN Status VARCHAR(50) DEFAULT 'Recebida' AFTER Observacoes;

-- Atualizar doações existentes (opcional - define valores padrão)
UPDATE Doacao 
SET TipoDoacao = 'Outros',
    DescricaoItem = 'Item não especificado',
    Quantidade = 1.00,
    Unidade = 'Unidades',
    Status = 'Recebida'
WHERE TipoDoacao IS NULL;

-- Verificar estrutura atualizada
DESCRIBE Doacao;

SELECT 'Colunas TipoDoacao, DescricaoItem, Quantidade, Unidade, Observacoes e Status adicionadas com sucesso!' AS Status;