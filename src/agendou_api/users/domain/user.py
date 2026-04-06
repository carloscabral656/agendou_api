from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from agendou_api.users.domain.enums import UserRole, UserStatus


@dataclass
class User:
    full_name: str
    email: str
    id: UUID | None = None
    company_id: UUID | None = None
    phone: str | None = None
    password_hash: str | None = None
    role: UserRole = UserRole.customer
    status: UserStatus = UserStatus.active
    avatar_url: str | None = None
    last_login_at: datetime | None = None
