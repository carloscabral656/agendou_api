from uuid import UUID

from pydantic import BaseModel, EmailStr

from agendou_api.users.domain.enums import UserRole, UserStatus
from agendou_api.users.domain.user import User


class UserPublic(BaseModel):
    id: UUID
    company_id: UUID | None
    full_name: str
    email: EmailStr
    phone: str | None
    role: UserRole
    status: UserStatus
    avatar_url: str | None


def user_to_public(user: User) -> UserPublic:
    if user.id is None:
        msg = "User must have id"
        raise ValueError(msg)
    return UserPublic(
        id=user.id,
        company_id=user.company_id,
        full_name=user.full_name,
        email=user.email,
        phone=user.phone,
        role=user.role,
        status=user.status,
        avatar_url=user.avatar_url,
    )
