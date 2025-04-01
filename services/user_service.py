import re
from datetime import datetime

import bcrypt
from sqlalchemy import or_
from sqlalchemy.orm import Session

from models.history_transactions import HistoryTransaction, TransactionType
from models.user import User
from schemas.user_schema import UserCreate
from services.wallet_service import create_wallet_service


def is_valid_email(email: str) -> bool:
    """Validate email format."""
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_regex, email) is not None


def get_password_hash(password: str) -> str:
    """Hash a password for storing in the database."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify that a plain password matches the stored hashed password."""
    return bcrypt.hashpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    ) == hashed_password.encode("utf-8")


def get_user_service(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email_service(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_by_username_service(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def get_users_service(
    db: Session, skip: int = 0, limit: int = 100
) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()


def create_user_service(db: Session, user: UserCreate) -> User:
    if not is_valid_email(user.email):
        raise ValueError("Invalid email format")
    if get_user_by_email_service(db, user.email):
        raise ValueError("Email already registered")
    if get_user_by_username_service(db, user.username):
        raise ValueError("Username already taken")

    hashed_password = get_password_hash(user.password)

    try:
        db_user = User(
            email=user.email,
            username=user.username,
            password=hashed_password,
            is_admin=user.is_admin if user.is_admin else False,
            is_active=user.is_active if user.is_active else True,
            parent_id=user.parent_id if user.parent_id else None,
        )

        db.add(db_user)
        db.flush()

        wallet_id = create_wallet_service(db, db_user.id)
        if not wallet_id:
            raise ValueError("Failed to create wallet")

        db.commit()
        db.refresh(db_user)
        return db_user

    except Exception as err:
        db.rollback()
        raise err


def get_user_transactions_service(
    db: Session,
    user_id: int,
    transaction_type: int = None,
    start_date: datetime = None,
    end_date: datetime = None,
) -> list[dict]:
    query = db.query(HistoryTransaction).filter(
        or_(
            HistoryTransaction.source_user_id == user_id,
            HistoryTransaction.destination_user_id == user_id,
        )
    )

    if transaction_type is not None:
        query = query.filter(
            HistoryTransaction.transaction_type == transaction_type
        )

    if start_date:
        query = query.filter(HistoryTransaction.created_at >= start_date)

    if end_date:
        query = query.filter(HistoryTransaction.created_at <= end_date)

    transactions = query.order_by(HistoryTransaction.created_at.desc()).all()

    result = []
    for transaction in transactions:
        transaction_dict = {
            "id": transaction.id,
            "transaction_type": transaction.transaction_type,
            "amount": transaction.amount,
            "source_user_id": transaction.source_user_id,
            "destination_user_id": transaction.destination_user_id,
            "created_at": transaction.created_at,
            "is_receiver": (
                transaction.transaction_type == TransactionType.TRANSFER
                and transaction.destination_user_id == user_id
            ),
        }
        result.append(transaction_dict)

    return result
