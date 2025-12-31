from datetime import datetime
from pydantic import BaseModel


class FavoriteBase(BaseModel):
    device_id: str
    drink_id: int
    is_custom: bool

    class Config:
        from_attributes = True

class FavoriteRequest(FavoriteBase):
    pass

class FavoriteResponse(FavoriteBase):
    created_at: datetime

    class Config:
        from_attributes = True