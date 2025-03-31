import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from config.database import get_db
from main import app
from schemas.user_schema import UserCreate
from services.user_service import (create_user_service,
                                   get_user_by_username_service)


@pytest.fixture
def db_session():
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def test_client():
    """Fixture to provide a test client for FastAPI app."""
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def test_user():
    """Fixture to create and delete a test user."""
    db: Session = next(get_db())
    existing_user = get_user_by_username_service(db, username="testuser")
    if existing_user:
        yield existing_user
    else:
        test_user_data = UserCreate(
            username="testuser",
            email="testuser@example.com",
            password="testpassword",
            is_admin=False,
            is_active=True,
        )
        test_user = create_user_service(db=db, user=test_user_data)
        yield test_user


@pytest.fixture(scope="module")
def valid_token(test_client, test_user):
    """Fixture to provide a valid token for authentication."""
    response = test_client.post(
        "/login/",
        json={"username": test_user.username, "password": "testpassword"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture(scope="module")
def test_another_user():
    """Fixture to create and delete a test user."""
    db: Session = next(get_db())
    existing_user = get_user_by_username_service(
        db, username="anothertestuser"
    )
    if existing_user:
        yield existing_user
    else:
        test_user_data = UserCreate(
            username="anothertestuser",
            email="anothertestuser@example.com",
            password="testpassword",
            is_admin=False,
            is_active=True,
        )
        test_user = create_user_service(db=db, user=test_user_data)
        yield test_user
