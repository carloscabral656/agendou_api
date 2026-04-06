from uuid import UUID

from agendou_api.companies.application.ports.company_settings_repository import (
    CompanySettingsRepository,
)
from agendou_api.companies.domain.company_settings import CompanySettings


class GetCompanySettingsUseCase:
    def __init__(self, settings: CompanySettingsRepository) -> None:
        self._settings = settings

    async def execute(self, company_id: UUID) -> CompanySettings | None:
        return await self._settings.get_by_company_id(company_id)
