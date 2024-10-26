from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Turnover(Base):
    __tablename__ = "turnovers"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, index=True)
    year = Column(Integer)
    turnover = Column(Float)