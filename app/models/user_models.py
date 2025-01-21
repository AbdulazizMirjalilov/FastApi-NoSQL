from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserModel(BaseModel):
    id: Optional[str] = None
    full_name: str
    email: EmailStr
    password: str
    created_at: datetime = datetime.utcnow()
