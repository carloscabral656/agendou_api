from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError

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
from agendou_api.companies.domain.enums import UnitStatus
from agendou_api.companies.infrastructure.http.dependencies import (
    get_create_unit_use_case,
    get_get_company_settings_use_case,
    get_get_company_use_case,
    get_get_unit_use_case,
    get_list_companies_use_case,
    get_list_units_use_case,
    get_onboard_company_use_case,
    get_update_company_settings_use_case,
    get_update_company_use_case,
    get_update_unit_use_case,
)
from agendou_api.companies.infrastructure.http.schemas.company_schemas import (
    CompanyPublic,
    OnboardCompanyBody,
    PatchCompanyBody,
    company_to_public,
)
from agendou_api.companies.infrastructure.http.schemas.onboarding_schemas import OnboardingResponse
from agendou_api.companies.infrastructure.http.schemas.settings_schemas import (
    CompanySettingsPublic,
    PatchCompanySettingsBody,
    settings_to_public,
)
from agendou_api.companies.infrastructure.http.schemas.unit_schemas import (
    CreateUnitBody,
    PatchUnitBody,
    UnitPublic,
    unit_to_public,
)
from agendou_api.shared.infrastructure.http.tenant_access import require_company_scoped
from agendou_api.shared.infrastructure.security.pyjwt_token_provider import PyJwtTokenProvider
from agendou_api.users.domain.enums import UserRole
from agendou_api.users.domain.user import User
from agendou_api.users.infrastructure.http.dependencies import get_jwt_token_provider
from agendou_api.users.infrastructure.http.schemas.user_public import user_to_public
from agendou_api.users.infrastructure.http.security import get_current_active_user, require_roles

router = APIRouter(prefix="/companies", tags=["companies"])

_read_tenant = require_company_scoped(
    UserRole.company_admin,
    UserRole.manager,
    UserRole.staff,
    UserRole.super_admin,
)
_write_company = require_company_scoped(UserRole.company_admin, UserRole.super_admin)
_write_units = require_company_scoped(
    UserRole.company_admin,
    UserRole.manager,
    UserRole.super_admin,
)
_delete_unit = require_company_scoped(UserRole.company_admin, UserRole.super_admin)


@router.post("/onboarding", response_model=OnboardingResponse, status_code=status.HTTP_201_CREATED)
async def onboard_company(
    body: OnboardCompanyBody,
    use_case: Annotated[OnboardCompanyUseCase, Depends(get_onboard_company_use_case)],
    tokens: Annotated[PyJwtTokenProvider, Depends(get_jwt_token_provider)],
) -> OnboardingResponse:
    try:
        result = await use_case.execute(
            legal_name=body.legal_name,
            trade_name=body.trade_name,
            document_number=body.document_number,
            company_email=str(body.company_email) if body.company_email else None,
            company_phone=body.company_phone,
            website=body.website,
            timezone=body.timezone,
            currency=body.currency,
            admin_full_name=body.admin_full_name,
            admin_email=str(body.admin_email),
            admin_password=body.admin_password,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Violação de unicidade (ex.: documento já cadastrado)",
        ) from e
    admin = result.admin_user
    assert admin.id is not None
    assert result.company.id is not None
    access_token = tokens.create_access_token(
        user_id=admin.id,
        role=admin.role.value,
        company_id=result.company.id,
    )
    return OnboardingResponse(
        access_token=access_token,
        company=company_to_public(result.company),
        user=user_to_public(admin),
    )


@router.get("/me", response_model=CompanyPublic)
async def get_my_company(
    user: Annotated[User, Depends(get_current_active_user)],
    use_case: Annotated[GetCompanyUseCase, Depends(get_get_company_use_case)],
) -> CompanyPublic:
    if user.company_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário não está vinculado a uma empresa",
        )
    company = await use_case.execute(user.company_id)
    if company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada")
    return company_to_public(company)


@router.get("", response_model=list[CompanyPublic])
async def list_companies(
    _admin: Annotated[User, Depends(require_roles(UserRole.super_admin))],
    use_case: Annotated[ListCompaniesUseCase, Depends(get_list_companies_use_case)],
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
) -> list[CompanyPublic]:
    rows = await use_case.execute(skip=skip, limit=limit)
    return [company_to_public(c) for c in rows]


@router.get("/{company_id}", response_model=CompanyPublic)
async def get_company(
    company_id: UUID,
    _user: Annotated[User, Depends(_read_tenant)],
    use_case: Annotated[GetCompanyUseCase, Depends(get_get_company_use_case)],
) -> CompanyPublic:
    company = await use_case.execute(company_id)
    if company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada")
    return company_to_public(company)


