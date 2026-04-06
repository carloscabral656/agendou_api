from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from agendou_api.companies.domain.unit import Unit
from agendou_api.companies.infrastructure.persistence.models.unit_model import UnitModel


def _to_domain(row: UnitModel) -> Unit:
    return Unit(
        id=row.id,
        company_id=row.company_id,
        name=row.name,
        email=row.email,
        phone=row.phone,
        status=row.status,
        zip_code=row.zip_code,
        state=row.state,
        city=row.city,
        district=row.district,
        street=row.street,
        number=row.number,
        complement=row.complement,
        latitude=row.latitude,
        longitude=row.longitude,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


class SqlAlchemyUnitRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_by_company(self, company_id: UUID) -> list[Unit]:
        result = await self._session.execute(
            select(UnitModel).where(UnitModel.company_id == company_id).order_by(UnitModel.name),
        )
        return [_to_domain(r) for r in result.scalars().all()]

    async def get_by_id_and_company(self, unit_id: UUID, company_id: UUID) -> Unit | None:
        result = await self._session.execute(
            select(UnitModel).where(
                UnitModel.id == unit_id,
                UnitModel.company_id == company_id,
            ),
        )
        row = result.scalar_one_or_none()
        return _to_domain(row) if row else None

    async def save(self, unit: Unit) -> Unit:
        model = UnitModel(
            company_id=unit.company_id,
            name=unit.name,
            email=unit.email,
            phone=unit.phone,
            status=unit.status,
            zip_code=unit.zip_code,
            state=unit.state,
            city=unit.city,
            district=unit.district,
            street=unit.street,
            number=unit.number,
            complement=unit.complement,
            latitude=unit.latitude,
            longitude=unit.longitude,
        )
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return _to_domain(model)

    async def update(self, unit: Unit) -> Unit:
        if unit.id is None:
            msg = "Unit id is required for update"
            raise ValueError(msg)
        result = await self._session.execute(
            select(UnitModel).where(
                UnitModel.id == unit.id,
                UnitModel.company_id == unit.company_id,
            ),
        )
        model = result.scalar_one_or_none()
        if model is None:
            msg = "Unit not found"
            raise ValueError(msg)
        model.name = unit.name
        model.email = unit.email
        model.phone = unit.phone
        model.status = unit.status
        model.zip_code = unit.zip_code
        model.state = unit.state
        model.city = unit.city
        model.district = unit.district
        model.street = unit.street
        model.number = unit.number
        model.complement = unit.complement
        model.latitude = unit.latitude
        model.longitude = unit.longitude
        await self._session.flush()
        await self._session.refresh(model)
        return _to_domain(model)
