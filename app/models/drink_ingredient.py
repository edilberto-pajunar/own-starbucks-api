from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.config import Base


class DrinkIngredient(Base):
    __tablename__ = "drink_ingredients"

    id = Column(Integer, primary_key=True)
    drink_id = Column(Integer, ForeignKey("drinks.id"))
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"))
    quantity = Column(Integer)
    unit = Column(String) # pump | shot | ml
    is_removable = Column(Boolean, default=True)

    drink = relationship("Drink", back_populates="ingredients")
    ingredient = relationship("Ingredient", back_populates="drinks")