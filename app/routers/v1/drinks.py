from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session, joinedload

from app.config import get_db
from app.models.api import ApiResponse
from app.models.drink import Drink
from app.schemas.drink import DrinkResponse, DrinkSearch, DrinkWithIngredients
from app.services.file_service import FileService

router = APIRouter(
    prefix="/api/v1/drinks",
)

@router.get("/", response_model=ApiResponse[List[DrinkResponse]])
async def read_drinks(db: Session = Depends(get_db)):
    drinks = db.query(Drink).all()
    if not drinks:
        raise HTTPException(status_code=404, detail="No drinks found")

    return ApiResponse(
        message="Drinks fetched successfully",
        data=drinks
    )

@router.get("/with-ingredients", response_model=ApiResponse[List[DrinkWithIngredients]])
async def read_drinks_with_ingredients(db: Session = Depends(get_db)):
    drinks = db.query(Drink).options(joinedload(Drink.ingredients)).all()
    if not drinks:
        raise HTTPException(status_code=404, detail="No drinks found")
    
    drinks_with_ingredients = []
    for drink in drinks:
        drink_dict = {
            "id": drink.id,
            "name": drink.name,
            "category": drink.category,
            "description": drink.description,
            "image_url": drink.image_url,
            "base_beverage": drink.base_beverage,
            "default_size": drink.default_size,
            "default_ice_level": drink.default_ice_level,
            "default_sweetness_level": drink.default_sweetness_level,
            "is_customizable": drink.is_customizable,
            "createdAt": drink.createdAt,
            "ingredients": [
                {
                    "id": di.ingredient.id,
                    "name": di.ingredient.name,
                    "type": di.ingredient.type,
                    "quantity": di.quantity,
                    "unit": di.unit,
                    "is_removable": di.is_removable
                }
                for di in drink.ingredients
            ]
        }
        drinks_with_ingredients.append(drink_dict)

    return ApiResponse(
        message="Drinks with ingredients fetched successfully",
        data=drinks_with_ingredients
    )

@router.get("/{drink_id}", response_model=ApiResponse[DrinkWithIngredients])
async def get_drink_by_id(drink_id: int, db: Session = Depends(get_db)):
    drink = db.query(Drink).options(joinedload(Drink.ingredients)).filter(Drink.id == drink_id).first()
    if not drink:
        raise HTTPException(status_code=404, detail="Drink not found")
    
    drink_dict = {
        "id": drink.id,
        "name": drink.name,
        "category": drink.category,
        "description": drink.description,
        "image_url": drink.image_url,
        "base_beverage": drink.base_beverage,
        "default_size": drink.default_size,
        "default_ice_level": drink.default_ice_level,
        "default_sweetness_level": drink.default_sweetness_level,
        "is_customizable": drink.is_customizable,
        "createdAt": drink.createdAt,
        "ingredients": [
            {
                "id": di.ingredient.id,
                "name": di.ingredient.name,
                "type": di.ingredient.type,
                "quantity": di.quantity,
                "unit": di.unit,
                "is_removable": di.is_removable
            }
            for di in drink.ingredients
        ]
    }
    
    return ApiResponse(
        message="Drink fetched successfully",
        data=drink_dict
    )

@router.post("/", response_model=ApiResponse[DrinkResponse])
async def create_drink(
    name: str = Form(...),
    category: str = Form(...),
    description: str = Form(...),
    base_beverage: str = Form(...),
    default_size: str = Form(...),
    is_customizable: Optional[bool] = Form(True),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)):

    image_url = None
    if image:
        file_service = FileService()
        image_url = await file_service.save_image(image)

    new_drink = Drink(
        name=name,
        category=category,
        description=description,
        base_beverage=base_beverage,
        default_size=default_size,
        is_customizable=is_customizable,
        image_url=image_url,
        createdAt=datetime.now(),
    )

    db.add(new_drink)
    db.commit()
    db.refresh(new_drink)
    return ApiResponse(
        message="A new drink created successfully",
        data=new_drink
    )

@router.post("/search", response_model=ApiResponse[List[DrinkResponse]])
async def search_drinks(search: DrinkSearch, db: Session = Depends(get_db)):
    drinks = db.query(Drink).filter(Drink.name.ilike(f"%{search.query}%")).all()
  
    return ApiResponse(
        message="Drinks fetched successfully",
        data= drinks if drinks else []
    )

@router.post("/{drink_id}", response_model=ApiResponse[DrinkResponse])
async def get_drink(drink_id: int, db: Session = Depends(get_db)):
    drink = db.query(Drink).filter(Drink.id == drink_id).first()
    if drink is None:
        raise HTTPException(status_code=404, detail="Drink not found")
    return ApiResponse(
        message="Drink fetched successfully",
        data=drink
    )
