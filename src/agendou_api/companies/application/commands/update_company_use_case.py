from uuid import UUID

from agendou_api.companies.application.ports.company_repository import CompanyRepository
from agendou_api.companies.domain.company import Company
from agendou_api.companies.domain.enums import CompanyStatus


class UpdateCompanyUseCase:
    def __init__(self, companies: CompanyRepository) -> None:
        self._companies = companies

    async def execute(
        self,
        company_id: UUID,
        *,
        legal_name: str | None = None,
        trade_name: str | None = None,
        document_number: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        website: str | None = None,
        timezone: str | None = None,
        currency: str | None = None,
        status: CompanyStatus | None = None,
    ) -> Company:
        current = await self._companies.get_by_id(company_id)
        if current is None:
            msg = "Company not found"
            raise ValueError(msg)
        updated = Company(
            id=current.id,
            legal_name=legal_name if legal_name is not None else current.legal_name,
            trade_name=trade_name if trade_name is not None else current.trade_name,
            document_number=document_number
            if document_number is not None
            else current.document_number,
            email=email if email is not None else current.email,
            phone=phone if phone is not None else current.phone,
            website=website if website is not None else current.website,
            timezone=timezone if timezone is not None else current.timezone,
            currency=currency if currency is not None else current.currency,
            status=status if status is not None else current.status,
            created_at=current.created_at,
            updated_at=current.updated_at,
        )
        return await self._companies.update(updated)
