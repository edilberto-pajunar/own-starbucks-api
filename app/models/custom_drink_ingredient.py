from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.config import Base


class CustomDrinkIngredient(Base):
    __tablename__ = "custom_drink_ingredients"

    id = Column(Integer, primary_key=True)
    custom_drink_id = Column(Integer, ForeignKey("custom_drinks.id"))
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"))
    quantity = Column(Integer)
    unit = Column(String)
    is_added = Column(Boolean, default=False)

    custom_drink = relationship("CustomDrink", back_populates="ingredients")
    ingredient = relationship("Ingredient")

