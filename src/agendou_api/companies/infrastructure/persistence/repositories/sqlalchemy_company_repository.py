from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from agendou_api.companies.domain.company import Company
from agendou_api.companies.infrastructure.persistence.models.company_model import CompanyModel


def _to_domain(row: CompanyModel) -> Company:
    return Company(
        id=row.id,
        legal_name=row.legal_name,
        trade_name=row.trade_name,
        document_number=row.document_number,
        email=row.email,
        phone=row.phone,
        website=row.website,
        timezone=row.timezone,
        currency=row.currency,
        status=row.status,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


class SqlAlchemyCompanyRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, company_id: UUID) -> Company | None:
        result = await self._session.execute(
            select(CompanyModel).where(CompanyModel.id == company_id),
        )
        row = result.scalar_one_or_none()
        return _to_domain(row) if row else None

    async def save(self, company: Company) -> Company:
        model = CompanyModel(
            legal_name=company.legal_name,
            trade_name=company.trade_name,
            document_number=company.document_number,
            email=company.email,
            phone=company.phone,
            website=company.website,
            timezone=company.timezone,
            currency=company.currency,
            status=company.status,
        )
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return _to_domain(model)

    async def update(self, company: Company) -> Company:
        if company.id is None:
            msg = "Company id is required for update"
            raise ValueError(msg)
        result = await self._session.execute(
            select(CompanyModel).where(CompanyModel.id == company.id),
        )
        model = result.scalar_one_or_none()
        if model is None:
            msg = "Company not found"
            raise ValueError(msg)
        model.legal_name = company.legal_name
        model.trade_name = company.trade_name
        model.document_number = company.document_number
        model.email = company.email
        model.phone = company.phone
        model.website = company.website
        model.timezone = company.timezone
        model.currency = company.currency
        model.status = company.status
        await self._session.flush()
        await self._session.refresh(model)
        return _to_domain(model)

    async def list_paginated(self, *, skip: int, limit: int) -> list[Company]:
        stmt = (
            select(CompanyModel).order_by(CompanyModel.created_at.desc()).offset(skip).limit(limit)
        )
        result = await self._session.execute(stmt)
        return [_to_domain(r) for r in result.scalars().all()]
