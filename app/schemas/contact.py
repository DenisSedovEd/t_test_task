from datetime import datetime
from typing import Optional

from sqlalchemy.orm import DeclarativeBase


class ContactBase(DeclarativeBase):
    pass

class ContactCreate(ContactBase):
    lead_external_id: str
    source_id: int
    message: Optional[str] = None

class ContactResponse(ContactBase):
    id: int
    lead_id: int
    operator_id: Optional[int]
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True