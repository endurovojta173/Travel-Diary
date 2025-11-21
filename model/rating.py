from pydantic import BaseModel, Field
from typing import Optional

class RatingCreate(BaseModel):
    rating: int = Field(min_length=1, max_length=1)

class Rating(RatingCreate):
    id: int
    id_user: int
    id_location: int
    class Config:
        from_attributes = True


