# src/infra/db/settings/base.py

from sqlalchemy.orm import declarative_base

# Criação da base declarativa para as entidades do SQLAlchemy.
Base = declarative_base()
