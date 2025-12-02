from typing import List

from pydantic import BaseModel


class SourceWeightCreate(BaseModel):
    operator_id: int
    weight: int


class SourceCreate(BaseModel):
    name: str


class SourceCreateRequest(BaseModel):
    name: str
    weights: List[SourceWeightCreate]


class SourceResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
