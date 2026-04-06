from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status

from agendou_api.users.domain.enums import UserRole
from agendou_api.users.domain.user import User
from agendou_api.users.infrastructure.http.security import get_current_active_user


async def ensure_company_path_access(
    company_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> UUID:
    """Tenant users may only access their own company_id; super_admin may access any."""
    if current_user.role == UserRole.super_admin:
        return company_id
    if current_user.company_id is None or current_user.company_id != company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )
    return company_id


def require_company_scoped(*allowed: UserRole):
    """Require allowed role and tenant match on path company_id (super_admin skips match)."""

    async def _dep(
        company_id: UUID,
        user: Annotated[User, Depends(get_current_active_user)],
    ) -> User:
        if user.role not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        if user.role != UserRole.super_admin:
            if user.company_id is None or user.company_id != company_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Forbidden",
                )
        return user

    return _dep
