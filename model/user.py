from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    name:str = Field(min_length=3,max_length=500)
    email:str = Field(min_length=4,max_length=500)
    password:str = Field(min_length=8)
class UserLogin(BaseModel):
    email:str = Field(min_length=4,max_length=500)
    password:str = Field(min_length=8)
class UserOut(BaseModel):
    id:int
    name:str
    email:str
    role:str