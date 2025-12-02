from typing import Optional

from pydantic import BaseModel


class OperatorBase(BaseModel):
    name: str
    is_active: bool
    max_load_limit: int


class OperatorCreate(OperatorBase):
    pass


class OperatorResponse(OperatorBase):
    id: int

    class Config:
        from_attributes = True


class OperatorUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None
    max_load_limit: Optional[int] = None

    class Config:
        from_attributes = True
