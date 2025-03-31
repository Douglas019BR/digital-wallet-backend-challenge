def test_login_success(test_client):
    """Test successful login."""
    retries = 0
    attempts = 3
    while retries < attempts:
        response = test_client.post(
            "/login/",
            json={"username": "testuser", "password": "testpassword"},
        )
        if response.status_code == 200:
            break
        else:
            print("Login failed, retrying...")
            retries += 1
            continue
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
