from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from agendou_api.users.application.commands.update_profile_use_case import UpdateProfileUseCase
from agendou_api.users.domain.user import User
from agendou_api.users.infrastructure.http.dependencies import get_update_profile_use_case
from agendou_api.users.infrastructure.http.schemas.profile_schemas import UpdateProfileBody
from agendou_api.users.infrastructure.http.schemas.user_public import UserPublic, user_to_public
from agendou_api.users.infrastructure.http.security import get_current_active_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserPublic)
async def read_me(
    user: Annotated[User, Depends(get_current_active_user)],
) -> UserPublic:
    return user_to_public(user)


@router.patch("/me", response_model=UserPublic)
async def update_me(
    body: UpdateProfileBody,
    user: Annotated[User, Depends(get_current_active_user)],
    use_case: Annotated[UpdateProfileUseCase, Depends(get_update_profile_use_case)],
) -> UserPublic:
    if body.full_name is None and body.phone is None and body.avatar_url is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Informe ao menos um campo para atualizar",
        )
    assert user.id is not None
    try:
        updated = await use_case.execute(
            user_id=user.id,
            full_name=body.full_name,
            phone=body.phone,
            avatar_url=body.avatar_url,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    return user_to_public(updated)
