from typing import Any, Protocol
from uuid import UUID


class JwtTokenProvider(Protocol):
    def create_access_token(
        self,
        *,
        user_id: UUID,
        role: str,
        company_id: UUID | None,
    ) -> str: ...

    def decode_access_token(self, token: str) -> dict[str, Any]: ...

    def create_password_reset_token(self, *, user_id: UUID) -> str: ...

    def decode_password_reset_token(self, token: str) -> UUID: ...
