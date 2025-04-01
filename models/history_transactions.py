import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from config.database import Base


class TransactionType(enum.IntEnum):
    DEPOSIT = 0
    WITHDRAW = 1
    TRANSFER = 2

    @classmethod
    def as_str(cls, value):
        """Convert enum value to readable string"""
        mapping = {
            cls.DEPOSIT: "deposit",
            cls.WITHDRAW: "withdraw",
            cls.TRANSFER: "transfer",
        }
        return mapping.get(value, "unknown")


class HistoryTransaction(Base):
    __tablename__ = "history_transactions"

    id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=False)
    source_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    destination_user_id = Column(
        Integer, ForeignKey("users.id"), nullable=True
    )  # Nullable for deposits and withdraw
    transaction_type = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    wallet = relationship("Wallet", back_populates="history_transactions")
    destination_user = relationship(
        "User",
        foreign_keys=[destination_user_id],
        back_populates="destination_transactions",
    )
    source_user = relationship(
        "User",
        foreign_keys=[source_user_id],
        back_populates="source_transactions",
    )

    @property
    def transaction_type_name(self):
        """Return the string representation of the transaction type"""
        return TransactionType.as_str(self.transaction_type)
