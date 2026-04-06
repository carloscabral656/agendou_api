from typing import Protocol
from uuid import UUID

from agendou_api.companies.domain.unit import Unit


class UnitRepository(Protocol):
    async def list_by_company(self, company_id: UUID) -> list[Unit]: ...

    async def get_by_id_and_company(self, unit_id: UUID, company_id: UUID) -> Unit | None: ...

    async def save(self, unit: Unit) -> Unit: ...

    async def update(self, unit: Unit) -> Unit: ...
