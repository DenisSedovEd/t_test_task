from sqlalchemy.orm import DeclarativeBase


class OperatorBase(DeclarativeBase):
    name: str
    is_active: bool
    max_load_limit: int

class OperatorCreate(OperatorBase):
    pass

class OperatorResponse(OperatorBase):
    id: int
    class Config:
        from_attributes = True

