# tests/test_infra/test_db/arquivo_entity_test.py

import os
import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infra.db.settings.base import Base
from src.infra.db.entities.pasta_entity import EntidadePasta
from src.infra.db.entities.arquivo_entity import EntidadeArquivo

# Carregar as variáveis do .env
load_dotenv()

# Usar a URL do banco de dados a partir do .env
DATABASE_URL = os.getenv("DATABASE_URL")


@pytest.fixture(scope="module")
def test_db_engine():
    """Fixture que cria uma engine do banco de dados para os testes."""
    if DATABASE_URL is None:
        raise ValueError(
            "DATABASE_URL não está definido nas variáveis de ambiente.")

    engine = create_engine(DATABASE_URL)

    # Criar as tabelas se ainda não estiverem criadas
    with engine.connect() as connection:
        if not engine.dialect.has_table(connection, "tb_pastas"):
            Base.metadata.create_all(engine)

    yield engine
    engine.dispose()  # Fecha a conexão após os testes


@pytest.fixture(scope="function")
def test_db_session(test_db_engine):
    """Fixture que cria uma nova sessão para o banco de dados a cada teste."""
    session_local = sessionmaker(bind=test_db_engine)
    session = session_local()
    yield session
    session.rollback()  # Faz rollback para limpar o banco após cada teste
    session.close()


def test_create_arquivo_entity(test_db_session):
    """Testa a criação de uma entidade 'EntidadeArquivo'."""
    # Cria uma pasta relacionada para a entidade EntidadeArquivo
    pasta = EntidadePasta(nome_pasta="Documentos")
    test_db_session.add(pasta)
    test_db_session.commit()

    # Cria uma entidade EntidadeArquivo
    novo_arquivo = EntidadeArquivo(
        id_pasta=pasta.id_pasta,
        nome_arquivo="exemplo.txt",
        extensao_arquivo="txt",
        tamanho_em_bytes=1024,
    )
    test_db_session.add(novo_arquivo)
    test_db_session.commit()

    # Recupera o arquivo criado
    arquivo_salvo = test_db_session.query(EntidadeArquivo).first()

    # Verificações
    assert arquivo_salvo is not None
    assert arquivo_salvo.id_arquivo is not None
    assert arquivo_salvo.nome_arquivo == "exemplo.txt"
    assert arquivo_salvo.extensao_arquivo == "txt"
    assert arquivo_salvo.tamanho_em_bytes == 1024
    assert arquivo_salvo.is_excluido is False
    assert arquivo_salvo.id_pasta == pasta.id_pasta


def test_repr_method(test_db_session):
    """Testa o método __repr__ da entidade EntidadeArquivo."""
    # Cria uma pasta relacionada para a entidade EntidadeArquivo
    pasta = EntidadePasta(nome_pasta="Documentos")
    test_db_session.add(pasta)
    test_db_session.commit()

    # Cria uma entidade EntidadeArquivo
    novo_arquivo = EntidadeArquivo(
        id_pasta=pasta.id_pasta,
        nome_arquivo="documento.pdf",
        extensao_arquivo="pdf",
        tamanho_em_bytes=2048,
    )
    test_db_session.add(novo_arquivo)
    test_db_session.commit()

    # Verifica a saída do método __repr__
    expected_repr = (
        f"EntidadeArquivo(id={novo_arquivo.id_arquivo}, "
        f"nome_arquivo='documento.pdf', extensao_arquivo='pdf')"
    )
    assert repr(novo_arquivo) == expected_repr


def test_to_dict_with_all_fields(test_db_session):
    """Testa o método to_dict com todos os campos preenchidos."""
    pasta = EntidadePasta(nome_pasta="Imagens")
    test_db_session.add(pasta)
    test_db_session.commit()

    arquivo = EntidadeArquivo(
        id_pasta=pasta.id_pasta,
        nome_arquivo="paisagem.jpg",
        extensao_arquivo="jpg",
        tamanho_em_bytes=5120,
    )
    test_db_session.add(arquivo)
    test_db_session.commit()

    arquivo_dict = arquivo.to_dict()

    assert arquivo_dict["id_arquivo"] == arquivo.id_arquivo
    assert arquivo_dict["id_pasta"] == arquivo.id_pasta
    assert arquivo_dict["nome_arquivo"] == "paisagem.jpg"
    assert arquivo_dict["extensao_arquivo"] == "jpg"
    assert arquivo_dict["tamanho_arquivo_bytes"] == 5120
    assert arquivo_dict["is_excluido"] is False
    assert arquivo_dict["data_criacao"] is not None
    assert arquivo_dict["data_atualizacao"] is not None


def test_to_dict_with_null_dates(test_db_session):
    """Testa o método to_dict com datas nulas."""
    pasta = EntidadePasta(nome_pasta="Downloads")
    test_db_session.add(pasta)
    test_db_session.commit()

    arquivo = EntidadeArquivo(
        id_pasta=pasta.id_pasta,
        nome_arquivo="arquivo.zip",
        extensao_arquivo="zip",
        tamanho_em_bytes=10240,
    )
    test_db_session.add(arquivo)
    test_db_session.commit()

    arquivo_dict = arquivo.to_dict()

    assert arquivo_dict["data_criacao"] is None
    assert arquivo_dict["data_atualizacao"] is None
