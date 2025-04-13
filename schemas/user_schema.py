from datetime import datetime

from pydantic import BaseModel, ValidationInfo, field_validator


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    username: str
    email: str
    password: str
    is_admin: bool = False
    is_active: bool = True
    parent_id: int | None = None

    @field_validator("username", "email", "password", mode="before")
    def validate_not_empty(cls, value, info: ValidationInfo):
        if not value or not str(value).strip():
            raise ValueError(
                f"The field '{info.field_name}' can not be empty."
            )
        return value


class UserResponse(UserBase):
    id: int
    email: str
    is_admin: bool
    is_active: bool
    parent_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True
        json_encoders = {datetime: lambda dt: dt.isoformat() if dt else None}
