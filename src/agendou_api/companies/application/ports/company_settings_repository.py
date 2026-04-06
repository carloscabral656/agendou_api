from typing import Protocol
from uuid import UUID

from agendou_api.companies.domain.company_settings import CompanySettings


class CompanySettingsRepository(Protocol):
    async def get_by_company_id(self, company_id: UUID) -> CompanySettings | None: ...

    async def save(self, settings: CompanySettings) -> CompanySettings: ...

    async def update(self, settings: CompanySettings) -> CompanySettings: ...
