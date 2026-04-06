from pydantic import BaseModel, Field


class UpdateProfileBody(BaseModel):
    full_name: str | None = Field(None, min_length=1, max_length=180)
    phone: str | None = Field(None, max_length=30)
    avatar_url: str | None = Field(None, max_length=255)
