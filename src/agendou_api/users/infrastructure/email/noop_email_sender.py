import logging

logger = logging.getLogger(__name__)


class NoopEmailSender:
    async def send_password_reset(self, *, to_email: str, reset_token: str) -> None:
        logger.info(
            "Password reset stub: email=%s token_prefix=%s...",
            to_email,
            reset_token[:12] if reset_token else "",
        )
