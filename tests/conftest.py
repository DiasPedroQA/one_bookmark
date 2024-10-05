# Configuração do pytest para testes com banco de dados

import os
from dotenv import load_dotenv
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infrastructure.database import Base

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Banco de dados de teste usando as variáveis de ambiente ou SQLite em memória
DB_DRIVER = os.getenv("DB_DRIVER", "mysql+pymysql")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "#R1040grau$")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "db_gerenciador_arquivos")

# URL de conexão com o banco de dados para SQLAlchemy
SQLALCHEMY_DATABASE_URL = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Debug: Verificar a URL do banco de dados
print("SQLALCHEMY_DATABASE_URL:", SQLALCHEMY_DATABASE_URL)

# Verifique se a URL não está vazia
if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("A URL do banco de dados não pode ser vazia.")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Configura o banco de dados de teste antes de rodar os testes
@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
