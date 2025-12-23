from sqlalchemy.orm import relationship
from app.config import Base
from sqlalchemy import Column, Integer, String, DateTime

class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(String) # milk | syrup | topping \ base | shot
    created_at = Column(DateTime)

    drinks = relationship("DrinkIngredient", back_populates="ingredient")

