from datetime import datetime

from pydantic import BaseModel


class WalletBase(BaseModel):
    user_id: int
    balance: int
    currency: str = "BRL"


class WalletCreate(WalletBase):
    pass


class WalletResponse(WalletBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True
        json_encoders = {datetime: lambda dt: dt.isoformat() if dt else None}
