from datetime import datetime, timedelta, timezone

from models.history_transactions import HistoryTransaction, TransactionType


def test_get_transactions_unauthorized(test_client):
    response = test_client.get("/users/me/transactions")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_get_transactions_success(
    test_client, valid_token, db_session, test_user
):
    test_transaction = HistoryTransaction(
        source_user_id=test_user.id,
        wallet_id=test_user.wallets[0].id,
        amount=100.0,
        transaction_type=TransactionType.DEPOSIT,
    )
    db_session.add(test_transaction)
    db_session.commit()

    try:
        response = test_client.get(
            "/users/me/transactions",
            headers={"Authorization": f"Bearer {valid_token}"},
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) > 0
    finally:
        db_session.delete(test_transaction)
        db_session.commit()


def test_get_transactions_by_type(
    test_client, valid_token, db_session, test_user
):
    deposit_transaction = HistoryTransaction(
        source_user_id=test_user.id,
        wallet_id=test_user.wallets[0].id,
        amount=100.0,
        transaction_type=TransactionType.DEPOSIT,
    )
    transfer_transaction = HistoryTransaction(
        source_user_id=test_user.id,
        wallet_id=test_user.wallets[0].id,
        amount=50.0,
        transaction_type=TransactionType.TRANSFER,
    )

    db_session.add(deposit_transaction)
    db_session.add(transfer_transaction)
    db_session.commit()

    try:
        transaction_type = TransactionType.DEPOSIT
        response = test_client.get(
            f"/users/me/transactions?transaction_type={transaction_type}",
            headers={"Authorization": f"Bearer {valid_token}"},
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        for transaction in response.json():
            assert transaction["transaction_type"] == transaction_type
    finally:
        db_session.delete(deposit_transaction)
        db_session.delete(transfer_transaction)
        db_session.commit()


def test_get_transactions_by_date_range(
    test_client, valid_token, db_session, test_user
):
    now = datetime.now(timezone.utc)
    old_transaction = HistoryTransaction(
        source_user_id=test_user.id,
        wallet_id=test_user.wallets[0].id,
        amount=200.0,
        transaction_type=TransactionType.DEPOSIT,
        created_at=now - timedelta(days=60),
    )
    recent_transaction = HistoryTransaction(
        source_user_id=test_user.id,
        wallet_id=test_user.wallets[0].id,
        amount=150.0,
        transaction_type=TransactionType.DEPOSIT,
        created_at=now - timedelta(days=15),
    )

    db_session.add(old_transaction)
    db_session.add(recent_transaction)
    db_session.commit()

    try:
        end_date = now.isoformat()
        start_date = (now - timedelta(days=30)).isoformat()

        response = test_client.get(
            f"/users/me/transactions?start_date={start_date}&end_date={end_date}",
            headers={"Authorization": f"Bearer {valid_token}"},
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)

        transaction_ids = [t["id"] for t in response.json()]
        if transaction_ids:
            assert recent_transaction.id in transaction_ids
            assert old_transaction.id not in transaction_ids
    finally:
        db_session.delete(old_transaction)
        db_session.delete(recent_transaction)
        db_session.commit()


def test_get_transactions_combined_filters(
    test_client, valid_token, db_session, test_user
):
    now = datetime.now(timezone.utc)

    old_deposit = HistoryTransaction(
        source_user_id=test_user.id,
        wallet_id=test_user.wallets[0].id,
        amount=100.0,
        transaction_type=TransactionType.DEPOSIT,
        created_at=now - timedelta(days=60),
    )
    recent_deposit = HistoryTransaction(
        source_user_id=test_user.id,
        wallet_id=test_user.wallets[0].id,
        amount=200.0,
        transaction_type=TransactionType.DEPOSIT,
        created_at=now - timedelta(days=15),
    )
    recent_transfer = HistoryTransaction(
        source_user_id=test_user.id,
        wallet_id=test_user.wallets[0].id,
        amount=50.0,
        transaction_type=TransactionType.TRANSFER,
        created_at=now - timedelta(days=10),
    )

    db_session.add(old_deposit)
    db_session.add(recent_deposit)
    db_session.add(recent_transfer)
    db_session.commit()

    try:
        transaction_type = TransactionType.TRANSFER
        end_date = now.isoformat()
        start_date = (now - timedelta(days=30)).isoformat()

        response = test_client.get(
            f"/users/me/transactions?transaction_type={transaction_type}&start_date={start_date}&end_date={end_date}",
            headers={"Authorization": f"Bearer {valid_token}"},
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)

        for transaction in response.json():
            assert transaction["transaction_type"] == transaction_type
    finally:
        db_session.delete(old_deposit)
        db_session.delete(recent_deposit)
        db_session.delete(recent_transfer)
        db_session.commit()


def test_get_transactions_invalid_date_format(test_client, valid_token):
    response = test_client.get(
        "/users/me/transactions?start_date=invalid-date",
        headers={"Authorization": f"Bearer {valid_token}"},
    )
    assert response.status_code == 422


def test_get_transactions_invalid_type(test_client, valid_token):
    response = test_client.get(
        "/users/me/transactions?transaction_type=99",
        headers={"Authorization": f"Bearer {valid_token}"},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 0
