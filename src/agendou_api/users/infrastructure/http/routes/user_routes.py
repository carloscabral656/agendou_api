from fastapi import APIRouter, Depends, HTTPException, status

from agendou_api.users.infrastructure.http.controllers.user_controller import UserController
from agendou_api.users.infrastructure.http.dependencies import get_user_controller
from agendou_api.users.infrastructure.http.schemas.create_user import CreateUserBody, UserResponse

router = APIRouter(prefix="/users")


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    body: CreateUserBody,
    controller: UserController = Depends(get_user_controller),
) -> UserResponse:
    try:
        user = await controller.create_user(name=body.name, email=str(body.email))
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from e
    assert user.id is not None
    return UserResponse(id=user.id, name=user.name, email=user.email)
