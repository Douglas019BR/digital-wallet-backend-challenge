def test_login_success(test_client, test_user):
    response = test_client.post(
        "/login/",
        json={"username": test_user.username, "password": "testpassword"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_failure(test_client, test_user):
    response = test_client.post(
        "/login/",
        json={"username": test_user.username, "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"
