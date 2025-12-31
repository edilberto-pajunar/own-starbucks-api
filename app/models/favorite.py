from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.config import Base
import datetime


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, nullable=False)
    drink_id = Column(Integer, ForeignKey("drinks.id"), nullable=False)
    is_custom = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.datetime.now(datetime.timezone.utc))

    drink = relationship("Drink", back_populates="favorites")