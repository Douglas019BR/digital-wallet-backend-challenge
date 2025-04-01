from sqlalchemy.orm import Session

from models.history_transactions import HistoryTransaction, TransactionType
from models.user import User
from models.wallet import Wallet


def get_wallet_service(db: Session, wallet_id: int) -> Wallet | None:
    return db.query(Wallet).filter(Wallet.id == wallet_id).first()


def create_wallet_service(
    db: Session, user_id: int, currency: str = "BRL"
) -> int:
    # It's necessary commit db after call it
    try:
        db_wallet = Wallet(
            user_id=user_id,
            balance=0.0,
            currency=currency,
        )
        db.add(db_wallet)
        db.flush()
        return db_wallet.id
    except Exception:
        return


def add_balance_service(
    db: Session, wallet_id: int, current_user: User, value: float
) -> Wallet:
    wallet = get_wallet_service(db, wallet_id)
    if not wallet:
        raise Exception("Wallet not found")
    if not wallet.user_id == current_user.id:
        raise Exception("This wallet doesn't belong to you")
    if value < 0:
        raise Exception("The value can't be less than zero")
    wallet.balance += value
    transaction = HistoryTransaction(
        wallet_id=wallet.id,
        source_user_id=current_user.id,
        transaction_type=TransactionType.DEPOSIT,
        amount=value,
    )
    db.add(transaction)
    db.commit()

    return wallet


def transfer_balance_service(
    db: Session,
    source_wallet_id: int,
    destination_wallet_id: int,
    current_user: User,
    amount: float,
) -> str:
    if amount <= 0:
        raise Exception("Transfer amount must be greater than zero")
    source_wallet = get_wallet_service(db, source_wallet_id)
    if not source_wallet:
        raise Exception("Source wallet not found")
    if source_wallet.user_id != current_user.id:
        raise Exception("Source wallet doesn't belong to you")
    if source_wallet.id == destination_wallet_id:
        raise Exception("Cannot transfer to the same wallet")
    if source_wallet.balance < amount:
        raise Exception("Insufficient balance for transfer")

    destination_wallet = get_wallet_service(db, destination_wallet_id)
    if not destination_wallet:
        raise Exception("Destination wallet not found")

    try:
        source_wallet.balance -= amount
        destination_wallet.balance += amount
        transaction = HistoryTransaction(
            wallet_id=source_wallet.id,
            source_user_id=current_user.id,
            destination_user_id=destination_wallet.user_id,
            transaction_type=TransactionType.TRANSFER,
            amount=amount,
        )
        db.add(transaction)
        db.commit()

        return f"Successfully transferred {amount} {source_wallet.currency}. New balance: {source_wallet.balance}"
    except Exception as err:
        db.rollback()
        raise Exception(f"Transfer failed: {str(err)}")
