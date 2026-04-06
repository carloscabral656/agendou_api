from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID

import jwt

from agendou_api.config.settings import Settings

TOKEN_TYPE_RESET = "password_reset"


class PyJwtTokenProvider:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def create_access_token(
        self,
        *,
        user_id: UUID,
        role: str,
        company_id: UUID | None,
    ) -> str:
        expire = datetime.now(UTC) + timedelta(minutes=self._settings.access_token_expire_minutes)
        payload: dict[str, Any] = {
            "sub": str(user_id),
            "role": role,
            "exp": expire,
            "type": "access",
        }
        if company_id is not None:
            payload["company_id"] = str(company_id)
        return jwt.encode(
            payload,
            self._settings.jwt_secret_key,
            algorithm=self._settings.jwt_algorithm,
        )

    def decode_access_token(self, token: str) -> dict[str, Any]:
        payload = jwt.decode(
            token,
            self._settings.jwt_secret_key,
            algorithms=[self._settings.jwt_algorithm],
        )
        if payload.get("type") != "access":
            msg = "Not an access token"
            raise ValueError(msg)
        return payload

    def create_password_reset_token(self, *, user_id: UUID) -> str:
        expire = datetime.now(UTC) + timedelta(
            minutes=self._settings.password_reset_token_expire_minutes
        )
        payload = {
            "sub": str(user_id),
            "exp": expire,
            "type": TOKEN_TYPE_RESET,
        }
        return jwt.encode(
            payload,
            self._settings.jwt_secret_key,
            algorithm=self._settings.jwt_algorithm,
        )

    def decode_password_reset_token(self, token: str) -> UUID:
        try:
            payload = jwt.decode(
                token,
                self._settings.jwt_secret_key,
                algorithms=[self._settings.jwt_algorithm],
            )
        except jwt.PyJWTError as e:
            msg = "Invalid or expired reset token"
            raise ValueError(msg) from e
        if payload.get("type") != TOKEN_TYPE_RESET:
            msg = "Invalid token type"
            raise ValueError(msg)
        try:
            return UUID(payload["sub"])
        except (KeyError, ValueError) as e:
            msg = "Invalid or expired reset token"
            raise ValueError(msg) from e
