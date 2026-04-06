from typing import Protocol


class EmailSender(Protocol):
    async def send_password_reset(self, *, to_email: str, reset_token: str) -> None: ...
