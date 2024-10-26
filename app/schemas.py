from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

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