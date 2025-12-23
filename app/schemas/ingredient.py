from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class IngredientBase(BaseModel):
    name: str
    type: str
    created_at: datetime

    class Config:
        from_attributes = True

class IngredientCreate(BaseModel):
    name: str
    type: str
    created_at: Optional[datetime] = None

class IngredientResponse(IngredientBase):
    id: int

    class Config:
        from_attributes = True

