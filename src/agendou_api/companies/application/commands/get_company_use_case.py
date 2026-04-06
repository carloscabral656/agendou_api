from uuid import UUID

from agendou_api.companies.application.ports.company_repository import CompanyRepository
from agendou_api.companies.domain.company import Company


class GetCompanyUseCase:
    def __init__(self, companies: CompanyRepository) -> None:
        self._companies = companies

    async def execute(self, company_id: UUID) -> Company | None:
        return await self._companies.get_by_id(company_id)
