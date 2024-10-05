-- complete_schema.sql
-- Criação do banco de dados e estrutura do sistema de gerenciamento de arquivos

-- ===========================
-- Criação das tabelas
-- ===========================

-- Criação da tabela de pastas (tb_folders)
CREATE TABLE IF NOT EXISTS tb_folders (
    folder_id INTEGER PRIMARY KEY,  -- ID da pasta
    folder_caminho_absoluto TEXT NOT NULL,  -- Caminho absoluto da pasta
    folder_nome TEXT NOT NULL,  -- Nome da pasta
    folder_is_deletado INTEGER DEFAULT 0,  -- Flag de soft delete (0 para False, 1 para True)
    folder_data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,  -- Data de criação
    folder_data_modificacao DATETIME DEFAULT CURRENT_TIMESTAMP  -- Data de modificação
);

-- Criação da tabela de arquivos (tb_files), com relacionamento à tabela de pastas
CREATE TABLE IF NOT EXISTS tb_files (
    file_id INTEGER PRIMARY KEY,  -- ID do arquivo
    file_caminho_absoluto TEXT NOT NULL,  -- Caminho absoluto do arquivo
    file_nome TEXT NOT NULL,  -- Nome do arquivo
    file_tamanho INTEGER,  -- Tamanho do arquivo em bytes
    file_extensao TEXT,  -- Extensão do arquivo
    file_is_deletado INTEGER DEFAULT 0,  -- Flag de soft delete (0 para False, 1 para True)
    folder_id INTEGER,  -- Relacionamento com a tabela de pastas
    FOREIGN KEY (folder_id) REFERENCES tb_folders(folder_id),  -- Referência à tabela de pastas
    file_data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,  -- Data de criação
    file_data_modificacao DATETIME DEFAULT CURRENT_TIMESTAMP  -- Data de modificação
);

-- Criação da tabela de logs (tb_logs) para registrar operações CRUD
CREATE TABLE IF NOT EXISTS tb_logs (
    log_id INTEGER PRIMARY KEY,  -- ID do log
    log_acao TEXT NOT NULL,  -- Exemplo: INSERT, UPDATE, SOFT DELETE
    log_descricao TEXT NOT NULL,  -- Descrição da ação realizada
    log_tabela_afetada TEXT NOT NULL,  -- Exemplo: tb_files, tb_folders
    log_registro_id INTEGER NOT NULL,  -- ID do registro afetado
    log_data_acoes DATETIME DEFAULT CURRENT_TIMESTAMP  -- Data da ação
);

-- ===========================
-- Inserção de dados
-- ===========================

-- Inserindo dados na tabela tb_folders
INSERT INTO tb_folders (folder_caminho_absoluto, folder_nome)
VALUES
('/usuarios/pedro/documentos', 'Documentos'),
('/usuarios/pedro/imagens', 'Imagens');

-- Inserindo dados na tabela tb_files
INSERT INTO tb_files (file_caminho_absoluto, file_nome, file_tamanho, file_extensao, folder_id)
VALUES 
('/usuarios/pedro/documentos/relatorio.pdf', 'relatorio.pdf', 102400, '.pdf', 1),
('/usuarios/pedro/imagens/foto.jpg', 'foto.jpg', 204800, '.jpg', 2);

-- ===========================
-- Soft Delete
-- ===========================

-- Soft delete de uma pasta (marca como deletada)
UPDATE tb_folders
SET folder_is_deletado = 1
WHERE folder_id = 1;

-- Soft delete de um arquivo (marca como deletado)
UPDATE tb_files
SET file_is_deletado = 1
WHERE file_id = 1;

-- ===========================
-- Consultas
-- ===========================

-- Consultar tb_logs das operações (logs devem incluir os soft deletes registrados automaticamente)
SELECT * FROM tb_logs;

