# src/infra/db/repositories/arquivo_repository_test.py

from datetime import datetime
import pytest
from src.infra.db.entities.arquivo_entity import EntidadeArquivo
from src.infra.db.settings.connection import DBConnectionHandler
from .arquivo_repository_impl import ArquivoRepositorio


@pytest.fixture
def arquivo_data():
    """
    Fixture que fornece dados mockados para a entidade 'EntidadeArquivo'.
    """
    return {
        'nome_arquivo': 'exemplo_documento',
        'extensao_arquivo': 'html',
        'tamanho_em_bytes': 2048,
        'is_excluido': False,
        'data_criacao': datetime.now(),
        'data_atualizacao': datetime.now(),
    }


@pytest.fixture
def db_session():
    """
    Fixture que fornece uma sessão de banco de dados para os testes.
    """
    db_handler = DBConnectionHandler()
    with db_handler as session:
        yield session  # Fornece a sessão para os testes
        # Limpa a tabela após o teste
        session.execute_query(EntidadeArquivo)
        session.commit()


def test_inserir_arquivo(db_session, arquivo_data):
    """
    Testa a inserção de um novo arquivo no repositório.

    Parâmetros:
        db_session: Sessão de banco de dados.
        arquivo_data (dict): Dados mockados para a entidade 'EntidadeArquivo'.
    """
    # Instância do repositório a ser testado
    repositorio_arquivos = ArquivoRepositorio()

    # Inserir novo registro de arquivo usando o repositório
    repositorio_arquivos.inserir_arquivo(
        1,  # Certifique-se de que esse id_pasta é válido
        arquivo_data['nome_arquivo'],
        arquivo_data['extensao_arquivo'],
        arquivo_data['tamanho_arquivo_bytes'],  # Corrigido o nome da chave
        arquivo_data['is_excluido'],
        arquivo_data['data_criacao'],
        arquivo_data['data_atualizacao']
    )

    # Recuperar o arquivo inserido para validar a inserção
    arquivo_inserido = db_session.query(
        EntidadeArquivo
    ).filter_by(
        nome_arquivo=arquivo_data['nome_arquivo'],
        extensao_arquivo=arquivo_data['extensao_arquivo'],
        tamanho_arquivo_bytes=arquivo_data['tamanho_arquivo_bytes']
    ).first()

    # Assertivas para verificar se o arquivo foi inserido corretamente
    assert arquivo_inserido is not None, \
        "Erro: O arquivo não foi encontrado no banco de dados."

    assert arquivo_inserido.nome_arquivo == arquivo_data['nome_arquivo'], \
        f"Erro: Nome esperado '{arquivo_data['nome_arquivo']}', " \
        f"mas encontrei: '{arquivo_inserido.nome_arquivo}'"

    assert arquivo_inserido.extensao_arquivo == arquivo_data['extensao_arquivo'], \
        f"Erro: Extensão esperada '{arquivo_data['extensao_arquivo']}', " \
        f"mas encontrei: '{arquivo_inserido.extensao_arquivo}'"  # noqa: E501

    assert arquivo_inserido.tamanho_arquivo_bytes == arquivo_data['tamanho_arquivo_bytes'], \
        f"Erro: Tamanho esperado '{arquivo_data['tamanho_arquivo_bytes']}', " \
        f"mas encontrei: '{arquivo_inserido.tamanho_arquivo_bytes}'"  # noqa: E501

    assert arquivo_inserido.is_excluido == arquivo_data['is_excluido'], \
        f"Erro: Status esperado '{arquivo_data['is_excluido']}', " \
        f"mas encontrei: '{arquivo_inserido.is_excluido}'"
