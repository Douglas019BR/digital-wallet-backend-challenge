def test_login_success(test_client):
    """Test successful login."""
    response = test_client.post(
        "/login/",
        json={"username": "testuser", "password": "testpassword"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_failure(test_client):
    """Test login failure with incorrect credentials."""
    response = test_client.post(
        "/login/",
        json={"username": "testuser", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"
