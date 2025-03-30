from datetime import datetime

from pydantic import BaseModel, Field


class WalletBase(BaseModel):
    user_id: int
    balance: float = 0.0
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


class DepositRequest(BaseModel):
    amount: float = Field(..., gt=0)


class TransferRequest(BaseModel):
    destination_wallet_id: int
    amount: float = Field(..., gt=0)


class BalanceResponse(BaseModel):
    message: str
    balance: float
