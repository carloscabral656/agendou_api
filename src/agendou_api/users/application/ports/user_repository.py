from typing import Protocol

from agendou_api.users.domain.user import User


class UserRepository(Protocol):
    async def save(self, user: User) -> User: ...

    async def get_by_email(self, email: str) -> User | None: ...
