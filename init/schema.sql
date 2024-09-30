-- schema.sql
-- Criação e estrutura do banco de dados para o sistema de gerenciamento de arquivos

-- =========================
-- Criar banco de dados (se necessário)
-- =========================
CREATE DATABASE IF NOT EXISTS file_manager;

-- =========================
-- Selecionar banco de dados
-- =========================
USE file_manager;

-- =========================
-- TABELA: folders
-- =========================
CREATE TABLE IF NOT EXISTS folders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    folder_name VARCHAR(255) NOT NULL,
    parent_folder_id INT DEFAULT NULL,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW() ON UPDATE NOW(),
    CONSTRAINT fk_parent_folder FOREIGN KEY (parent_folder_id) REFERENCES folders(id) ON DELETE SET NULL
);

-- Índice para otimizar buscas por pastas ativas (não deletadas)
CREATE INDEX idx_folders_is_deleted ON folders (is_deleted);

-- =========================
-- TABELA: files
-- =========================
CREATE TABLE IF NOT EXISTS files (
    id INT PRIMARY KEY AUTO_INCREMENT,
    folder_id INT NOT NULL,
    filename VARCHAR(255) NOT NULL,
    file_extension ENUM('txt', 'docx', 'pdf', 'html', 'csv') NOT NULL,
    size_in_bytes INT CHECK (size_in_bytes >= 0),
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW() ON UPDATE NOW(),
    CONSTRAINT fk_folder FOREIGN KEY (folder_id) REFERENCES folders(id) ON DELETE CASCADE,
    CONSTRAINT unq_filename_extension UNIQUE (folder_id, filename, file_extension)
);

-- Índice para otimizar buscas de arquivos ativos dentro de pastas específicas
CREATE INDEX idx_files_folder_id ON files (folder_id, is_deleted);
CREATE INDEX idx_files_is_deleted ON files (is_deleted);

-- =========================
-- TABELA: file_metadata
-- =========================
CREATE TABLE IF NOT EXISTS file_metadata (
    id INT PRIMARY KEY AUTO_INCREMENT,
    file_id INT NOT NULL,
    author VARCHAR(255) DEFAULT 'Desconhecido',
    last_modified TIMESTAMP DEFAULT NOW() ON UPDATE NOW(),
    created_by VARCHAR(255) DEFAULT 'Sistema',
    CONSTRAINT fk_file FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE
);

-- Índice para otimizar buscas por metadados
CREATE INDEX idx_file_metadata_file_id ON file_metadata (file_id);

-- =========================
-- TABELA: file_logs
-- =========================
CREATE TABLE IF NOT EXISTS file_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    file_id INT NOT NULL,
    action ENUM('created', 'updated', 'deleted', 'restored') NOT NULL,
    log_timestamp TIMESTAMP DEFAULT NOW(),
    description TEXT,
    CONSTRAINT fk_file_logs FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE
);

-- Índice para otimizar buscas por logs de arquivos
CREATE INDEX idx_file_logs_file_id ON file_logs (file_id);
