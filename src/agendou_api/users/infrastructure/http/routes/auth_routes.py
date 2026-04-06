from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from agendou_api.shared.infrastructure.security.pyjwt_token_provider import PyJwtTokenProvider
from agendou_api.users.application.commands.authenticate_user_use_case import (
    AmbiguousCompanyError,
    AuthenticateUserUseCase,
)
from agendou_api.users.application.commands.register_user_use_case import RegisterUserUseCase
from agendou_api.users.application.commands.request_password_reset_use_case import (
    RequestPasswordResetUseCase,
)
from agendou_api.users.application.commands.reset_password_use_case import ResetPasswordUseCase
from agendou_api.users.domain.enums import UserRole
from agendou_api.users.domain.user import User
from agendou_api.users.infrastructure.http.dependencies import (
    get_authenticate_user_use_case,
    get_jwt_token_provider,
    get_register_user_use_case,
    get_request_password_reset_use_case,
    get_reset_password_use_case,
)
from agendou_api.users.infrastructure.http.schemas.auth_schemas import (
    ForgotPasswordBody,
    ForgotPasswordResponse,
    LoginBody,
    RegisterBody,
    ResetPasswordBody,
    TokenResponse,
)
from agendou_api.users.infrastructure.http.schemas.user_public import UserPublic, user_to_public
from agendou_api.users.infrastructure.http.security import require_roles

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register(
    body: RegisterBody,
    use_case: Annotated[RegisterUserUseCase, Depends(get_register_user_use_case)],
) -> UserPublic:
    try:
        user = await use_case.execute(
            company_id=body.company_id,
            full_name=body.full_name,
            email=str(body.email),
            password=body.password,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="company_id inválido ou dados inconsistentes",
        ) from e
    return user_to_public(user)


@router.post("/login", response_model=TokenResponse)
async def login(
    body: LoginBody,
    use_case: Annotated[AuthenticateUserUseCase, Depends(get_authenticate_user_use_case)],
    tokens: Annotated[PyJwtTokenProvider, Depends(get_jwt_token_provider)],
) -> TokenResponse:
    try:
        user = await use_case.execute(
            email=str(body.email),
            password=body.password,
            company_id=body.company_id,
        )
    except AmbiguousCompanyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vários cadastros com este e-mail; informe company_id.",
        ) from e
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        ) from e
    assert user.id is not None
    access_token = tokens.create_access_token(
        user_id=user.id,
        role=user.role.value,
        company_id=user.company_id,
    )
    return TokenResponse(access_token=access_token)


@router.post("/forgot-password", response_model=ForgotPasswordResponse)
async def forgot_password(
    body: ForgotPasswordBody,
    use_case: Annotated[RequestPasswordResetUseCase, Depends(get_request_password_reset_use_case)],
) -> ForgotPasswordResponse:
    await use_case.execute(email=str(body.email), company_id=body.company_id)
    return ForgotPasswordResponse()


@router.post("/reset-password", status_code=status.HTTP_204_NO_CONTENT)
async def reset_password(
    body: ResetPasswordBody,
    use_case: Annotated[ResetPasswordUseCase, Depends(get_reset_password_use_case)],
) -> None:
    try:
        await use_case.execute(token=body.token, new_password=body.new_password)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout() -> None:
    """JWT é stateless: descarte o token no cliente. Este endpoint existe apenas para convenção."""
    return None


@router.get("/admin-only-example")
async def admin_only_example(
    _user: Annotated[User, Depends(require_roles(UserRole.company_admin, UserRole.super_admin))],
) -> dict[str, bool]:
    return {"ok": True}
