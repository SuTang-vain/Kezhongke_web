from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from typing import Optional

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    nickname: Optional[str] = Field(default=None)
    avatar_url: Optional[str] = Field(default=None)
    bio: Optional[str] = Field(default=None)
    is_active: bool = True
    is_verified: bool = False
    role: str = "member"

class User(UserBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    hashed_password: str

class UserCreate(UserBase):
    password: str

class UserUpdate(SQLModel):
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    password: Optional[str] = None

class UserRead(UserBase):
    id: UUID
