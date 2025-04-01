from datetime import datetime, timedelta

from models.history_transactions import TransactionType


def test_get_transactions_unauthorized(test_client):
    response = test_client.get("/users/me/transactions")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


# def test_get_transactions_success(test_client, valid_token, db_session, test_user):
#     response = test_client.get(
#         "/users/me/transactions",
#         headers={"Authorization": f"Bearer {valid_token}"},
#     )
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)


# def test_get_transactions_by_type(test_client, valid_token, db_session, test_user):
#     """Test fetching transactions filtered by type."""
#     transaction_type = TransactionType.DEPOSIT
#     response = test_client.get(
#         f"/users/me/transactions?transaction_type={transaction_type}",
#         headers={"Authorization": f"Bearer {valid_token}"},
#     )
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)

#     # Verify all returned transactions are of the requested type
#     for transaction in response.json():
#         assert transaction["transaction_type"] == transaction_type


# def test_get_transactions_by_date_range(test_client, valid_token, db_session, test_user):
#     """Test fetching transactions filtered by date range."""
#     end_date = datetime.now().isoformat()
#     start_date = (datetime.now() - timedelta(days=30)).isoformat()

#     response = test_client.get(
#         f"/users/me/transactions?start_date={start_date}&end_date={end_date}",
#         headers={"Authorization": f"Bearer {valid_token}"},
#     )
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)


# def test_get_transactions_combined_filters(test_client, valid_token, db_session, test_user):
#     """Test fetching transactions with combined filters (type and date range)."""
#     transaction_type = TransactionType.TRANSFER
#     end_date = datetime.now().isoformat()
#     start_date = (datetime.now() - timedelta(days=30)).isoformat()

#     response = test_client.get(
#         f"/users/me/transactions?transaction_type={transaction_type}&start_date={start_date}&end_date={end_date}",
#         headers={"Authorization": f"Bearer {valid_token}"},
#     )
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)

#     # Verify all returned transactions are of the requested type
#     for transaction in response.json():
#         assert transaction["transaction_type"] == transaction_type


def test_get_transactions_invalid_date_format(test_client, valid_token):
    """Test fetching transactions with invalid date format."""
    response = test_client.get(
        "/users/me/transactions?start_date=invalid-date",
        headers={"Authorization": f"Bearer {valid_token}"},
    )
    assert response.status_code == 422  # Validation error


def test_get_transactions_invalid_type(test_client, valid_token):
    """Test fetching transactions with invalid transaction type."""
    response = test_client.get(
        "/users/me/transactions?transaction_type=99",  # Invalid type
        headers={"Authorization": f"Bearer {valid_token}"},
    )
    assert (
        response.status_code == 200
    )  # Should still work but return no results
    assert isinstance(response.json(), list)
    assert len(response.json()) == 0
