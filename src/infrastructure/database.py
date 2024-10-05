# Configuração do banco de dados com SQLAlchemy

import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criação da engine do SQLAlchemy (substitua a URL pelo seu banco de dados)
DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

if not DATABASE_URL:
    logger.error("A URL do banco de dados não foi encontrada. Verifique suas variáveis de ambiente.")
    raise ValueError("A URL do banco de dados não pode ser vazia.")

engine = create_engine(DATABASE_URL, echo=True)

# Criando a sessão para interagir com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para criação dos modelos
Base = declarative_base()


# Dependência para obter uma sessão de banco de dados
def get_db():
    db = SessionLocal()
    try:
        logger.info("Sessão de banco de dados criada.")
        yield db
    finally:
        db.close()
        logger.info("Sessão de banco de dados fechada.")
