from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class HistoryTransactionBase(BaseModel):
    wallet_id: int
    user_id: int
    transaction_type: str  # 'deposit', 'withdraw', or 'transfer'
    amount: float
    source_user_id: Optional[int] = None


class HistoryTransactionCreate(HistoryTransactionBase):
    pass


class HistoryTransactionResponse(HistoryTransactionBase):
    id: int
    created_at: datetime | None = None

    class Config:
        orm_mode = True
        json_encoders = {datetime: lambda dt: dt.isoformat() if dt else None}
