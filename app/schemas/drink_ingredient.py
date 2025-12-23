from pydantic import BaseModel
from typing import Optional


class DrinkIngredientBase(BaseModel):
    drink_id: int
    ingredient_id: int
    quantity: int
    unit: str
    is_removable: Optional[bool] = True

    class Config:
        from_attributes = True

class DrinkIngredientCreate(DrinkIngredientBase):
    pass

class DrinkIngredientResponse(DrinkIngredientBase):
    id: int

    class Config:
        from_attributes = True

