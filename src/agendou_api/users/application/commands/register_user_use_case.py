from uuid import UUID

from agendou_api.users.application.ports.password_hasher import PasswordHasher
from agendou_api.users.application.ports.user_repository import UserRepository
from agendou_api.users.domain.enums import UserRole, UserStatus
from agendou_api.users.domain.user import User


class RegisterUserUseCase:
    def __init__(self, users: UserRepository, password_hasher: PasswordHasher) -> None:
        self._users = users
        self._password_hasher = password_hasher

    async def execute(
        self,
        *,
        company_id: UUID,
        full_name: str,
        email: str,
        password: str,
        role: UserRole = UserRole.customer,
        status: UserStatus = UserStatus.active,
    ) -> User:
        existing = await self._users.get_by_company_and_email(company_id, email)
        if existing is not None:
            msg = "User with this email already exists for this company"
            raise ValueError(msg)
        password_hash = self._password_hasher.hash(password)
        user = User(
            company_id=company_id,
            full_name=full_name,
            email=email,
            password_hash=password_hash,
            role=role,
            status=status,
        )
        return await self._users.save(user)
