from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from agendou_api.users.domain.user import User
from agendou_api.users.infrastructure.persistence.models.user_model import UserModel


def _to_domain(row: UserModel) -> User:
    return User(
        id=row.id,
        company_id=row.company_id,
        full_name=row.full_name,
        email=row.email,
        phone=row.phone,
        password_hash=row.password_hash,
        role=row.role,
        status=row.status,
        avatar_url=row.avatar_url,
        last_login_at=row.last_login_at,
    )


class SqlAlchemyUserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        result = await self._session.execute(select(UserModel).where(UserModel.id == user_id))
        row = result.scalar_one_or_none()
        return _to_domain(row) if row else None

    async def get_by_company_and_email(self, company_id: UUID | None, email: str) -> User | None:
        stmt = select(UserModel).where(UserModel.email == email)
        if company_id is not None:
            stmt = stmt.where(UserModel.company_id == company_id)
        else:
            stmt = stmt.where(UserModel.company_id.is_(None))
        result = await self._session.execute(stmt)
        row = result.scalar_one_or_none()
        return _to_domain(row) if row else None

    async def list_by_email(self, email: str) -> list[User]:
        result = await self._session.execute(select(UserModel).where(UserModel.email == email))
        return [_to_domain(r) for r in result.scalars().all()]

    async def save(self, user: User) -> User:
        model = UserModel(
            company_id=user.company_id,
            full_name=user.full_name,
            email=user.email,
            phone=user.phone,
            password_hash=user.password_hash,
            role=user.role,
            status=user.status,
            avatar_url=user.avatar_url,
        )
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return _to_domain(model)

    async def update(self, user: User) -> User:
        if user.id is None:
            msg = "User id is required for update"
            raise ValueError(msg)
        result = await self._session.execute(select(UserModel).where(UserModel.id == user.id))
        model = result.scalar_one_or_none()
        if model is None:
            msg = "User not found"
            raise ValueError(msg)
        model.full_name = user.full_name
        model.phone = user.phone
        model.avatar_url = user.avatar_url
        await self._session.flush()
        await self._session.refresh(model)
        return _to_domain(model)

    async def update_password_hash(self, user_id: UUID, password_hash: str) -> None:
        await self._session.execute(
            update(UserModel).where(UserModel.id == user_id).values(password_hash=password_hash)
        )

    async def set_last_login_at(self, user_id: UUID) -> None:
        from datetime import UTC, datetime

        await self._session.execute(
            update(UserModel).where(UserModel.id == user_id).values(last_login_at=datetime.now(UTC))
        )
