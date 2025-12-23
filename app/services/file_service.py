from pathlib import Path
import shutil
import uuid

from fastapi import HTTPException, UploadFile


class FileService:
    def __init__(self, upload_dir: str = "uploads/drink"):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.allowed_types = ["image/jpeg", "image/png", "image/jpg", "image/webp"]

    async def save_image(self, file: UploadFile) -> str:
        """ Save uploaded image and return the URL path"""
        if file.content_type not in self.allowed_types:
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Only JPEG, PNG and WebP images allowed."
            )
        
        # Generate unique filename
        file_extension = file.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = self.upload_dir / unique_filename

        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return f"/uploads/drinks/{unique_filename}"