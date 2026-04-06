from uuid import UUID

from agendou_api.users.application.commands.authenticate_user_use_case import (
    AmbiguousCompanyError,
)
from agendou_api.users.application.ports.email_sender import EmailSender
from agendou_api.users.application.ports.jwt_token_provider import JwtTokenProvider
from agendou_api.users.application.ports.user_repository import UserRepository


class RequestPasswordResetUseCase:
    def __init__(
        self,
        users: UserRepository,
        tokens: JwtTokenProvider,
        email_sender: EmailSender,
    ) -> None:
        self._users = users
        self._tokens = tokens
        self._email_sender = email_sender

    async def execute(self, *, email: str, company_id: UUID | None) -> None:
        try:
            user = await self._resolve_user(email=email, company_id=company_id)
        except AmbiguousCompanyError:
            return
        if user is None or user.id is None:
            return
        token = self._tokens.create_password_reset_token(user_id=user.id)
        await self._email_sender.send_password_reset(to_email=email, reset_token=token)

    async def _resolve_user(self, *, email: str, company_id: UUID | None):
        if company_id is not None:
            return await self._users.get_by_company_and_email(company_id, email)
        users = await self._users.list_by_email(email)
        if len(users) == 0:
            return None
        if len(users) == 1:
            return users[0]
        raise AmbiguousCompanyError
