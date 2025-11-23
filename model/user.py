from pydantic import BaseModel, Field, EmailStr, ConfigDict


class UserBase(BaseModel):
    name:str = Field(min_length=3,max_length=100)
    email:str = EmailStr
class UserCreate(UserBase):
    password:str = Field(min_length=8,max_length=100)
class UserLogin(BaseModel):
    email: EmailStr
    password: str
class UserOut(UserBase):
    id: int
    id_role: int
    #Díky tomuto můžu přistupovat k user.atribut a ne jen jako k dict
    model_config = ConfigDict(from_attributes=True)