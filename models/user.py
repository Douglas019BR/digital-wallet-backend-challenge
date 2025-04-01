from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from config.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    is_admin = Column(Boolean, default=False)  # for future features
    is_active = Column(Boolean, default=True)  # for future features
    parent_id = Column(Integer, nullable=True)  # for future features
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    wallets = relationship(
        "Wallet",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="joined",
    )

    destination_transactions = relationship(
        "HistoryTransaction",
        back_populates="destination_user",
        foreign_keys="HistoryTransaction.destination_user_id",
        lazy="joined",
    )
    source_transactions = relationship(
        "HistoryTransaction",
        foreign_keys="HistoryTransaction.source_user_id",
        back_populates="source_user",
        lazy="joined",
    )
