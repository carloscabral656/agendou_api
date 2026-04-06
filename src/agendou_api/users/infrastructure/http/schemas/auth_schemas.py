from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class RegisterBody(BaseModel):
    company_id: UUID
    full_name: str = Field(..., min_length=1, max_length=180)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class LoginBody(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1, max_length=128)
    company_id: UUID | None = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ForgotPasswordBody(BaseModel):
    email: EmailStr
    company_id: UUID | None = None


class ForgotPasswordResponse(BaseModel):
    message: str = (
        "Se o e-mail existir em nossa base, você receberá instruções para redefinir a senha."
    )


class ResetPasswordBody(BaseModel):
    token: str = Field(..., min_length=10)
    new_password: str = Field(..., min_length=8, max_length=128)
