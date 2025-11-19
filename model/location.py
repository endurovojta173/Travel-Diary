from pydantic import BaseModel, Field

class LocationCreate(BaseModel):
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    id_user: int

class Location(LocationCreate):
    id: int
    class Config:
        from_attributes= True
