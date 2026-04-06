from uuid import UUID

from agendou_api.companies.application.ports.unit_repository import UnitRepository
from agendou_api.companies.domain.unit import Unit


class GetUnitUseCase:
    def __init__(self, units: UnitRepository) -> None:
        self._units = units

    async def execute(self, company_id: UUID, unit_id: UUID) -> Unit | None:
        return await self._units.get_by_id_and_company(unit_id, company_id)
