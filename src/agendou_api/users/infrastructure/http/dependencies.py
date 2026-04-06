from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from agendou_api.shared.infrastructure.database.session import get_async_session
from agendou_api.users.application.commands.create_user_use_case import CreateUserUseCase
from agendou_api.users.infrastructure.http.controllers.user_controller import UserController
from agendou_api.users.infrastructure.persistence.repositories.sqlalchemy_user_repository import (
    SqlAlchemyUserRepository,
)


def get_user_repository(
    session: AsyncSession = Depends(get_async_session),
) -> SqlAlchemyUserRepository:
    return SqlAlchemyUserRepository(session)


def get_create_user_use_case(
    repo: SqlAlchemyUserRepository = Depends(get_user_repository),
) -> CreateUserUseCase:
    return CreateUserUseCase(repo)


def get_user_controller(
    use_case: CreateUserUseCase = Depends(get_create_user_use_case),
) -> UserController:
    return UserController(use_case)
