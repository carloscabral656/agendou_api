from uuid import UUID

from agendou_api.companies.application.ports.unit_repository import UnitRepository
from agendou_api.companies.domain.unit import Unit


class ListUnitsUseCase:
    def __init__(self, units: UnitRepository) -> None:
        self._units = units

    async def execute(self, company_id: UUID) -> list[Unit]:
        return await self._units.list_by_company(company_id)