@router.patch("/{company_id}", response_model=CompanyPublic)
async def patch_company(
    company_id: UUID,
    body: PatchCompanyBody,
    _user: Annotated[User, Depends(_write_company)],
    use_case: Annotated[UpdateCompanyUseCase, Depends(get_update_company_use_case)],
) -> CompanyPublic:
    if not body.model_fields_set:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Informe ao menos um campo para atualizar",
        )
    try:
        updated = await use_case.execute(
            company_id,
            legal_name=body.legal_name,
            trade_name=body.trade_name,
            document_number=body.document_number,
            email=str(body.email) if body.email is not None else None,
            phone=body.phone,
            website=body.website,
            timezone=body.timezone,
            currency=body.currency,
            status=body.status,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Violação de unicidade (ex.: documento já cadastrado)",
        ) from e
    return company_to_public(updated)


@router.get("/{company_id}/settings", response_model=CompanySettingsPublic)
async def get_company_settings(
    company_id: UUID,
    _user: Annotated[User, Depends(_read_tenant)],
    use_case: Annotated[GetCompanySettingsUseCase, Depends(get_get_company_settings_use_case)],
) -> CompanySettingsPublic:
    row = await use_case.execute(company_id)
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configurações não encontradas",
        )
    return settings_to_public(row)


@router.patch("/{company_id}/settings", response_model=CompanySettingsPublic)
async def patch_company_settings(
    company_id: UUID,
    body: PatchCompanySettingsBody,
    _user: Annotated[User, Depends(_write_company)],
    use_case: Annotated[
        UpdateCompanySettingsUseCase,
        Depends(get_update_company_settings_use_case),
    ],
) -> CompanySettingsPublic:
    if not body.model_fields_set:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Informe ao menos um campo para atualizar",
        )
    try:
        updated = await use_case.execute(
            company_id,
            booking_min_notice_minutes=body.booking_min_notice_minutes,
            booking_max_days_ahead=body.booking_max_days_ahead,
            cancellation_min_notice_minutes=body.cancellation_min_notice_minutes,
            reschedule_min_notice_minutes=body.reschedule_min_notice_minutes,
            allow_online_booking=body.allow_online_booking,
            allow_waitlist=body.allow_waitlist,
            require_payment_advance=body.require_payment_advance,
            default_slot_interval_minutes=body.default_slot_interval_minutes,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    return settings_to_public(updated)


@router.get("/{company_id}/units", response_model=list[UnitPublic])
async def list_units(
    company_id: UUID,
    _user: Annotated[User, Depends(_read_tenant)],
    use_case: Annotated[ListUnitsUseCase, Depends(get_list_units_use_case)],
) -> list[UnitPublic]:
    rows = await use_case.execute(company_id)
    return [unit_to_public(u) for u in rows]


@router.post("/{company_id}/units", response_model=UnitPublic, status_code=status.HTTP_201_CREATED)
async def create_unit(
    company_id: UUID,
    body: CreateUnitBody,
    _user: Annotated[User, Depends(_write_units)],
    use_case: Annotated[CreateUnitUseCase, Depends(get_create_unit_use_case)],
) -> UnitPublic:
    unit = await use_case.execute(
        company_id,
        name=body.name,
        email=str(body.email) if body.email else None,
        phone=body.phone,
        status=body.status or UnitStatus.active,
        zip_code=body.zip_code,
        state=body.state,
        city=body.city,
        district=body.district,
        street=body.street,
        number=body.number,
        complement=body.complement,
        latitude=body.latitude,
        longitude=body.longitude,
    )
    return unit_to_public(unit)


@router.get("/{company_id}/units/{unit_id}", response_model=UnitPublic)
async def get_unit(
    company_id: UUID,
    unit_id: UUID,
    _user: Annotated[User, Depends(_read_tenant)],
    use_case: Annotated[GetUnitUseCase, Depends(get_get_unit_use_case)],
) -> UnitPublic:
    unit = await use_case.execute(company_id, unit_id)
    if unit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unidade não encontrada")
    return unit_to_public(unit)


@router.patch("/{company_id}/units/{unit_id}", response_model=UnitPublic)
async def patch_unit(
    company_id: UUID,
    unit_id: UUID,
    body: PatchUnitBody,
    _user: Annotated[User, Depends(_write_units)],
    use_case: Annotated[UpdateUnitUseCase, Depends(get_update_unit_use_case)],
) -> UnitPublic:
    if not body.model_fields_set:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Informe ao menos um campo para atualizar",
        )
    try:
        updated = await use_case.execute(
            company_id,
            unit_id,
            name=body.name,
            email=str(body.email) if body.email is not None else None,
            phone=body.phone,
            status=body.status,
            zip_code=body.zip_code,
            state=body.state,
            city=body.city,
            district=body.district,
            street=body.street,
            number=body.number,
            complement=body.complement,
            latitude=body.latitude,
            longitude=body.longitude,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    return unit_to_public(updated)


@router.delete("/{company_id}/units/{unit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_unit(
    company_id: UUID,
    unit_id: UUID,
    _user: Annotated[User, Depends(_delete_unit)],
    use_case: Annotated[UpdateUnitUseCase, Depends(get_update_unit_use_case)],
) -> None:
    try:
        await use_case.execute(company_id, unit_id, status=UnitStatus.inactive)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
