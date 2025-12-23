from app.config import Base
from sqlalchemy import Column, Integer, Float, String, DateTime



class CustomizedDrink(Base):
    __tablename__ = "customized_drinks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    base_drink_name = Column(String, nullable=False)
    base_drink_photo = Column(String, nullable=False)
    image = Column(String, nullable=False)
    milk_type = Column(String, nullable=False)
    sugar_level = Column(String, nullable=False)
    cup_size = Column(String, nullable=False)
    extras = Column(String, nullable=False)
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False)
