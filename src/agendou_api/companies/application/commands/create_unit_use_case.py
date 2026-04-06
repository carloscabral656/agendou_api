from decimal import Decimal
from uuid import UUID

from agendou_api.companies.application.ports.unit_repository import UnitRepository
from agendou_api.companies.domain.enums import UnitStatus
from agendou_api.companies.domain.unit import Unit


class CreateUnitUseCase:
    def __init__(self, units: UnitRepository) -> None:
        self._units = units

    async def execute(
        self,
        company_id: UUID,
        *,
        name: str,
        email: str | None = None,
        phone: str | None = None,
        status: UnitStatus = UnitStatus.active,
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
        unit = Unit(
            company_id=company_id,
            name=name,
            email=email,
            phone=phone,
            status=status,
            zip_code=zip_code,
            state=state,
            city=city,
            district=district,
            street=street,
            number=number,
            complement=complement,
            latitude=latitude,
            longitude=longitude,
        )
        return await self._units.save(unit)
