from agendou_api.users.application.commands.create_user_use_case import CreateUserUseCase
from agendou_api.users.domain.user import User


class UserController:
    def __init__(self, create_user_use_case: CreateUserUseCase) -> None:
        self._create_user_use_case = create_user_use_case

    async def create_user(self, *, name: str, email: str) -> User:
        return await self._create_user_use_case.execute(name=name, email=email)
