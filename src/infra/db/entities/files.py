from sqlalchemy.sql import func
from sqlalchemy import (
    Boolean, Integer, Enum, String, Text,
    Column, ForeignKey, TIMESTAMP
)
from sqlalchemy.orm import relationship
from src.infra.db.settings.base import Base


class Folder(Base):
    """
    Representação da tabela 'folders'.
    """
    __tablename__ = "folders"

    id = Column(
        Integer, primary_key=True, autoincrement=True)
    folder_name = Column(
        String(255), nullable=False)
    parent_folder_id = Column(
        Integer, ForeignKey("folders.id"), nullable=True)
    is_deleted = Column(
        Boolean, default=False)
    created_at = Column(
        TIMESTAMP, server_default=func.now())
    updated_at = Column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relacionamento para subpastas
    subfolders = relationship("Folder", remote_side=[id])

    def __repr__(self) -> str:
        return f"Folder(id={self.id}, folder_name='{self.folder_name}')"


class File(Base):
    """
    Representação da tabela 'files'.
    """
    __tablename__ = "files"

    id = Column(
        Integer, primary_key=True,
        autoincrement=True)
    folder_id = Column(
        Integer, ForeignKey("folders.id", ondelete="CASCADE"),
        nullable=False)
    filename = Column(
        String(255),
        nullable=False)
    file_extension = Column(
        Enum('txt', 'docx', 'pdf', 'html', 'csv', name='file_extension_enum'),
        nullable=False)
    size_in_bytes = Column(
        Integer, nullable=False,
        default=0)
    is_deleted = Column(
        Boolean, default=False)
    created_at = Column(
        TIMESTAMP, server_default=func.now())
    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now())

    # Relacionamento com a tabela Folder
    folder = relationship("Folder")

    def __repr__(self) -> str:
        return (
            f"File(id={self.id}, filename='{self.filename}', "
            f"file_extension='{self.file_extension}')"
        )


class FileMetadata(Base):
    """
    Representação da tabela 'file_metadata'.
    """
    __tablename__ = "file_metadata"

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(
        Integer, ForeignKey("files.id", ondelete="CASCADE"),
        nullable=False)
    author = Column(
        String(255), default="Desconhecido")
    last_modified = Column(
        TIMESTAMP, server_default=func.now(),
        onupdate=func.now())
    created_by = Column(
        String(255), default="Sistema")

    # Relacionamento com a tabela File
    file = relationship("File")

    def __repr__(self) -> str:
        return (
            f"FileMetadata(id={self.id}, author='{self.author}', "
            f"created_by='{self.created_by}')"
        )


class FileLog(Base):
    """
    Representação da tabela 'file_logs'.
    """
    __tablename__ = "file_logs"

    id = Column(
        Integer, primary_key=True,
        autoincrement=True)
    file_id = Column(
        Integer, ForeignKey("files.id", ondelete="CASCADE"),
        nullable=False)
    action = Column(Enum(
        'created', 'updated', 'deleted',
        'restored', name='file_action_enum'),
        nullable=False)
    log_timestamp = Column(
        TIMESTAMP,
        server_default=func.now())
    description = Column(
        Text,
        nullable=True)

    # Relacionamento com a tabela File
    file = relationship("File")

    def __repr__(self) -> str:
        return (
            f"FileLog(id={self.id}, action='{self.action}', "
            f"log_timestamp={self.log_timestamp})"
        )
