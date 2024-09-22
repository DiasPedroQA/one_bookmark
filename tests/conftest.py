# tests/conftest.py

import pytest
from app.api import create_app


@pytest.fixture
def client():
    """Fixture para criar um cliente de teste da aplicação Flask."""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
