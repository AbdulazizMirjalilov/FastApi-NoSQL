from pydantic import BaseModel, EmailStr


class UserCreateSchema(BaseModel):
    full_name: str
    email: EmailStr
    password: str
