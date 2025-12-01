-- Adicionar campos de meta e arrecadado em Campanhas
USE somos_darua;

ALTER TABLE CampanhaDoacao
ADD COLUMN Meta DECIMAL(10,2) DEFAULT 0.00 AFTER Descricao,
ADD COLUMN Arrecadado DECIMAL(10,2) DEFAULT 0.00 AFTER Meta,
ADD COLUMN TipoMeta VARCHAR(20) DEFAULT 'R$' AFTER Arrecadado;

-- Atualizar campanhas existentes (opcional)
UPDATE CampanhaDoacao SET Meta = 10000.00, Arrecadado = 0.00, TipoMeta = 'R$' WHERE Meta IS NULL;

SELECT 'Campos Meta, Arrecadado e TipoMeta adicionados com sucesso!' AS Status;