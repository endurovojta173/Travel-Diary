from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator


class UserBase(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=100)

    @field_validator('password')
    @classmethod
    def validate_password_complexity(cls, validate_password: str) -> str:
        # Kontrola čísla
        if not any(char.isdigit() for char in validate_password):
            raise ValueError('Heslo musí obsahovat alespoň jednu číslici')

        # Kontrola velkého písmene
        if not any(char.isupper() for char in validate_password):
            raise ValueError('Heslo musí obsahovat alespoň jedno velké písmeno')

        # Kontrola speciálního znaku
        if not any(char in "!@#$%^&*()-_=+" for char in validate_password):
            raise ValueError('Heslo musí obsahovat speciální znak')

        return validate_password

class UserCreateWithRole(UserCreate):
    role: int
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(UserBase):
    id: int
    id_role: int
    #Díky tomuto můžu přistupovat k user.atribut a ne jen jako k dict
    model_config = ConfigDict(from_attributes=True)
