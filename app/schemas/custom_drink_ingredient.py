from pydantic import BaseModel
from typing import Optional


class CustomDrinkIngredientBase(BaseModel):
    custom_drink_id: int
    ingredient_id: int
    quantity: int
    unit: str
    is_added: Optional[bool] = False

    class Config:
        from_attributes = True

class CustomDrinkIngredientCreate(CustomDrinkIngredientBase):
    pass

class CustomDrinkIngredientResponse(CustomDrinkIngredientBase):
    id: int

    class Config:
        from_attributes = True

