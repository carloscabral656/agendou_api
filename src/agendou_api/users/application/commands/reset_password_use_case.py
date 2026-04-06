from agendou_api.users.application.ports.jwt_token_provider import JwtTokenProvider
from agendou_api.users.application.ports.password_hasher import PasswordHasher
from agendou_api.users.application.ports.user_repository import UserRepository


class ResetPasswordUseCase:
    def __init__(
        self,
        users: UserRepository,
        password_hasher: PasswordHasher,
        tokens: JwtTokenProvider,
    ) -> None:
        self._users = users
        self._password_hasher = password_hasher
        self._tokens = tokens

    async def execute(self, *, token: str, new_password: str) -> None:
        try:
            user_id = self._tokens.decode_password_reset_token(token)
        except ValueError as e:
            msg = "Invalid or expired reset token"
            raise ValueError(msg) from e
        user = await self._users.get_by_id(user_id)
        if user is None:
            msg = "Invalid or expired reset token"
            raise ValueError(msg)
        password_hash = self._password_hasher.hash(new_password)
        await self._users.update_password_hash(user_id, password_hash)
