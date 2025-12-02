from sqlalchemy.orm import DeclarativeBase


class SourceWeightCreate(DeclarativeBase):
    operator_id: int
    weight: int

class SourceCreate(DeclarativeBase):
    name: str

class SourceResponse(DeclarativeBase):
    id: int
    name: str

    class Config:
        from_attributes = True