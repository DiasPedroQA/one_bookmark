# src/infra/db/repositories/arquivo_repository_test.py
from datetime import datetime
from infra.db.entities.arquivo_entity import EntidadeArquivo
from src.infra.db.settings.connection import DBConnectionHandler
from .arquivo_repository_impl import ArquivoRepositorio


def test_inserir_arquivo():
    # Mock de dados para inserção
    mock_nome_arquivo = 'exemplo_documento'
    mock_extensao_arquivo = 'html'  # O ENUM definido aceita apenas o valor
    mock_tamanho_em_bytes = 2048
    mock_is_excluido = False
    mock_data_criacao = datetime.now()
    mock_data_atualizacao = datetime.now()

    # Instância do repositório a ser testado
    repositorio_arquivos = ArquivoRepositorio()

    # Conexão para garantir que o teste se execute de forma independente
    with DBConnectionHandler() as database:
        try:
            # Inserir novo registro de arquivo usando o repositório
            repositorio_arquivos.inserir_arquivo(
                None, mock_nome_arquivo, mock_extensao_arquivo,
                mock_tamanho_em_bytes, mock_is_excluido,
                mock_data_criacao, mock_data_atualizacao
            )

            # Recuperar o arquivo inserido para validar a inserção
            arquivo_inserido = database.session.query(
                EntidadeArquivo
            ).filter_by(
                nome_arquivo=mock_nome_arquivo,
                extensao_arquivo=mock_extensao_arquivo,
                tamanho_arquivo_bytes=mock_tamanho_em_bytes
            ).first()

            # Assertivas para verificar se o arquivo foi inserido corretamente
            assert arquivo_inserido is not None, \
                "Erro: O arquivo não foi encontrado no banco de dados."
            assert arquivo_inserido.nome_arquivo == mock_nome_arquivo, \
                f"Erro: Nome esperado '{mock_nome_arquivo}', " \
                f"mas encontrei: '{arquivo_inserido.nome_arquivo}'"
            assert arquivo_inserido.extensao_arquivo == mock_extensao_arquivo, \
                f"Erro: Extensão esperada '{mock_extensao_arquivo}', " \
                f"mas encontrei: '{arquivo_inserido.extensao_arquivo}'"  # noqa: E501
            assert arquivo_inserido.tamanho_arquivo_bytes == \
                mock_tamanho_em_bytes, \
                f"Erro: Tamanho esperado '{mock_tamanho_em_bytes}', " \
                f"mas encontrei: '{arquivo_inserido.tamanho_arquivo_bytes}'"
            assert arquivo_inserido.is_excluido == mock_is_excluido, \
                f"Erro: Status esperado '{mock_is_excluido}', " \
                f"mas encontrei: '{arquivo_inserido.is_excluido}'"

        finally:
            # Limpar dados de teste para garantir que não haja interferência
            database.session.query(EntidadeArquivo).filter_by(
                nome_arquivo=mock_nome_arquivo,
                extensao_arquivo=mock_extensao_arquivo
            ).delete()
            database.session.commit()
