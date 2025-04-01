from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from config.database import get_db
from controllers.auth_controller import get_current_user
from schemas.transaction_schema import TransactionResponse
from schemas.user_schema import UserCreate, UserResponse
from services.user_service import (create_user_service, get_user_service,
                                   get_user_transactions_service,
                                   get_users_service)

user_router = APIRouter()


@user_router.post("/", response_model=UserResponse, status_code=201)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        new_user = create_user_service(db=db, user=user_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return new_user


@user_router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    user = get_user_service(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.get("/", response_model=list[UserResponse])
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    users = get_users_service(db=db, skip=skip, limit=limit)
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users


@user_router.get("/me/transactions", response_model=list[TransactionResponse])
def get_user_transactions(
    transaction_type: Optional[int] = Query(
        None,
        description="Filter by transaction type: 0=deposit, 1=withdraw, 2=transfer",
    ),
    start_date: Optional[datetime] = Query(
        None, description="Filter by start date (ISO format)"
    ),
    end_date: Optional[datetime] = Query(
        None, description="Filter by end date (ISO format)"
    ),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        transactions = get_user_transactions_service(
            db=db,
            user_id=current_user.id,
            transaction_type=transaction_type,
            start_date=start_date,
            end_date=end_date,
        )

        return transactions
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
