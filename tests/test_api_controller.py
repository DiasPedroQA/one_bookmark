import os
import logging
from typing import Generator
from dotenv import load_dotenv
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.interface.api_controller import APIController
from src.infrastructure.db_mysql.database import Base

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Construção da URL do banco de dados a partir das variáveis de ambiente
DB_DRIVER = os.getenv("DB_DRIVER", "mysql+pymysql")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "#R1040grau$")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "db_gerenciador_arquivos")

# URL de conexão com o banco de dados para SQLAlchemy
SQLALCHEMY_DATABASE_URL = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Caso queira usar SQLite em memória para testes, substitua a linha acima pela linha abaixo:
# SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    logger.info("Criando banco de dados na memória para os testes.")
    Base.metadata.create_all(bind=engine)
    db: Session = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        logger.info("Fechando sessão do banco de dados.")
    Base.metadata.drop_all(bind=engine)
    logger.info("Banco de dados destruído após os testes.")


def test_post_folder_path_absolute(db: Session) -> None:
    logger.info("Iniciando teste: test_post_folder_path_absolute")
    api_controller: APIController = APIController(db)
    response: dict = api_controller.post_folder_path("/home/user/Downloads")
    logger.info("Resposta recebida: %s", response)

    assert response["status"] == "success"
    assert response["path"] == "/home/user/Downloads"
    logger.info("Teste test_post_folder_path_absolute passou com sucesso.")


def test_post_folder_path_relative(db: Session) -> None:
    logger.info("Iniciando teste: test_post_folder_path_relative")
    api_controller: APIController = APIController(db)
    response: dict = api_controller.post_folder_path("Downloads")
    logger.info("Resposta recebida: %s", response)

    assert response["status"] == "success"
    assert response["path"] == "Downloads"
    logger.info("Teste test_post_folder_path_relative passou com sucesso.")
