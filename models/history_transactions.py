# from datetime import datetime

# from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship

# from config.database import Base


# class HistoryTransaction(Base):
#     __tablename__ = "history_transactions"

#     id = Column(Integer, primary_key=True, index=True)
#     wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=False)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     source_user_id = Column(
#         Integer, ForeignKey("users.id"), nullable=True
#     )  # Nullable for deposits and withdraw
#     transaction_type = Column(
#         String, nullable=False
#     )  # 'deposit', 'withdraw', or 'transfer'
#     amount = Column(Float, nullable=False)
#     created_at = Column(DateTime, default=datetime.utcnow)

#     wallet = relationship("Wallet", back_populates="history_transactions")
#     user = relationship(
#         "User", foreign_keys=[user_id], back_populates="history_transactions"
#     )
#     source_user = relationship("User", foreign_keys=[source_user_id])
