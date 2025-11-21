from pydantic import BaseModel, Field
from typing import Optional

class PhotoCreate(BaseModel):
    name: str = Field(min_length=1)
    alt_text:Optional[str] = None
    url:str = Field(min_length=1)

class Photo(PhotoCreate):
    id: int
    id_location: int
    class Config:
        from_attributes = True


