from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
import datetime

from app.config import Base

class Drink(Base):
    __tablename__ = "drinks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String)
    image_url = Column(String)
    base_beverage = Column(String)
    default_size = Column(String)
    default_ice_level = Column(String)
    default_sweetness_level = Column(Integer)
    is_customizable = Column(Boolean, default=True)
    createdAt = Column(DateTime, nullable=False, default=datetime.timezone.utc)

    ingredients = relationship("DrinkIngredient", back_populates="drink")
    favorites = relationship("Favorite", back_populates="drink")