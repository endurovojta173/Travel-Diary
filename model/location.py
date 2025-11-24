from pydantic import BaseModel, Field

class LocationCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=10)
