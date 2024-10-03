-- schema.sql

CREATE DATABASE IF NOT EXISTS db_gerenciador_arquivos;
USE db_gerenciador_arquivos;

CREATE TABLE IF NOT EXISTS tb_folders (
    folder_id INT AUTO_INCREMENT PRIMARY KEY,
    folder_nome VARCHAR(255) NOT NULL,
    folder_is_deletado BOOLEAN DEFAULT FALSE,
    folder_data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    folder_data_modificacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tb_files (
    file_id INT AUTO_INCREMENT PRIMARY KEY,
    file_caminho_absoluto VARCHAR(500) NOT NULL,
    file_nome VARCHAR(255) NOT NULL,
    file_tamanho BIGINT,
    file_extensao VARCHAR(10),
    file_is_deletado BOOLEAN DEFAULT FALSE,
    folder_id INT,
    FOREIGN KEY (folder_id) REFERENCES tb_folders(folder_id),
    file_data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    file_data_modificacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tb_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    log_acao VARCHAR(50) NOT NULL,
    log_descricao TEXT NOT NULL,
    log_tabela_afetada VARCHAR(50) NOT NULL,
    log_registro_id INT NOT NULL,
    log_data_acoes TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER $$
CREATE TRIGGER after_insert_folder
AFTER INSERT ON tb_folders
FOR EACH ROW
BEGIN
    INSERT INTO tb_logs (log_acao, log_descricao, log_tabela_afetada, log_registro_id) 
    VALUES ('INSERT', CONCAT('Uma nova pasta com ID ', NEW.folder_id, ' foi criada.'), 'tb_folders', NEW.folder_id);
END $$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER after_update_folder
AFTER UPDATE ON tb_folders
FOR EACH ROW
BEGIN
    IF OLD.folder_nome <> NEW.folder_nome THEN 
        INSERT INTO tb_logs (log_acao, log_descricao, log_tabela_afetada, log_registro_id) 
        VALUES ('UPDATE', CONCAT('A pasta com ID ', NEW.folder_id, ' foi atualizada.'), 'tb_folders', NEW.folder_id);
    END IF;
END $$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER before_soft_delete_folder
BEFORE UPDATE ON tb_folders
FOR EACH ROW
BEGIN
    IF NEW.folder_is_deletado = TRUE AND OLD.folder_is_deletado = FALSE THEN 
        INSERT INTO tb_logs (log_acao, log_descricao, log_tabela_afetada, log_registro_id) 
        VALUES ('SOFT DELETE', CONCAT('A pasta com ID ', OLD.folder_id, ' foi marcada como deletada.'), 'tb_folders', OLD.folder_id);
    END IF;
END $$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER after_insert_file
AFTER INSERT ON tb_files
FOR EACH ROW
BEGIN
    INSERT INTO tb_logs (log_acao, log_descricao, log_tabela_afetada, log_registro_id)
    VALUES ('INSERT', CONCAT('Um novo arquivo com ID ', NEW.file_id, ' foi criado.'), 'tb_files', NEW.file_id);
END $$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER after_update_file
AFTER UPDATE ON tb_files
FOR EACH ROW
BEGIN
    IF OLD.file_nome <> NEW.file_nome THEN
        INSERT INTO tb_logs (log_acao, log_descricao, log_tabela_afetada, log_registro_id)
        VALUES ('UPDATE', CONCAT('O arquivo com ID ', NEW.file_id, ' foi atualizado.'), 'tb_files', NEW.file_id);
    END IF;
END $$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER before_soft_delete_file
BEFORE UPDATE ON tb_files
FOR EACH ROW
BEGIN
    IF NEW.file_is_deletado = TRUE AND OLD.file_is_deletado = FALSE THEN
        INSERT INTO tb_logs (log_acao, log_descricao, log_tabela_afetada, log_registro_id)
        VALUES ('SOFT DELETE', CONCAT('O arquivo com ID ', OLD.file_id, ' foi marcado como deletado.'), 'tb_files', OLD.file_id);
    END IF;
END $$
DELIMITER ;

CREATE INDEX idx_folder_id ON tb_files (folder_id);
CREATE INDEX idx_file_is_deletado ON tb_files (file_is_deletado);
CREATE INDEX idx_folder_is_deletado ON tb_folders (folder_is_deletado);
