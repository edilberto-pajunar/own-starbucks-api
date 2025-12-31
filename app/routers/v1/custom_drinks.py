from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session, joinedload

from app.config import get_db
from app.models.api import ApiResponse
from app.models.custom_drink import CustomDrink
from app.models.custom_drink_ingredient import CustomDrinkIngredient
from app.models.drink import Drink
from app.schemas.custom_drink import CustomDrinkResponse, CustomDrinkWithIngredients
from app.schemas.drink import DrinkResponse
from app.services.file_service import FileService

router = APIRouter(
    prefix="/api/v1/custom-drinks",
)

@router.get("/", response_model=ApiResponse[List[CustomDrinkResponse]])
async def get_all_custom_drinks(db: Session = Depends(get_db)):
    """Get all custom drinks"""
    custom_drinks = db.query(CustomDrink).all()
    if not custom_drinks:
        raise HTTPException(status_code=404, detail="No custom drinks found")
        
    return ApiResponse(
        message="Custom drinks fetched successfully",
        data=custom_drinks
    )

@router.get("/with-ingredients", response_model=ApiResponse[List[CustomDrinkWithIngredients]])
async def get_custom_drinks_with_ingredients(db: Session = Depends(get_db)):
    """Get all custom drinks with their ingredients"""
    custom_drinks = db.query(CustomDrink).options(joinedload(CustomDrink.ingredients)).all()
    if not custom_drinks:
        raise HTTPException(status_code=404, detail="No custom drinks found")
    
    drinks_with_ingredients = []
    for drink in custom_drinks:
        base_drink = db.query(Drink).filter(Drink.id == drink.base_drink_id).first()
        if not base_drink:
            continue
    
        base_drink_response = DrinkResponse.model_validate(base_drink)

        drink_dict = {
            "id": drink.id,
            "name": drink.name,
            "base_drink": base_drink_response,
            "user_id": drink.user_id,
            "milk_type": drink.milk_type,
            "sugar_level": drink.sugar_level,
            "cup_size": drink.cup_size,
            "total_price": drink.total_price,
            "image": drink.image,
            "created_at": drink.created_at,
            "ingredients": [
                {
                    "id": ci.ingredient.id,
                    "name": ci.ingredient.name,
                    "type": ci.ingredient.type,
                    "quantity": ci.quantity,
                    "unit": ci.unit,
                    "is_added": ci.is_added
                }
                for ci in drink.ingredients
            ]
        }
        drinks_with_ingredients.append(drink_dict)

    return ApiResponse(
        message="Custom drinks with ingredients fetched successfully",
        data=drinks_with_ingredients
    )

@router.get("/{custom_drink_id}", response_model=ApiResponse[CustomDrinkWithIngredients])
async def get_custom_drink_by_id(custom_drink_id: int, db: Session = Depends(get_db)):
    """Get a specific custom drink with ingredients"""
    drink = db.query(CustomDrink).options(joinedload(CustomDrink.ingredients)).filter(CustomDrink.id == custom_drink_id).first()
    if not drink:
        raise HTTPException(status_code=404, detail="Custom drink not found")
    
    drink_dict = {
        "id": drink.id,
        "name": drink.name,
        "base_drink_id": drink.base_drink_id,
        "user_id": drink.user_id,
        "milk_type": drink.milk_type,
        "sugar_level": drink.sugar_level,
        "cup_size": drink.cup_size,
        "total_price": drink.total_price,
        "image": drink.image,
        "created_at": drink.created_at,
        "ingredients": [
            {
                "id": ci.ingredient.id,
                "name": ci.ingredient.name,
                "type": ci.ingredient.type,
                "quantity": ci.quantity,
                "unit": ci.unit,
                "is_added": ci.is_added
            }
            for ci in drink.ingredients
        ]
    }
    
    return ApiResponse(
        message="Custom drink fetched successfully",
        data=drink_dict
    )

@router.post("/", response_model=ApiResponse[CustomDrinkResponse])
async def create_custom_drink(
        name: str = Form(...),
        base_drink_id: int = Form(...),
        milk_type: str = Form(None),
        sugar_level: str = Form(None),
        cup_size: str = Form(None),
        total_price: float = Form(...),
        user_id: Optional[int] = Form(None),
        image: Optional[UploadFile] = File(None),
        db: Session = Depends(get_db),
    ):
    """Create a new custom drink with optional image upload"""
    
    image_url = None
    if image:
        file_service = FileService()
        image_url = await file_service.save_image(image)
    
    new_drink = CustomDrink(
        name=name,
        base_drink_id=base_drink_id,
        user_id=user_id,
        milk_type=milk_type,
        sugar_level=sugar_level,
        cup_size=cup_size,
        total_price=total_price,
        image=image_url,
        created_at=datetime.now()
    )
    
    db.add(new_drink)
    db.commit()
    db.refresh(new_drink)

    return ApiResponse(
        message="Custom drink created successfully",
        data=new_drink
    )

