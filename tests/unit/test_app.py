# tests/unit/test_app.py

from app.api import create_app


def test_create_app():
    """Teste a criação da aplicação Flask."""
    app = create_app()
    assert app is not None, "A aplicação não foi criada."
    assert app.testing, "A aplicação não está em modo de teste."
