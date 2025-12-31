from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config import get_db
from app.models.api import ApiResponse
from app.models.drink import Drink
from app.models.favorite import Favorite
from app.schemas.drink import DrinkResponse
from app.schemas.favorite import FavoriteRequest, FavoriteResponse


router = APIRouter(
    prefix="/api/v1/favorites",
)

@router.get("/", response_model=ApiResponse[List[FavoriteResponse]])
async def get_all_favorites(db: Session = Depends(get_db)):
    favorites = db.query(Favorite).all()

    favorite_drinks = []
    for favorite in favorites:
        favorite_drink = db.query(Drink).filter(Drink.id == favorite.drink_id).first()
        if not favorite_drink:
            continue

        favorite_drink = {
            "id": favorite.id,
            "drink": DrinkResponse.model_validate(favorite_drink),
            "device_id": favorite.device_id,
            "is_custom": favorite.is_custom,
            "created_at": favorite.created_at
        }
        favorite_drinks.append(favorite_drink)

    return ApiResponse(
        message="Favorites fetched successfully",
        data=favorite_drinks
    )

@router.post("/", response_model=ApiResponse[FavoriteResponse])
async def add_favorite(favorite: FavoriteRequest, db: Session = Depends(get_db)):
    new_favorite = Favorite(
        device_id= favorite.device_id,
        drink_id= favorite.drink_id,
        is_custom= favorite.is_custom,
    )
    db.add(new_favorite)
    db.commit()
    db.refresh(new_favorite)
    return ApiResponse(
        message="Favorite added successfully",
        data=new_favorite
    )