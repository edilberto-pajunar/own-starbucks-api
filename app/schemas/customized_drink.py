from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CustomizedDrinkBase(BaseModel):
    name: str
    base_drink_name: str
    base_drink_photo: str
    milk_type: str
    sugar_level: str
    cup_size: str
    extras: str
    total_price: float
    created_at: datetime
    image: str

    class Config:
        from_attributes = True

class CustomizedDrinkCreate(BaseModel):
    name: str
    base_drink_name: str
    base_drink_photo: str
    milk_type: str
    sugar_level: str
    cup_size: str
    extras: str
    total_price: float
    created_at: datetime
    image: Optional[str] = None

class CustomizedDrinkResponse(CustomizedDrinkBase):
    id: int

    class Config:
        from_attributes = True