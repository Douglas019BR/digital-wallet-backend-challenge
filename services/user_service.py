import re

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from models.user import User
from schemas.user_schema import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def is_valid_email(email: str) -> bool:
    """Validate email format."""
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_regex, email) is not None


def get_password_hash(password: str) -> str:
    """Hash a password for storing in the database."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify that a plain password matches the stored hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


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
    hashed_password = get_password_hash(user.password)
    if not is_valid_email(user.email):
        raise ValueError("Invalid email format")
    if get_user_by_email_service(db, user.email):
        raise ValueError("Email already registered")
    if get_user_by_username_service(db, user.username):
        raise ValueError("Username already taken")

    db_user = User(
        email=user.email,
        username=user.username,
        password=hashed_password,
        is_admin=user.is_admin if user.is_admin else False,
        is_active=user.is_active if user.is_active else True,
        parent_id=user.parent_id if user.parent_id else None,
    )
    if not db_user:
        raise ValueError("Invalid user data")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
