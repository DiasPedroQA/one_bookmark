# Entidade que representa o caminho da pasta

from sqlalchemy import Column, Integer, String
from src.infrastructure.database import Base


class SQLTable_Pasta(Base):
    __tablename__ = "folders"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, unique=True, nullable=False)
