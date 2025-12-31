from app.config import Base
from sqlalchemy import Column, ForeignKey, Integer, Float, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class CustomDrink(Base):
    __tablename__ = "custom_drinks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    base_drink_id = Column(Integer, ForeignKey("drinks.id"))
    name = Column(String, nullable=False)
    image = Column(String)
    milk_type = Column(String)
    sugar_level = Column(String)
    cup_size = Column(String)
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

    base_drink = relationship("Drink")
    user = relationship("User")
    ingredients = relationship("CustomDrinkIngredient", back_populates="custom_drink")
