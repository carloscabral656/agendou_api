from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from agendou_api.config.settings import Settings, get_settings
from agendou_api.shared.infrastructure.database.session import get_async_session
from agendou_api.shared.infrastructure.security.bcrypt_password_hasher import BcryptPasswordHasher
from agendou_api.shared.infrastructure.security.pyjwt_token_provider import PyJwtTokenProvider
from agendou_api.users.application.commands.authenticate_user_use_case import (
    AuthenticateUserUseCase,
)
from agendou_api.users.application.commands.register_user_use_case import RegisterUserUseCase
from agendou_api.users.application.commands.request_password_reset_use_case import (
    RequestPasswordResetUseCase,
)
from agendou_api.users.application.commands.reset_password_use_case import ResetPasswordUseCase
from agendou_api.users.application.commands.update_profile_use_case import UpdateProfileUseCase
from agendou_api.users.infrastructure.email.noop_email_sender import NoopEmailSender
from agendou_api.users.infrastructure.persistence.repositories.sqlalchemy_user_repository import (
    SqlAlchemyUserRepository,
)

_password_hasher = BcryptPasswordHasher()
_email_sender = NoopEmailSender()


def get_password_hasher() -> BcryptPasswordHasher:
    return _password_hasher


def get_email_sender() -> NoopEmailSender:
    return _email_sender


def get_jwt_token_provider(settings: Settings = Depends(get_settings)) -> PyJwtTokenProvider:
    return PyJwtTokenProvider(settings)


def get_user_repository(
    session: AsyncSession = Depends(get_async_session),
) -> SqlAlchemyUserRepository:
    return SqlAlchemyUserRepository(session)


def get_register_user_use_case(
    repo: SqlAlchemyUserRepository = Depends(get_user_repository),
    hasher: BcryptPasswordHasher = Depends(get_password_hasher),
) -> RegisterUserUseCase:
    return RegisterUserUseCase(repo, hasher)


def get_authenticate_user_use_case(
    repo: SqlAlchemyUserRepository = Depends(get_user_repository),
    hasher: BcryptPasswordHasher = Depends(get_password_hasher),
) -> AuthenticateUserUseCase:
    return AuthenticateUserUseCase(repo, hasher)


def get_update_profile_use_case(
    repo: SqlAlchemyUserRepository = Depends(get_user_repository),
) -> UpdateProfileUseCase:
    return UpdateProfileUseCase(repo)


def get_request_password_reset_use_case(
    repo: SqlAlchemyUserRepository = Depends(get_user_repository),
    tokens: PyJwtTokenProvider = Depends(get_jwt_token_provider),
    mail: NoopEmailSender = Depends(get_email_sender),
) -> RequestPasswordResetUseCase:
    return RequestPasswordResetUseCase(repo, tokens, mail)


def get_reset_password_use_case(
    repo: SqlAlchemyUserRepository = Depends(get_user_repository),
    hasher: BcryptPasswordHasher = Depends(get_password_hasher),
    tokens: PyJwtTokenProvider = Depends(get_jwt_token_provider),
) -> ResetPasswordUseCase:
    return ResetPasswordUseCase(repo, hasher, tokens)
