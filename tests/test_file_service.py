# tests/test_file_service.py

import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from use_cases.file_service import FileService


@pytest.fixture
def file_service():
    db_url = os.getenv('DB_NAME')
    if db_url is None:
        raise ValueError(f"Variável de ambiente SQL - {db_url} não foi definida")

    engine = create_engine(db_url)
    session = Session(engine)

    return FileService(db=session)


def test_criar_arquivo(file_service, tmp_path):
    # Diretório temporário para criar o arquivo no SO
    file_path = tmp_path / "test_file.txt"
    novo_arquivo = file_service.criar_arquivo("test_file.txt", str(file_path), "conteúdo inicial")

    # Verifica se o arquivo foi criado no sistema operacional
    assert os.path.exists(file_path)

    # Verifica se o conteúdo do arquivo é o esperado
    with open(file_path, 'r', encoding='utf-8') as f:
        assert f.read() == "conteúdo inicial"

    # Verifica se o arquivo foi persistido no banco de dados
    assert novo_arquivo.nome == "test_file.txt"
    assert novo_arquivo.caminho == str(file_path)


def test_atualizar_arquivo(file_service, tmp_path):
    file_path = tmp_path / "test_file.txt"
    file_service.criar_arquivo("test_file.txt", str(file_path), "conteúdo inicial")

    # Atualiza o arquivo
    file_service.atualizar_arquivo("test_file.txt", "novo_conteúdo")

    # Verifica se o conteúdo foi atualizado
    with open(file_path, 'r', encoding='utf-8') as f:
        assert f.read() == "novo_conteúdo"


def test_deletar_arquivo(file_service, tmp_path):
    file_path = tmp_path / "test_file.txt"
    file_service.criar_arquivo("test_file.txt", str(file_path), "conteúdo inicial")

    # Deleta o arquivo
    file_service.deletar_arquivo("test_file.txt")

    # Verifica se o arquivo foi removido do SO
    assert not os.path.exists(file_path)

    # Verifica se foi removido do banco
    assert file_service.buscar_arquivo_por_nome("test_file.txt") is None
