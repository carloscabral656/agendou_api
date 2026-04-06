from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from agendou_api.companies.application.commands.create_unit_use_case import CreateUnitUseCase
from agendou_api.companies.application.commands.get_company_settings_use_case import (
    GetCompanySettingsUseCase,
)
from agendou_api.companies.application.commands.get_company_use_case import GetCompanyUseCase
from agendou_api.companies.application.commands.get_unit_use_case import GetUnitUseCase
from agendou_api.companies.application.commands.list_companies_use_case import ListCompaniesUseCase
from agendou_api.companies.application.commands.list_units_use_case import ListUnitsUseCase
from agendou_api.companies.application.commands.onboard_company_use_case import (
    OnboardCompanyUseCase,
)
from agendou_api.companies.application.commands.update_company_settings_use_case import (
    UpdateCompanySettingsUseCase,
)
from agendou_api.companies.application.commands.update_company_use_case import UpdateCompanyUseCase
from agendou_api.companies.application.commands.update_unit_use_case import UpdateUnitUseCase
from agendou_api.companies.infrastructure.persistence.repositories import (
    SqlAlchemyCompanyRepository,
    SqlAlchemyCompanySettingsRepository,
    SqlAlchemyUnitRepository,
)
from agendou_api.shared.infrastructure.database.session import get_async_session
from agendou_api.shared.infrastructure.security.bcrypt_password_hasher import BcryptPasswordHasher
from agendou_api.users.infrastructure.http.dependencies import (
    get_password_hasher,
    get_user_repository,
)
from agendou_api.users.infrastructure.persistence.repositories.sqlalchemy_user_repository import (
    SqlAlchemyUserRepository,
)


def get_company_repository(
    session: AsyncSession = Depends(get_async_session),
) -> SqlAlchemyCompanyRepository:
    return SqlAlchemyCompanyRepository(session)


def get_company_settings_repository(
    session: AsyncSession = Depends(get_async_session),
) -> SqlAlchemyCompanySettingsRepository:
    return SqlAlchemyCompanySettingsRepository(session)


def get_unit_repository(
    session: AsyncSession = Depends(get_async_session),
) -> SqlAlchemyUnitRepository:
    return SqlAlchemyUnitRepository(session)


def get_get_company_use_case(
    repo: SqlAlchemyCompanyRepository = Depends(get_company_repository),
) -> GetCompanyUseCase:
    return GetCompanyUseCase(repo)


def get_list_companies_use_case(
    repo: SqlAlchemyCompanyRepository = Depends(get_company_repository),
) -> ListCompaniesUseCase:
    return ListCompaniesUseCase(repo)


def get_update_company_use_case(
    repo: SqlAlchemyCompanyRepository = Depends(get_company_repository),
) -> UpdateCompanyUseCase:
    return UpdateCompanyUseCase(repo)


def get_get_company_settings_use_case(
    repo: SqlAlchemyCompanySettingsRepository = Depends(get_company_settings_repository),
) -> GetCompanySettingsUseCase:
    return GetCompanySettingsUseCase(repo)


def get_update_company_settings_use_case(
    repo: SqlAlchemyCompanySettingsRepository = Depends(get_company_settings_repository),
) -> UpdateCompanySettingsUseCase:
    return UpdateCompanySettingsUseCase(repo)


def get_list_units_use_case(
    repo: SqlAlchemyUnitRepository = Depends(get_unit_repository),
) -> ListUnitsUseCase:
    return ListUnitsUseCase(repo)


def get_create_unit_use_case(
    repo: SqlAlchemyUnitRepository = Depends(get_unit_repository),
) -> CreateUnitUseCase:
    return CreateUnitUseCase(repo)


def get_get_unit_use_case(
    repo: SqlAlchemyUnitRepository = Depends(get_unit_repository),
) -> GetUnitUseCase:
    return GetUnitUseCase(repo)


def get_update_unit_use_case(
    repo: SqlAlchemyUnitRepository = Depends(get_unit_repository),
) -> UpdateUnitUseCase:
    return UpdateUnitUseCase(repo)


def get_onboard_company_use_case(
    companies: SqlAlchemyCompanyRepository = Depends(get_company_repository),
    settings: SqlAlchemyCompanySettingsRepository = Depends(get_company_settings_repository),
    users: SqlAlchemyUserRepository = Depends(get_user_repository),
    hasher: BcryptPasswordHasher = Depends(get_password_hasher),
) -> OnboardCompanyUseCase:
    return OnboardCompanyUseCase(companies, settings, users, hasher)