@router.post("/{custom_drink_id}/ingredients", response_model=ApiResponse[CustomDrinkWithIngredients])
async def add_ingredient_to_custom_drink(
        custom_drink_id: int,
        ingredient_id: int = Form(...),
        quantity: int = Form(...),
        unit: str = Form(...),
        is_added: bool = Form(False),
        db: Session = Depends(get_db)
    ):
    """Add or modify an ingredient for a custom drink"""
    
    drink = db.query(CustomDrink).filter(CustomDrink.id == custom_drink_id).first()
    if not drink:
        raise HTTPException(status_code=404, detail="Custom drink not found")
    
    new_ingredient = CustomDrinkIngredient(
        custom_drink_id=custom_drink_id,
        ingredient_id=ingredient_id,
        quantity=quantity,
        unit=unit,
        is_added=is_added
    )
    
    db.add(new_ingredient)
    db.commit()
    
    drink = db.query(CustomDrink).options(joinedload(CustomDrink.ingredients)).filter(CustomDrink.id == custom_drink_id).first()
    
    drink_dict = {
        "id": drink.id,
        "name": drink.name,
        "base_drink_id": drink.base_drink_id,
        "user_id": drink.user_id,
        "milk_type": drink.milk_type,
        "sugar_level": drink.sugar_level,
        "cup_size": drink.cup_size,
        "total_price": drink.total_price,
        "image": drink.image,
        "created_at": drink.created_at,
        "ingredients": [
            {
                "id": ci.ingredient.id,
                "name": ci.ingredient.name,
                "type": ci.ingredient.type,
                "quantity": ci.quantity,
                "unit": ci.unit,
                "is_added": ci.is_added
            }
            for ci in drink.ingredients
        ]
    }
    
    return ApiResponse(
        message="Ingredient added to custom drink successfully",
        data=drink_dict
    )

@router.put("/{custom_drink_id}", response_model=ApiResponse[CustomDrinkResponse])
async def update_custom_drink(
        custom_drink_id: int,
        name: Optional[str] = Form(None),
        milk_type: Optional[str] = Form(None),
        sugar_level: Optional[str] = Form(None),
        cup_size: Optional[str] = Form(None),
        total_price: Optional[float] = Form(None),
        image: Optional[UploadFile] = File(None),
        db: Session = Depends(get_db)
    ):
    """Update a custom drink"""
    
    drink = db.query(CustomDrink).filter(CustomDrink.id == custom_drink_id).first()
    if not drink:
        raise HTTPException(status_code=404, detail="Custom drink not found")
    
    if name:
        drink.name = name
    if milk_type:
        drink.milk_type = milk_type
    if sugar_level:
        drink.sugar_level = sugar_level
    if cup_size:
        drink.cup_size = cup_size
    if total_price:
        drink.total_price = total_price
    if image:
        file_service = FileService()
        image_url = await file_service.save_image(image)
        drink.image = image_url
    
    db.commit()
    db.refresh(drink)
    
    return ApiResponse(
        message="Custom drink updated successfully",
        data=drink
    )

@router.delete("/{custom_drink_id}")
async def delete_custom_drink(custom_drink_id: int, db: Session = Depends(get_db)):
    """Delete a custom drink"""
    
    drink = db.query(CustomDrink).filter(CustomDrink.id == custom_drink_id).first()
    if not drink:
        raise HTTPException(status_code=404, detail="Custom drink not found")
    
    db.query(CustomDrinkIngredient).filter(CustomDrinkIngredient.custom_drink_id == custom_drink_id).delete()
    db.delete(drink)
    db.commit()
    
    return ApiResponse(
        message="Custom drink deleted successfully",
        data={"id": custom_drink_id}
    )

@router.delete("/{custom_drink_id}/ingredients/{ingredient_id}")
async def remove_ingredient_from_custom_drink(
        custom_drink_id: int,
        ingredient_id: int,
        db: Session = Depends(get_db)
    ):
    """Remove an ingredient from a custom drink"""
    
    custom_ingredient = db.query(CustomDrinkIngredient).filter(
        CustomDrinkIngredient.custom_drink_id == custom_drink_id,
        CustomDrinkIngredient.id == ingredient_id
    ).first()
    
    if not custom_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found in this custom drink")
    
    db.delete(custom_ingredient)
    db.commit()
    
    return ApiResponse(
        message="Ingredient removed from custom drink successfully",
        data={"custom_drink_id": custom_drink_id, "ingredient_id": ingredient_id}
    )

