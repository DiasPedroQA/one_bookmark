import pytest
from app.core.usecases.validador_caminho import validar_caminho
from unittest import mock


@pytest.fixture
def setup_temp_files(tmp_path):
    dir_path = tmp_path / "test_dir"
    dir_path.mkdir()
    file_path = dir_path / "test_file.txt"
    file_path.write_text("Este é um arquivo de teste.")
    return str(dir_path), str(file_path)


def test_validar_diretorio_valido(setup_temp_files):
    dir_path, _ = setup_temp_files
    with mock.patch("os.path.exists", return_value=True), mock.patch("os.path.isdir", return_value=True):
        existe, tipo = validar_caminho(dir_path)
        assert existe is True
        assert tipo == 'diretorio'


def test_validar_arquivo_valido(setup_temp_files):
    _, file_path = setup_temp_files
    with mock.patch("os.path.exists", return_value=True), mock.patch("os.path.isfile", return_value=True):
        existe, tipo = validar_caminho(file_path)
        assert existe is True
        assert tipo == 'arquivo'


def test_validar_caminho_invalido():
    caminho_invalido = "caminho/invalido.txt"
    with mock.patch("os.path.exists", return_value=False):
        existe, tipo = validar_caminho(caminho_invalido)
        assert existe is False
        assert tipo == 'invalido'


def test_validar_caminho_inexistente():
    caminho_inexistente = "caminho/inexistente.txt"
    with mock.patch("os.path.exists", return_value=False):
        existe, tipo = validar_caminho(caminho_inexistente)
        assert existe is False
        assert tipo == 'invalido'


# Testes para diferenciar por sistema operacional
def test_validar_caminho_windows(setup_temp_files):
    dir_path, _ = setup_temp_files
    with mock.patch("os.path.exists", return_value=True), mock.patch("os.path.isdir", return_value=True), mock.patch("platform.system", return_value="Windows"):
        existe, tipo = validar_caminho(dir_path)
        assert existe is True
        assert tipo == 'diretorio'


def test_validar_caminho_ubuntu(setup_temp_files):
    dir_path, _ = setup_temp_files
    with mock.patch("os.path.exists", return_value=True), mock.patch("os.path.isdir", return_value=True), mock.patch("platform.system", return_value="Linux"):
        existe, tipo = validar_caminho(dir_path)
        assert existe is True
        assert tipo == 'diretorio'


def test_validar_caminho_mac(setup_temp_files):
    dir_path, _ = setup_temp_files
    with mock.patch("os.path.exists", return_value=True), mock.patch("os.path.isdir", return_value=True), mock.patch("platform.system", return_value="Darwin"):
        existe, tipo = validar_caminho(dir_path)
        assert existe is True
        assert tipo == 'diretorio'
