from services.user_service import get_user_by_email_service


def test_get_users_unauthorized(test_client):
    """Test fetching users without authorization."""
    response = test_client.get("/users/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_get_users_success(test_client, valid_token):
    """Test fetching users with valid token."""
    response = test_client.get(
        "/users/",
        headers={"Authorization": f"Bearer {valid_token}"},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


def test_get_user_not_found(test_client, valid_token):
    """Test fetching a non-existent user."""
    response = test_client.get(
        "/users/9999",
        headers={"Authorization": f"Bearer {valid_token}"},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_get_user_success(test_client, valid_token, test_user):
    """Test fetching an existing user."""
    response = test_client.get(
        f"/users/{test_user.id}",
        headers={"Authorization": f"Bearer {valid_token}"},
    )
    assert response.status_code == 200
    assert response.json()["id"] == test_user.id
    assert response.json()["username"] == test_user.username


def test_create_user_success(test_client, valid_token, db_session):
    """Test creating a new user."""
    body = {
        "username": "test1",
        "password": "test1passwd",
        "email": "test1@user.com",
    }
    response = test_client.post(
        "/users/",
        headers={"Authorization": f"Bearer {valid_token}"},
        json=body,
    )
    assert response.status_code == 201
    assert response.json()["username"] == body["username"]
    assert response.json()["email"] == body["email"]

    user_instance = get_user_by_email_service(db_session, email=body["email"])
    assert user_instance is not None
    db_session.delete(user_instance)
    db_session.commit()


def test_create_user_invalid_email(test_client, valid_token):
    """Test creating a user with an invalid email."""
    body = {
        "username": "test2",
        "password": "test2passwd",
        "email": "invalid-email",
    }
    response = test_client.post(
        "/users/",
        headers={"Authorization": f"Bearer {valid_token}"},
        json=body,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid email format"


def test_create_user_username_taken(test_client, valid_token, test_user):
    """Test creating a user with an already taken username."""
    body = {
        "username": test_user.username,
        "email": "testuser123@example.com",
        "password": "testpassword",
    }
    response = test_client.post(
        "/users/",
        headers={"Authorization": f"Bearer {valid_token}"},
        json=body,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already taken"


def test_create_user_email_taken(test_client, valid_token, test_user):
    """Test creating a user with an already taken email."""
    body = {
        "username": "test3",
        "email": test_user.email,
        "password": "test3passwd",
    }
    response = test_client.post(
        "/users/",
        headers={"Authorization": f"Bearer {valid_token}"},
        json=body,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_create_user_missing_args(test_client, valid_token):
    """Test creating a user with missing arguments."""
    body = {}
    response = test_client.post(
        "/users/",
        headers={"Authorization": f"Bearer {valid_token}"},
        json=body,
    )
    assert response.status_code == 422
