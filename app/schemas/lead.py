from typing import List

from pydantic import BaseModel

from app.schemas.contact import ContactResponse


class LeadResponse(BaseModel):
    id: int
    external_id: str
    contacts: List[ContactResponse] = []

    class Config:
        from_attributes = True