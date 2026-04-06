from agendou_api.users.application.ports.user_repository import UserRepository
from agendou_api.users.domain.user import User


class CreateUserUseCase:
    def __init__(self, users: UserRepository) -> None:
        self._users = users

    async def execute(self, *, name: str, email: str) -> User:
        existing = await self._users.get_by_email(email)
        if existing is not None:
            msg = "User with this email already exists"
            raise ValueError(msg)
        user = User(name=name, email=email)
        return await self._users.save(user)
