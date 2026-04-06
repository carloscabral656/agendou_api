from decimal import Decimal
from uuid import UUID

from agendou_api.companies.application.ports.unit_repository import UnitRepository
from agendou_api.companies.domain.enums import UnitStatus
from agendou_api.companies.domain.unit import Unit


class UpdateUnitUseCase:
    def __init__(self, units: UnitRepository) -> None:
        self._units = units

    async def execute(
        self,
        company_id: UUID,
        unit_id: UUID,
        *,
        name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        status: UnitStatus | None = None,
        zip_code: str | None = None,
        state: str | None = None,
        city: str | None = None,
        district: str | None = None,
        street: str | None = None,
        number: str | None = None,
        complement: str | None = None,
        latitude: Decimal | None = None,
        longitude: Decimal | None = None,
    ) -> Unit:
        current = await self._units.get_by_id_and_company(unit_id, company_id)
        if current is None:
            msg = "Unit not found"
            raise ValueError(msg)
        updated = Unit(
            id=current.id,
            company_id=current.company_id,
            name=name if name is not None else current.name,
            email=email if email is not None else current.email,
            phone=phone if phone is not None else current.phone,
            status=status if status is not None else current.status,
            zip_code=zip_code if zip_code is not None else current.zip_code,
            state=state if state is not None else current.state,
            city=city if city is not None else current.city,
            district=district if district is not None else current.district,
            street=street if street is not None else current.street,
            number=number if number is not None else current.number,
            complement=complement if complement is not None else current.complement,
            latitude=latitude if latitude is not None else current.latitude,
            longitude=longitude if longitude is not None else current.longitude,
            created_at=current.created_at,
            updated_at=current.updated_at,
        )
        return await self._units.update(updated)
