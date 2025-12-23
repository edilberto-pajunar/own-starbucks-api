from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.config import get_db
from app.models.api import ApiResponse
from app.models.customized_drink import CustomizedDrink
from app.schemas.customized_drink import CustomizedDrinkCreate, CustomizedDrinkResponse
from app.services.customized_drink_service import CustomizedDrinkService

router = APIRouter(
    prefix="/api/v1/customized-drinks",
)

@router.get("/", response_model=ApiResponse[List[CustomizedDrinkResponse]])
async def read_customized_drinks(db: Session = Depends(get_db)):
    customized_drinks = db.query(CustomizedDrink).all()
    if not customized_drinks:
        raise HTTPException(status_code=404, detail="No customized drinks found")
        
    return ApiResponse(
        message="Customized drinks fetched successfully",
        data=customized_drinks
    )

@router.post("/", response_model=ApiResponse[CustomizedDrinkResponse])
async def create_customized_drink(
        name: str = Form(...),
        base_drink_name: str = Form(...),
        base_drink_photo: str = Form(...),
        milk_type: str = Form(...),
        sugar_level: str = Form(...),
        cup_size: str = Form(...),
        extras: str = Form(...),
        price: float = Form(...),
        image: UploadFile = File(...),
        db: Session = Depends(get_db),
    ):

    """ Create a customized drink with image upload"""
    service = CustomizedDrinkService(db)

    # Create Pydantic model from form data
    drink_data = CustomizedDrinkCreate(
        name=name,
        base_drink_name=base_drink_name,
        base_drink_photo=base_drink_photo,
        milk_type=milk_type,
        sugar_level=sugar_level,
        cup_size=cup_size,
        extras=extras,
        total_price=price,
        created_at=datetime.now(),
    )

    new_drink = await service.create_drink_with_image(drink_data, image)

    return ApiResponse(
        message="A new customized drink created successfully",
        data=new_drink
    )

@router.put("/{customized_drink_id}", response_model=ApiResponse[CustomizedDrinkResponse])
async def update_customized_drink(customized_drink_id: int, customized_drink: CustomizedDrinkCreate, db: Session = Depends(get_db)):
    db_customized_drink = db.query(CustomizedDrink).filter(CustomizedDrink.id == customized_drink_id).first()
    if not db_customized_drink:
        raise HTTPException(status_code=404, detail="Customized drink does not exist!")
    
    for field, value in customized_drink.model_dump().items():
        setattr(db_customized_drink, field, value)
    
    db.commit()
    db.refresh(db_customized_drink)
    return ApiResponse(
        message="Customized drink updated successfully",
        data=db_customized_drink
    )