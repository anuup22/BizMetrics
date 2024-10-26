from pydantic import BaseModel

class TurnoverBase(BaseModel):
    company_name: str
    year: int
    turnover: float

class TurnoverCreate(TurnoverBase):
    pass

class Turnover(TurnoverBase):
    id: int

    class Config:
        from_attributes = True