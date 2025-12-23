from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import get_db
from app.models.api import ApiResponse
from app.models.drink import Drink
from app.schemas.drink import DrinkCreate, DrinkResponse, DrinkSearch

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

@router.post("/", response_model=ApiResponse[DrinkResponse])
async def create_drink(drink: DrinkCreate, db: Session = Depends(get_db)):
    new_drink = Drink(**drink.model_dump())
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
