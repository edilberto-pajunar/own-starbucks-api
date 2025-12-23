from app.models.customized_drink import CustomizedDrink
from app.schemas.customized_drink import CustomizedDrinkCreate
from app.services.file_service import FileService
from fastapi import Depends, UploadFile
from app.config import get_db
from sqlalchemy.orm import Session


class CustomizedDrinkService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.file_service = FileService()

    async def create_drink_with_image(self, drink_data: CustomizedDrinkCreate, image_file: UploadFile):
        """ Create a new customized drink with image upload"""
        # Upload image first
        image_url = await self.file_service.save_image(image_file)

        # Create drink with image URL
        drink_dict = drink_data.model_dump()
        drink_dict["image"] = image_url

        new_drink = CustomizedDrink(**drink_dict)
        self.db.add(new_drink)
        self.db.commit()
        self.db.refresh(new_drink)

        return new_drink

    def get_all_drinks(self):
        """ Get all customized drinks"""
        return self.db.query(CustomizedDrink).all()