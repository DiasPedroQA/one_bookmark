from sqlalchemy.orm import Session
from src.use_cases.folder_service import FolderService


class APIController:
    def __init__(self, db: Session) -> None:
        self.db: Session = db

    def post_folder_path(self, path: str) -> dict:
        # Chama o serviço para criar o caminho da pasta
        folder_service: FolderService = FolderService()
        folder_service.create_folder_path(self.db, path=path)
        return {"status": "success", "path": path}
