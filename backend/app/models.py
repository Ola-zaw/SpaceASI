from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.sql import func

from app.database import Base

# tworzy tabele iss_positions
class ISSPosition(Base):
    __tablename__ = "iss_positions"

    id = Column(Integer, primary_key=True, index=True)

    latitude = Column(Float)
    longitude = Column(Float)

    created_at = Column(DateTime(timezone=True), server_default=func.now())