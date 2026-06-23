from pathlib import Path
from datetime import datetime
from fastapi import UploadFile
import shutil

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"

ALLOWED_EXTENTIONS = {".pdf", ".docx", ".txt", ".md", ".csv", ".json", ".html"}


class FileStorageService:
    def __init__(self):
        self.upload_dir = DATA_DIR
        self.upload_dir.mkdir(exist_ok=True)

    def save_file(self, file: UploadFile) -> Path:
        self.validate_file(file)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        filename = f"{timestamp}_{file.filename}"
        save_path = self.upload_dir / filename

        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return save_path

    def get_file(self, filename: str) -> Path:
        file_path = self.upload_dir / filename

        if not file_path.exists():
            raise FileNotFoundError(f"{filename} 파일이 존재하지 않습니다.")

        return file_path

    def list_files(self) -> list[str]:
        return [file.name for file in self.upload_dir.iterdir() if file.is_file()]

    def delete_file(self, filename: str) -> bool:
        file_path = self.upload_dir / filename

        if not file_path.exists():
            return False

        file_path.unlink()
        return True

    def validate_file(self, file: UploadFile):
        ext = Path(file.filename).suffix.lower()

        if ext not in ALLOWED_EXTENTIONS:
            raise ValueError(f"지원하지 않는 파일 형식입니다: {ext}")
