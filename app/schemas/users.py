from datetime import datetime
import enum
from pydantic import BaseModel, Field, EmailStr


class UserTypes(str, enum.Enum):
    ADMIN = "admin"
    ORGANIZER = "organizer"
    USER = "user"


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: str = Field(..., min_length=3, max_length=100)
    user_type: UserTypes


class UserCreate(UserBase):
    hashed_password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = Field(None, min_length=3, max_length=100)
    password: str | None = Field(None, min_length=6)
    user_type: UserTypes | None = Field(None)


class UserOut(UserBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
