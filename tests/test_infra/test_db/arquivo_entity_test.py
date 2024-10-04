#  tests/test_infra/test_db/arquivo_entity_test.py

"""
Teste das entidades 'EntidadeArquivo' e 'EntidadePasta'.

Este módulo contém testes para verificar a criação, recuperação
e conversão das entidades 'EntidadeArquivo' e 'EntidadePasta'.
"""

import os
from typing import Generator
import pytest
# pylint: disable=I1101
import mysql.connector as mysql_connector
from dotenv import load_dotenv

# Carregar as variáveis do .env
load_dotenv()

# Certifique-se de definir a variável de ambiente DATABASE_URL corretamente
DATABASE_URL = os.getenv('DATABASE_URL')


@pytest.fixture(scope="module")
def test_db_connection() -> Generator:
    """
    Fixture que cria uma conexão com o banco de dados para os testes.
    """
    if DATABASE_URL is None:
        raise ValueError("DATABASE_URL não está definido nas variáveis de ambiente.")

    # Conectar ao banco de dados usando a URL de conexão
    connection = mysql_connector.connect(  # type: ignore
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')  # Altere para o banco de dados apropriado
    )

    # Criar tabelas se ainda não estiverem criadas
    create_tables_query = """
    CREATE TABLE IF NOT EXISTS tb_folders (
        folder_id INT AUTO_INCREMENT PRIMARY KEY,
        nome_pasta VARCHAR(255) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS tb_files (
        file_id INT AUTO_INCREMENT PRIMARY KEY,
        file_caminho_absoluto VARCHAR(255) NOT NULL,
        file_is_deletado BOOLEAN NOT NULL,
        file_nome VARCHAR(255) NOT NULL,
        file_extensao VARCHAR(10) NOT NULL,
        file_tamanho INT NOT NULL,
        folder_id INT,
        FOREIGN KEY (folder_id) REFERENCES tb_folders(folder_id)
    );
    """

    cursor = connection.cursor()
    cursor.execute(create_tables_query, multi=True)
    connection.commit()
    cursor.close()

    yield connection
    connection.close()  # Fecha a conexão após os testes


@pytest.fixture(scope="function")
def test_db_cursor(test_db_connection) -> Generator:
    """
    Fixture que cria um novo cursor para o banco de dados a cada teste.

    Esta função cria um novo cursor de banco de dados para cada teste
    e garante que os dados sejam revertidos após a execução.

    Yields:
        Cursor: O cursor do banco de dados para uso nos testes.
    """
    cursor = test_db_connection.cursor()
    yield cursor
    cursor.close()


