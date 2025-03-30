from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from config.database import get_db
from controllers.auth_controller import get_current_user
from models.user import User
from schemas.wallet_schema import (BalanceResponse, DepositRequest,
                                   TransferRequest, WalletResponse)
from services.wallet_service import (add_balance_service, get_wallet_service,
                                     transfer_balance_service)

router = APIRouter()


@router.get("/{wallet_id}/balance", response_model=BalanceResponse)
def get_wallet_balance(
    wallet_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    wallet = get_wallet_service(db, wallet_id)
    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Wallet not found"
        )

    if wallet.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this wallet",
        )
    message = "Balance :  "
    return BalanceResponse(message=message, balance=wallet.balance)


@router.post("/{wallet_id}/add-balance", response_model=BalanceResponse)
def add_balance(
    wallet_id: int,
    deposit_data: DepositRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        if deposit_data.amount <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Amount must be greater than zero",
            )

        wallet = add_balance_service(
            db, wallet_id, current_user, deposit_data.amount
        )
        message = "The new balance is "

        return BalanceResponse(message=message, balance=wallet.balance)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.post("/{source_wallet_id}/transfer", response_model=BalanceResponse)
def transfer_balance(
    source_wallet_id: int,
    transfer_data: TransferRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        message = transfer_balance_service(
            db=db,
            source_wallet_id=source_wallet_id,
            destination_wallet_id=transfer_data.destination_wallet_id,
            current_user=current_user,
            amount=transfer_data.amount,
        )

        wallet = get_wallet_service(db, source_wallet_id)

        return BalanceResponse(message=message, balance=wallet.balance)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
