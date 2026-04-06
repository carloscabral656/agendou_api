from pydantic import BaseModel

from agendou_api.companies.infrastructure.http.schemas.company_schemas import CompanyPublic
from agendou_api.users.infrastructure.http.schemas.user_public import UserPublic


class OnboardingResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    company: CompanyPublic
    user: UserPublic
