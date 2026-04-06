from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class CreateUserBody(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