-- Testando LEFT JOIN entre pastas e arquivos (exibindo arquivos não deletados)
SELECT f.*, fo.folder_nome AS nome_pasta
FROM tb_files f
LEFT JOIN tb_folders fo ON f.folder_id = fo.folder_id
WHERE f.file_is_deletado = 0;

-- Testando LEFT JOIN entre pastas e arquivos (exibindo pastas mesmo sem arquivos)
SELECT fo.*, f.file_nome
FROM tb_folders fo
LEFT JOIN tb_files f ON fo.folder_id = f.folder_id
WHERE fo.folder_is_deletado = 0;

-- Consultar arquivos não deletados e suas pastas
SELECT f.*, fo.folder_nome AS nome_pasta
FROM tb_files f
LEFT JOIN tb_folders fo ON f.folder_id = fo.folder_id
WHERE f.file_is_deletado = 0;

-- Consultar pastas e seus arquivos (mesmo aqueles deletados)
SELECT fo.*, f.*
FROM tb_folders fo
LEFT JOIN tb_files f ON fo.folder_id = f.folder_id;

-- ===========================
-- Criação de Triggers
-- ===========================

-- Trigger para registrar inserção de pastas
CREATE TRIGGER after_insert_folder
AFTER INSERT ON tb_folders
BEGIN
    INSERT INTO tb_logs (log_acao, log_descricao, log_tabela_afetada, log_registro_id)
    VALUES ('INSERT', 'Uma nova pasta com ID ' || NEW.folder_id || ' foi criada.', 'tb_folders', NEW.folder_id);
END;

-- Trigger para registrar atualização de pastas
CREATE TRIGGER after_update_folder
AFTER UPDATE ON tb_folders
BEGIN
    IF OLD.folder_nome <> NEW.folder_nome THEN
        INSERT INTO tb_logs (log_acao, log_descricao, log_tabela_afetada, log_registro_id)
        VALUES ('UPDATE', 'A pasta com ID ' || NEW.folder_id || ' foi atualizada.', 'tb_folders', NEW.folder_id);
    END IF;
END;

-- Trigger para registrar soft delete em pastas
CREATE TRIGGER before_soft_delete_folder
BEFORE UPDATE ON tb_folders
BEGIN
    IF NEW.folder_is_deletado = 1 AND OLD.folder_is_deletado = 0 THEN
        INSERT INTO tb_logs (log_acao, log_descricao, log_tabela_afetada, log_registro_id)
        VALUES ('SOFT DELETE', 'A pasta com ID ' || OLD.folder_id || ' foi marcada como deletada.', 'tb_folders', OLD.folder_id);
    END IF;
END;

-- Trigger para registrar inserção de arquivos
CREATE TRIGGER after_insert_file
AFTER INSERT ON tb_files
BEGIN
    INSERT INTO tb_logs (log_acao, log_descricao, log_tabela_afetada, log_registro_id)
    VALUES ('INSERT', 'Um novo arquivo com ID ' || NEW.file_id || ' foi criado.', 'tb_files', NEW.file_id);
END;

-- Trigger para registrar atualização de arquivos
CREATE TRIGGER after_update_file
AFTER UPDATE ON tb_files
BEGIN
    IF OLD.file_nome <> NEW.file_nome THEN
        INSERT INTO tb_logs (log_acao, log_descricao, log_tabela_afetada, log_registro_id)
        VALUES ('UPDATE', 'O arquivo com ID ' || NEW.file_id || ' foi atualizado.', 'tb_files', NEW.file_id);
    END IF;
END;

-- Trigger para registrar soft delete em arquivos
CREATE TRIGGER before_soft_delete_file
BEFORE UPDATE ON tb_files
BEGIN
    IF NEW.file_is_deletado = 1 AND OLD.file_is_deletado = 0 THEN
        INSERT INTO tb_logs (log_acao, log_descricao, log_tabela_afetada, log_registro_id)
        VALUES ('SOFT DELETE', 'O arquivo com ID ' || OLD.file_id || ' foi marcado como deletado.', 'tb_files', OLD.file_id);
    END IF;
END;
