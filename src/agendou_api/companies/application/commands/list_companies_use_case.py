from agendou_api.companies.application.ports.company_repository import CompanyRepository
from agendou_api.companies.domain.company import Company


class ListCompaniesUseCase:
    def __init__(self, companies: CompanyRepository) -> None:
        self._companies = companies

    async def execute(self, *, skip: int, limit: int) -> list[Company]:
        return await self._companies.list_paginated(skip=skip, limit=limit)
