from uuid import UUID

from agendou_api.users.application.ports.user_repository import UserRepository
from agendou_api.users.domain.user import User


class UpdateProfileUseCase:
    def __init__(self, users: UserRepository) -> None:
        self._users = users

    async def execute(
        self,
        *,
        user_id: UUID,
        full_name: str | None = None,
        phone: str | None = None,
        avatar_url: str | None = None,
    ) -> User:
        user = await self._users.get_by_id(user_id)
        if user is None:
            msg = "User not found"
            raise ValueError(msg)
        if full_name is not None:
            user.full_name = full_name
        if phone is not None:
            user.phone = phone
        if avatar_url is not None:
            user.avatar_url = avatar_url
        return await self._users.update(user)
