-- schema.sql
-- Criação e estrutura do banco de dados para o sistema de gerenciamento de arquivos

-- =========================
-- Criar banco de dados (se necessário)
-- =========================
CREATE DATABASE IF NOT EXISTS gerenciamento_arquivos_db;

-- =========================
-- Selecionar banco de dados
-- =========================
USE gerenciamento_arquivos_db;

-- =========================
-- TABELA: tb_diretorios
-- =========================
CREATE TABLE IF NOT EXISTS tb_pastas (
    id_diretorio INT PRIMARY KEY AUTO_INCREMENT,
    nome_diretorio VARCHAR(255) NOT NULL,
    id_diretorio_mae INT DEFAULT NULL,
    is_excluida BOOLEAN DEFAULT FALSE,
    data_criacao TIMESTAMP DEFAULT NOW(),
    data_atualizacao TIMESTAMP DEFAULT NOW() ON UPDATE NOW(),
    CONSTRAINT fk_diretorio_mae FOREIGN KEY (id_diretorio_mae) REFERENCES tb_pastas(id_diretorio) ON DELETE SET NULL
);

-- Índice para otimizar buscas por diretorios não excluídos
CREATE INDEX idx_diretorio_is_excluida ON tb_pastas (is_excluida);

-- =========================
-- TABELA: tb_arquivos
-- =========================
CREATE TABLE IF NOT EXISTS tb_arquivos (
    id_arquivo INT PRIMARY KEY AUTO_INCREMENT,
    id_diretorio INT NOT NULL,
    nome_arquivo VARCHAR(255) NOT NULL,
    extensao_arquivo ENUM('txt', 'docx', 'pdf', 'html', 'csv') NOT NULL,
    tamanho_arquivo_bytes INT CHECK (tamanho_arquivo_bytes >= 0),
    is_excluido BOOLEAN DEFAULT FALSE,
    data_criacao TIMESTAMP DEFAULT NOW(),
    data_atualizacao TIMESTAMP DEFAULT NOW() ON UPDATE NOW(),
    CONSTRAINT fk_diretorio FOREIGN KEY (id_diretorio) REFERENCES tb_pastas(id_diretorio) ON DELETE CASCADE,
    CONSTRAINT unq_nome_extensao UNIQUE (id_diretorio, nome_arquivo, extensao_arquivo)
);

-- Índice para otimizar buscas de arquivos não excluídos dentro de diretorios
CREATE INDEX idx_arquivo_id_diretorio ON tb_arquivos (id_diretorio, is_excluido);
CREATE INDEX idx_arquivo_is_excluido ON tb_arquivos (is_excluido);

-- =========================
-- TABELA: tb_arquivo_metadados
-- =========================
CREATE TABLE IF NOT EXISTS tb_arquivo_metadados (
    id_metadado INT PRIMARY KEY AUTO_INCREMENT,
    id_arquivo INT NOT NULL,
    autor VARCHAR(255) DEFAULT 'Desconhecido',
    data_modificacao TIMESTAMP DEFAULT NOW() ON UPDATE NOW(),
    criado_por VARCHAR(255) DEFAULT 'Sistema',
    CONSTRAINT fk_arquivo FOREIGN KEY (id_arquivo) REFERENCES tb_arquivos(id_arquivo) ON DELETE CASCADE
);

-- Índice para otimizar buscas por metadados
CREATE INDEX idx_metadado_id_arquivo ON tb_arquivo_metadados (id_arquivo);

-- =========================
-- TABELA: tb_logs_arquivo
-- =========================
CREATE TABLE IF NOT EXISTS tb_logs_arquivo (
    id_log INT PRIMARY KEY AUTO_INCREMENT,
    id_arquivo INT NOT NULL,
    acao ENUM('criado', 'atualizado', 'excluido', 'restaurado', 'metadado_adicionado', 'metadado_atualizado') NOT NULL,
    data_log TIMESTAMP DEFAULT NOW(),
    descricao TEXT,
    CONSTRAINT fk_log_arquivo FOREIGN KEY (id_arquivo) REFERENCES tb_arquivos(id_arquivo) ON DELETE CASCADE
);

-- Índice para otimizar buscas por logs de arquivos
CREATE INDEX idx_log_id_arquivo ON tb_logs_arquivo (id_arquivo);

-- =========================
-- TABELA: tb_logs_diretorios
-- =========================
CREATE TABLE IF NOT EXISTS tb_logs_diretorios (
    id_log_diretorio INT PRIMARY KEY AUTO_INCREMENT,
    id_diretorio INT NOT NULL,
    acao ENUM('criado', 'atualizado', 'excluido') NOT NULL,
    data_log TIMESTAMP DEFAULT NOW(),
    descricao TEXT,
    CONSTRAINT fk_log_diretorio FOREIGN KEY (id_diretorio) REFERENCES tb_pastas(id_diretorio) ON DELETE CASCADE
);

