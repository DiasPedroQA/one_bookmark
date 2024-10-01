# tests/test_infra/test_db/arquivo_entity_test.py
import os
import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infra.db.settings.base import Base
from infra.db.entities.pasta_entity import EntidadePasta
from infra.db.entities.arquivo_entity import EntidadeArquivo

# Carregar as variáveis do .env
load_dotenv()

# Usar a URL do banco de dados a partir do .env
DATABASE_URL = os.getenv("DATABASE_URL")


@pytest.fixture(scope="module")
def test_db_engine():
    """
    Fixture que cria uma engine do banco de dados para os testes.
    """
    engine = create_engine(DATABASE_URL)

    # Criar as tabelas se ainda não estiverem criadas
    if not engine.dialect.has_table(engine, "tb_pastas"):
        # Verifica se a tabela já existe
        Base.metadata.create_all(engine)

    yield engine
    engine.dispose()  # Fecha a conexão após os testes


@pytest.fixture(scope="function")
def test_db_session(test_db_engine):
    # Renomeado de db_session para test_db_session
    """
    Fixture que cria uma nova sessão para o banco de dados a cada teste.
    """
    session_local = sessionmaker(bind=test_db_engine)
    session = session_local()
    yield session
    session.rollback()  # Faz rollback para limpar o banco após cada teste
    session.close()


def test_create_arquivo_entity(test_db_session):
    # Alterado para usar test_db_session
    """
    Testa a criação de uma entidade 'EntidadeArquivo'
    e verifica se os atributos são armazenados corretamente.
    """
    # Cria uma pasta relacionada para a entidade EntidadeArquivo
    pasta = EntidadePasta(name="Documentos")
    test_db_session.add(pasta)
    test_db_session.commit()

    # Cria uma entidade EntidadeArquivo
    new_arquivo = EntidadeArquivo(
        pasta_id=pasta.id,
        nome_arquivo="exemplo.txt",
        extensao_arquivo="txt",
        tamanho_em_bytes=1024,
    )
    test_db_session.add(new_arquivo)
    test_db_session.commit()

    # Recupera o arquivo criado
    saved_arquivo = test_db_session.query(EntidadeArquivo).first()

    # Verificações
    assert saved_arquivo is not None
    assert saved_arquivo.id is not None
    assert saved_arquivo.nome_arquivo == "exemplo.txt"
    assert saved_arquivo.extensao_arquivo == "txt"
    assert saved_arquivo.tamanho_em_bytes == 1024
    assert saved_arquivo.is_excluido is False
    assert saved_arquivo.pasta_id == pasta.id


def test_repr_method(test_db_session):
    # Alterado para usar test_db_session
    """
    Testa o método __repr__ da entidade EntidadeArquivo.
    """
    # Cria uma pasta relacionada para a entidade EntidadeArquivo
    pasta = EntidadePasta(name="Documentos")
    test_db_session.add(pasta)
    test_db_session.commit()

    # Cria uma entidade EntidadeArquivo
    novo_arquivo = EntidadeArquivo(
        pasta_id=pasta.id,
        nome_arquivo="documento.pdf",
        extensao_arquivo="pdf",
        tamanho_em_bytes=2048,
    )
    test_db_session.add(novo_arquivo)
    test_db_session.commit()

    # Verifica a saída do método __repr__
    expected_repr = (
        f"EntidadeArquivo(id={novo_arquivo.id}, "
        f"nome_arquivo='documento.pdf', extensao_arquivo='pdf')"
    )
    assert repr(novo_arquivo) == expected_repr
