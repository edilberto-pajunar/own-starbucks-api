from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class DrinkBase(BaseModel):
    name: str
    category: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    base_beverage: Optional[str] = None
    default_size: Optional[str] = None
    default_ice_level: Optional[str] = None
    default_sweetness_level: Optional[int] = None
    is_customizable: Optional[bool] = True

    class Config:
        from_attributes = True

class DrinkCreate(BaseModel):
    name: str
    category: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    base_beverage: Optional[str] = None
    default_size: Optional[str] = None
    default_ice_level: Optional[str] = None
    default_sweetness_level: Optional[int] = None
    is_customizable: Optional[bool] = True
    createdAt: Optional[datetime] = None

class DrinkResponse(DrinkBase):
    id: int
    createdAt: datetime

    class Config:
        from_attributes = True

class DrinkIngredientInfo(BaseModel):
    id: int
    name: str
    type: str
    quantity: int
    unit: str
    is_removable: bool

    class Config:
        from_attributes = True

class DrinkWithIngredients(DrinkResponse):
    ingredients: List[DrinkIngredientInfo] = []

    class Config:
        from_attributes = True

class DrinkSearch(BaseModel):
    query: str
