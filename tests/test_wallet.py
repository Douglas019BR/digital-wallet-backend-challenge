from services.wallet_service import get_wallet_service


def test_get_wallet_balance_unauthorized(test_client):
    """Test fetching wallet balance without authorization."""
    response = test_client.get("/wallets/1/balance")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_get_wallet_balance_not_found(test_client, valid_token):
    """Test fetching balance for a non-existent wallet."""
    response = test_client.get(
        "/wallets/9999/balance",
        headers={"Authorization": f"Bearer {valid_token}"},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Wallet not found"


def test_get_wallet_balance_forbidden(
    test_client, valid_token, db_session, test_user, test_another_user
):
    """Test fetching balance for a wallet that doesn't belong to the user."""
    other_wallet = get_wallet_service(
        db_session, test_another_user.wallets[0].id
    )

    response = test_client.get(
        f"/wallets/{other_wallet.id}/balance",
        headers={"Authorization": f"Bearer {valid_token}"},
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "You don't have access to this wallet"


def test_get_wallet_balance_success(
    test_client, valid_token, test_user, db_session
):
    """Test successfully fetching wallet balance."""
    wallet = get_wallet_service(db_session, test_user.wallets[0].id)

    response = test_client.get(
        f"/wallets/{wallet.id}/balance",
        headers={"Authorization": f"Bearer {valid_token}"},
    )
    assert response.status_code == 200
    assert "balance" in response.json()
    assert "message" in response.json()


def test_add_balance_unauthorized(test_client):
    response = test_client.post(
        "/wallets/1/add-balance", json={"amount": 100.0}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_add_balance_not_found(test_client, valid_token):
    """Test adding balance to a non-existent wallet."""
    response = test_client.post(
        "/wallets/9999/add-balance",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"amount": 100.0},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Wallet not found"


def test_add_balance_invalid_amount(
    test_client, valid_token, test_user, db_session
):
    wallet = get_wallet_service(db_session, test_user.wallets[0].id)
    response = test_client.post(
        f"/wallets/{wallet.id}/add-balance",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"amount": -100.0},
    )
    assert response.status_code == 422
    assert (
        "Input should be greater than 0" in response.json()["detail"][0]["msg"]
    )

    response = test_client.post(
        f"/wallets/{wallet.id}/add-balance",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"amount": 0.0},
    )
    assert response.status_code == 422
    assert (
        "Input should be greater than 0" in response.json()["detail"][0]["msg"]
    )


def test_add_balance_success(test_client, valid_token, test_user, db_session):
    wallet = get_wallet_service(db_session, test_user.wallets[0].id)
    initial_balance = wallet.balance
    amount_to_add = 100.0

    response = test_client.post(
        f"/wallets/{wallet.id}/add-balance",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"amount": amount_to_add},
    )

    assert response.status_code == 200
    assert response.json()["balance"] == initial_balance + amount_to_add

    wallet.balance = initial_balance
    db_session.commit()


def test_transfer_balance_unauthorized(test_client):
    response = test_client.post(
        "/wallets/1/transfer",
        json={"destination_wallet_id": 2, "amount": 50.0},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_transfer_balance_source_not_found(test_client, valid_token):
    response = test_client.post(
        "/wallets/9999/transfer",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"destination_wallet_id": 1, "amount": 50.0},
    )
    assert response.status_code == 400
    assert "Source wallet not found" in response.json()["detail"]


def test_transfer_balance_destination_not_found(
    test_client, valid_token, test_user, db_session
):
    wallet = get_wallet_service(db_session, test_user.wallets[0].id)

    response = test_client.post(
        f"/wallets/{wallet.id}/transfer",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"destination_wallet_id": 9999, "amount": 50.0},
    )
    assert response.status_code == 400
    assert "Destination wallet not found" in response.json()["detail"]


def test_transfer_balance_insufficient_funds(
    test_client, valid_token, test_user, db_session, test_another_user
):
    source_wallet = get_wallet_service(db_session, test_user.wallets[0].id)
    dest_wallet = get_wallet_service(
        db_session, test_another_user.wallets[0].id
    )
    source_wallet.balance = 10.0
    db_session.commit()
    response = test_client.post(
        f"/wallets/{source_wallet.id}/transfer",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"destination_wallet_id": dest_wallet.id, "amount": 100.0},
    )

    assert response.status_code == 400
    assert "Insufficient balance for transfer" in response.json()["detail"]


def test_transfer_balance_same_wallet(
    test_client, valid_token, test_user, db_session
):
    wallet = get_wallet_service(db_session, test_user.wallets[0].id)

    response = test_client.post(
        f"/wallets/{wallet.id}/transfer",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"destination_wallet_id": wallet.id, "amount": 50.0},
    )
    assert response.status_code == 400
    assert "Cannot transfer to the same wallet" in response.json()["detail"]


def test_transfer_balance_success(
    test_client, valid_token, test_user, db_session, test_another_user
):
    source_wallet = get_wallet_service(db_session, test_user.wallets[0].id)

    initial_balance = 200.0
    source_wallet.balance = initial_balance
    db_session.commit()

    dest_wallet = get_wallet_service(
        db_session, test_another_user.wallets[0].id
    )

    initial_dest_balance = dest_wallet.balance
    transfer_amount = 50.0

    response = test_client.post(
        f"/wallets/{source_wallet.id}/transfer",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={
            "destination_wallet_id": dest_wallet.id,
            "amount": transfer_amount,
        },
    )

    assert response.status_code == 200
    assert response.json()["balance"] == initial_balance - transfer_amount

    db_session.refresh(dest_wallet)
    assert dest_wallet.balance == initial_dest_balance + transfer_amount
