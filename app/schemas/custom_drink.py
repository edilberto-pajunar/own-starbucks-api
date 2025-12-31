from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

from app.schemas.drink import DrinkResponse


class CustomDrinkIngredientInfo(BaseModel):
    id: int
    name: str
    type: str
    quantity: int
    unit: str
    is_added: bool

    class Config:
        from_attributes = True

class CustomDrinkBase(BaseModel):
    name: str
    base_drink: DrinkResponse
    milk_type: Optional[str] = None
    sugar_level: Optional[str] = None
    cup_size: Optional[str] = None
    total_price: float

    class Config:
        from_attributes = True

class CustomDrinkCreate(BaseModel):
    name: str
    base_drink_id: int
    user_id: Optional[int] = None
    milk_type: Optional[str] = None
    sugar_level: Optional[str] = None
    cup_size: Optional[str] = None
    total_price: float
    image: Optional[str] = None
    created_at: Optional[datetime] = None

class CustomDrinkResponse(CustomDrinkBase):
    id: int
    user_id: Optional[int] = None
    image: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class CustomDrinkWithIngredients(CustomDrinkResponse):
    ingredients: List[CustomDrinkIngredientInfo] = []

    class Config:
        from_attributes = True

