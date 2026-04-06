from dataclasses import dataclass

from agendou_api.companies.application.ports.company_repository import CompanyRepository
from agendou_api.companies.application.ports.company_settings_repository import (
    CompanySettingsRepository,
)
from agendou_api.companies.domain.company import Company
from agendou_api.companies.domain.company_settings import CompanySettings
from agendou_api.companies.domain.enums import CompanyStatus
from agendou_api.users.application.ports.password_hasher import PasswordHasher
from agendou_api.users.application.ports.user_repository import UserRepository
from agendou_api.users.domain.enums import UserRole, UserStatus
from agendou_api.users.domain.user import User


def _normalize_document(document_number: str | None) -> str | None:
    if document_number is None:
        return None
    stripped = document_number.strip()
    return stripped or None


@dataclass
class OnboardCompanyResult:
    company: Company
    admin_user: User


class OnboardCompanyUseCase:
    def __init__(
        self,
        companies: CompanyRepository,
        settings: CompanySettingsRepository,
        users: UserRepository,
        password_hasher: PasswordHasher,
    ) -> None:
        self._companies = companies
        self._settings = settings
        self._users = users
        self._password_hasher = password_hasher

    async def execute(
        self,
        *,
        legal_name: str,
        trade_name: str | None,
        document_number: str | None,
        company_email: str | None,
        company_phone: str | None,
        website: str | None,
        timezone: str,
        currency: str,
        admin_full_name: str,
        admin_email: str,
        admin_password: str,
    ) -> OnboardCompanyResult:
        doc = _normalize_document(document_number)
        company = Company(
            legal_name=legal_name.strip(),
            trade_name=trade_name.strip() if trade_name else None,
            document_number=doc,
            email=company_email.strip() if company_email else None,
            phone=company_phone.strip() if company_phone else None,
            website=website.strip() if website else None,
            timezone=timezone,
            currency=currency,
            status=CompanyStatus.active,
        )
        company = await self._companies.save(company)
        assert company.id is not None
        settings_row = CompanySettings(company_id=company.id)
        await self._settings.save(settings_row)

        existing = await self._users.get_by_company_and_email(company.id, admin_email)
        if existing is not None:
            msg = "User with this email already exists for this company"
            raise ValueError(msg)

        password_hash = self._password_hasher.hash(admin_password)
        admin = User(
            company_id=company.id,
            full_name=admin_full_name.strip(),
            email=admin_email.strip().lower(),
            password_hash=password_hash,
            role=UserRole.company_admin,
            status=UserStatus.active,
        )
        admin = await self._users.save(admin)
        return OnboardCompanyResult(company=company, admin_user=admin)
