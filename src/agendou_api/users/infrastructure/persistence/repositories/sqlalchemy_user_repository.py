from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from agendou_api.users.domain.user import User
from agendou_api.users.infrastructure.persistence.models.user_model import UserModel


def _to_domain(row: UserModel) -> User:
    return User(id=row.id, name=row.name, email=row.email)


class SqlAlchemyUserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_email(self, email: str) -> User | None:
        result = await self._session.execute(select(UserModel).where(UserModel.email == email))
        row = result.scalar_one_or_none()
        return _to_domain(row) if row else None

    async def save(self, user: User) -> User:
        model = UserModel(name=user.name, email=user.email)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return _to_domain(model)
