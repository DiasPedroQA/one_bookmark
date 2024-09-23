import os
import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client


def test_criar_arquivo(client):
    response = client.post('/api/v1/arquivos', json={
        'caminho': 'teste_api_arquivo.txt',
        'conteudo': 'Conteúdo para a API.'
    })
    assert response.status_code == 201
    assert b'Arquivo criado com sucesso.' in response.data
    os.remove('teste_api_arquivo.txt')


def test_criar_diretorio(client):
    response = client.post('/api/v1/diretorios', json={
        'caminho': 'teste_api_diretorio'
    })
    assert response.status_code == 201
    assert b'Diretorio criado com sucesso.' in response.data
    os.rmdir('teste_api_diretorio')
