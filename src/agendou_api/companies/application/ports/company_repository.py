from typing import Protocol
from uuid import UUID

from agendou_api.companies.domain.company import Company


class CompanyRepository(Protocol):
    async def get_by_id(self, company_id: UUID) -> Company | None: ...

    async def save(self, company: Company) -> Company: ...

    async def update(self, company: Company) -> Company: ...

    async def list_paginated(self, *, skip: int, limit: int) -> list[Company]: ...