-- Índice para otimizar buscas por logs de diretórios
CREATE INDEX idx_log_diretorio_id ON tb_logs_diretorios (id_diretorio);

-- =========================
-- EXEMPLOS DE USO - CRUD
-- =========================

-- 1. INSERIR dados nas tabelas

-- Inserir uma nova pasta (Raiz)
INSERT INTO tb_pastas (nome_diretorio) 
VALUES ('Documentos Importantes');

-- Inserir log de criação do diretório
INSERT INTO tb_logs_diretorios (id_diretorio, acao, descricao)
VALUES (1, 'criado', 'Diretório Documentos Importantes criado.');

-- Inserir uma subdiretorio
INSERT INTO tb_pastas (nome_diretorio, id_diretorio_mae) 
VALUES ('Trabalhos', 1);

-- Inserir log de criação da subdiretório
INSERT INTO tb_logs_diretorios (id_diretorio, acao, descricao)
VALUES (2, 'criado', 'Subdiretório Trabalhos criado.');

-- Inserir um arquivo na subdiretorio
INSERT INTO tb_arquivos (id_diretorio, nome_arquivo, extensao_arquivo, tamanho_arquivo_bytes)
VALUES (2, 'relatorio', 'pdf', 204800);

-- Inserir metadados para o arquivo
INSERT INTO tb_arquivo_metadados (id_arquivo, autor, criado_por)
VALUES (1, 'João Silva', 'Sistema');

-- Inserir log de criação do arquivo
INSERT INTO tb_logs_arquivo (id_arquivo, acao, descricao)
VALUES (1, 'criado', 'Arquivo criado por João Silva.');

-- 2. CONSULTAR dados nas tabelas

-- Buscar todas as diretorios ativos
SELECT * FROM tb_pastas WHERE is_excluida = FALSE;

-- Buscar todos os arquivos ativos dentro de uma pasta
SELECT * FROM tb_arquivos WHERE id_diretorio = 2 AND is_excluido = FALSE;

-- Buscar metadados de um arquivo
SELECT * FROM tb_arquivo_metadados WHERE id_arquivo = 1;

-- Buscar logs de um arquivo específico
SELECT * FROM tb_logs_arquivo WHERE id_arquivo = 1;

-- Buscar logs de um diretório específico
SELECT * FROM tb_logs_diretorios WHERE id_diretorio = 1;

-- 3. ATUALIZAR dados nas tabelas

-- Atualizar nome da pasta
UPDATE tb_pastas 
SET nome_diretorio = 'Documentos Pessoais', data_atualizacao = NOW() 
WHERE id_diretorio = 1;

-- Inserir log de atualização do diretório
INSERT INTO tb_logs_diretorios (id_diretorio, acao, descricao)
VALUES (1, 'atualizado', 'Diretório Documentos Importantes renomeado para Documentos Pessoais.');

-- Atualizar nome do arquivo
UPDATE tb_arquivos 
SET nome_arquivo = 'relatorio_final', data_atualizacao = NOW() 
WHERE id_arquivo = 1;

-- Inserir log de atualização do arquivo
INSERT INTO tb_logs_arquivo (id_arquivo, acao, descricao)
VALUES (1, 'atualizado', 'Arquivo relatorio renomeado para relatorio_final.');

-- Restaurar um arquivo excluído
UPDATE tb_arquivos 
SET is_excluido = FALSE, data_atualizacao = NOW() 
WHERE id_arquivo = 1;

-- Inserir log de restauração do arquivo
INSERT INTO tb_logs_arquivo (id_arquivo, acao, descricao)
VALUES (1, 'restaurado', 'Arquivo restaurado por João Silva.');

-- 4. EXCLUIR (marcar como excluído)

-- Excluir logicamente um arquivo
UPDATE tb_arquivos 
SET is_excluido = TRUE, data_atualizacao = NOW() 
WHERE id_arquivo = 1;

-- Inserir log de exclusão
INSERT INTO tb_logs_arquivo (id_arquivo, acao, descricao)
VALUES (1, 'excluido', 'Arquivo excluído por João Silva.');

-- Excluir logicamente um diretório
UPDATE tb_pastas 
SET is_excluida = TRUE, data_atualizacao = NOW() 
WHERE id_diretorio = 1;

-- Inserir log de exclusão do diretório
INSERT INTO tb_logs_diretorios (id_diretorio, acao, descricao)
VALUES (1, 'excluido', 'Diretório Documentos Pessoais excluído.');

DELIMITER //
CREATE TRIGGER before_update_tb_pastas
BEFORE UPDATE ON tb_pastas
FOR EACH ROW
BEGIN
    SET NEW.data_atualizacao = NOW();
END; //
DELIMITER ;
