def test_get_users_unauthorized(test_client):
    """Test fetching users without authorization."""
    response = test_client.get("/users/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_get_user_not_found(test_client, valid_token):
    """Test fetching a non-existent user."""
    response = test_client.get(
        "/users/9999",
        headers={"Authorization": f"Bearer {valid_token}"},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"