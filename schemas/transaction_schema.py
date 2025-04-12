from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TransactionResponse(BaseModel):
    id: int
    transaction_type: int
    transaction_type_name: str
    amount: float
    created_at: datetime
    wallet_id: int
    source_user_id: int
    destination_user_id: Optional[int] = None
    is_receiver: bool = False

    class ConfigDict:
        orm_mode = True
        json_encoders = {datetime: lambda dt: dt.isoformat() if dt else None}