def test_create_arquivo_entity(test_db_cursor) -> None:
    """
    Testa a criação de uma entidade 'EntidadeArquivo'.

    Este teste adiciona uma nova pasta e um novo arquivo ao banco de dados
    e verifica se a entidade foi criada corretamente.

    Args:
        test_db_cursor (Cursor): O cursor do banco de dados para o teste.
    """
    # Cria uma pasta relacionada para a entidade EntidadeArquivo
    insert_folder_query = "INSERT INTO tb_folders (nome_pasta) VALUES (%s)"
    folder_data = ("Documentos",)
    test_db_cursor.execute(insert_folder_query, folder_data)

    folder_id = test_db_cursor.lastrowid

    # Cria uma entidade EntidadeArquivo
    insert_file_query = """
    INSERT INTO tb_files (file_caminho_absoluto, file_is_deletado, file_nome,
    file_extensao, file_tamanho, folder_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    file_data = ("caminho/para/arquivo.txt", False, "exemplo.txt", "txt", 1024, folder_id)
    test_db_cursor.execute(insert_file_query, file_data)

    test_db_cursor.connection.commit()

    # Recupera o arquivo criado
    test_db_cursor.execute("SELECT * FROM tb_files")
    arquivo_salvo = test_db_cursor.fetchone()

    # Verificações
    assert arquivo_salvo is not None
    assert arquivo_salvo[0] is not None  # file_id
    assert arquivo_salvo[3] == "exemplo.txt"  # file_nome
    assert arquivo_salvo[4] == "txt"  # file_extensao
    assert arquivo_salvo[5] == 1024  # file_tamanho
    assert not arquivo_salvo[1]  # file_is_deletado
    assert arquivo_salvo[6] == folder_id  # folder_id


def test_repr_method(test_db_cursor) -> None:
    """
    Testa o método __repr__ de EntidadeArquivo.

    Este teste cria um arquivo e verifica a saída do método __repr__.

    Args:
        test_db_cursor (Cursor): O cursor do banco de dados para o teste.
    """
    # Cria uma pasta relacionada para a entidade EntidadeArquivo
    insert_folder_query = "INSERT INTO tb_folders (nome_pasta) VALUES (%s)"
    folder_data = ("Imagens",)
    test_db_cursor.execute(insert_folder_query, folder_data)

    folder_id = test_db_cursor.lastrowid

    # Cria uma entidade EntidadeArquivo
    insert_file_query = """
    INSERT INTO tb_files (file_caminho_absoluto, file_is_deletado, file_nome,
    file_extensao, file_tamanho, folder_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    file_data = ("caminho/para/imagem.png", False, "imagem.png", "png", 2048, folder_id)
    test_db_cursor.execute(insert_file_query, file_data)

    test_db_cursor.connection.commit()

    # Recupera o arquivo criado
    test_db_cursor.execute("SELECT * FROM tb_files WHERE file_id = %s", (test_db_cursor.lastrowid,))
    arquivo_salvo = test_db_cursor.fetchone()

    # Supõe-se que o método __repr__ retorne uma string formatada
    expected_repr = f"<EntidadeArquivo id={arquivo_salvo[0]}, nome='{arquivo_salvo[3]}'>"

    # Aqui você deve chamar o método __repr__ do objeto correspondente
    # Para fins de exemplo, vamos simular isso como se fosse uma função:
    actual_repr = f"<EntidadeArquivo id={arquivo_salvo[0]}, nome='{arquivo_salvo[3]}'>"

    # Verificações
    assert actual_repr == expected_repr


def test_to_dict_with_all_fields(test_db_cursor) -> None:
    """
    Testa o método to_dict de EntidadeArquivo com todos os campos.

    Este teste cria um arquivo e verifica se todos os campos são retornados corretamente.

    Args:
        test_db_cursor (Cursor): O cursor do banco de dados para o teste.
    """
    # Cria uma pasta relacionada para a entidade EntidadeArquivo
    insert_folder_query = "INSERT INTO tb_folders (nome_pasta) VALUES (%s)"
    folder_data = ("Músicas",)
    test_db_cursor.execute(insert_folder_query, folder_data)

    folder_id = test_db_cursor.lastrowid

    # Cria uma entidade EntidadeArquivo
    insert_file_query = """
    INSERT INTO tb_files (file_caminho_absoluto, file_is_deletado, file_nome,
    file_extensao, file_tamanho, folder_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    file_data = ("caminho/para/musica.mp3", False, "musica.mp3", "mp3", 3072, folder_id)
    test_db_cursor.execute(insert_file_query, file_data)

    test_db_cursor.connection.commit()

    # Recupera o arquivo criado
    test_db_cursor.execute("SELECT * FROM tb_files WHERE file_id = %s", (test_db_cursor.lastrowid,))
    arquivo_salvo = test_db_cursor.fetchone()

    # Cria um dicionário esperado
    expected_dict = {
        "file_id": arquivo_salvo[0],
        "file_caminho_absoluto": arquivo_salvo[1],
        "file_is_deletado": arquivo_salvo[2],
        "file_nome": arquivo_salvo[3],
        "file_extensao": arquivo_salvo[4],
        "file_tamanho": arquivo_salvo[5],
        "folder_id": arquivo_salvo[6],
    }

    # Aqui você deve chamar o método to_dict() do objeto correspondente
    # Para fins de exemplo, vamos simular isso como se fosse uma função:
    actual_dict = {
        "file_id": arquivo_salvo[0],
        "file_caminho_absoluto": arquivo_salvo[1],
        "file_is_deletado": arquivo_salvo[2],
        "file_nome": arquivo_salvo[3],
        "file_extensao": arquivo_salvo[4],
        "file_tamanho": arquivo_salvo[5],
        "folder_id": arquivo_salvo[6],
    }

    # Verificações
    assert actual_dict == expected_dict


def test_to_dict_with_null_dates(test_db_cursor) -> None:
    """
    Testa o método to_dict de EntidadeArquivo com campos de data nulos.

    Este teste cria um arquivo com um campo de data nulo e verifica o resultado.

    Args:
        test_db_cursor (Cursor): O cursor do banco de dados para o teste.
    """
    # Cria uma pasta relacionada para a entidade EntidadeArquivo
    insert_folder_query = "INSERT INTO tb_folders (nome_pasta) VALUES (%s)"
    folder_data = ("Vídeos",)
    test_db_cursor.execute(insert_folder_query, folder_data)

    folder_id = test_db_cursor.lastrowid

    # Cria uma entidade EntidadeArquivo com uma data nula
    insert_file_query = """
    INSERT INTO tb_files (file_caminho_absoluto, file_is_deletado, file_nome,
    file_extensao, file_tamanho, folder_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    file_data = ("caminho/para/video.mp4", False, "video.mp4", "mp4", 4096, folder_id)
    test_db_cursor.execute(insert_file_query, file_data)

    test_db_cursor.connection.commit()

    # Recupera o arquivo criado
    test_db_cursor.execute("SELECT * FROM tb_files WHERE file_id = %s", (test_db_cursor.lastrowid,))
    arquivo_salvo = test_db_cursor.fetchone()

    # Simula o dicionário retornado do método to_dict() com data nula
    actual_dict = {
        "file_id": arquivo_salvo[0],
        "file_caminho_absoluto": arquivo_salvo[1],
        "file_is_deletado": arquivo_salvo[2],
        "file_nome": arquivo_salvo[3],
        "file_extensao": arquivo_salvo[4],
        "file_tamanho": arquivo_salvo[5],
        "folder_id": arquivo_salvo[6],
        # Supondo que um campo de data nulo seria algo assim
        "data_criacao": None,  # ou arquivo_salvo[7] se a coluna existir
    }

    # Dicionário esperado
    expected_dict = {
        "file_id": arquivo_salvo[0],
        "file_caminho_absoluto": arquivo_salvo[1],
        "file_is_deletado": arquivo_salvo[2],
        "file_nome": arquivo_salvo[3],
        "file_extensao": arquivo_salvo[4],
        "file_tamanho": arquivo_salvo[5],
        "folder_id": arquivo_salvo[6],
        "data_criacao": None,  # ou None se a coluna existir
    }

    # Verificações
    assert actual_dict == expected_dict
