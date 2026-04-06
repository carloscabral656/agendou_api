from uuid import UUID

from agendou_api.users.application.ports.password_hasher import PasswordHasher
from agendou_api.users.application.ports.user_repository import UserRepository
from agendou_api.users.domain.user import User


class AmbiguousCompanyError(Exception):
    """Several accounts share this email; client must send company_id."""


class AuthenticateUserUseCase:
    def __init__(self, users: UserRepository, password_hasher: PasswordHasher) -> None:
        self._users = users
        self._password_hasher = password_hasher

    async def resolve_login_identity(
        self,
        *,
        email: str,
        company_id: UUID | None,
    ) -> User | None:
        if company_id is not None:
            return await self._users.get_by_company_and_email(company_id, email)
        users = await self._users.list_by_email(email)
        if len(users) == 0:
            return None
        if len(users) == 1:
            return users[0]
        raise AmbiguousCompanyError

    async def execute(
        self,
        *,
        email: str,
        password: str,
        company_id: UUID | None,
    ) -> User:
        user = await self.resolve_login_identity(email=email, company_id=company_id)
        if user is None:
            msg = "Invalid email or password"
            raise ValueError(msg)
        if not user.password_hash:
            msg = "Invalid email or password"
            raise ValueError(msg)
        if not self._password_hasher.verify(password, user.password_hash):
            msg = "Invalid email or password"
            raise ValueError(msg)
        assert user.id is not None
        await self._users.set_last_login_at(user.id)
        return user
