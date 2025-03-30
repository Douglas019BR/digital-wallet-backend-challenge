import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.database import SessionLocal
from schemas.user_schema import UserCreate
from services.user_service import (create_user_service,
                                   get_user_by_email_service)


def create_admin_user():
    db = SessionLocal()
    try:
        admin_email = "admin@example.com"
        existing_admin = get_user_by_email_service(db=db, email=admin_email)

        if existing_admin:
            print(f"Admin user already exists with email: {admin_email}")
            return

        admin_data = UserCreate(
            username="admin",
            email=admin_email,
            password="adminpass123",
            is_admin=True,
            is_active=True,
        )

        admin_user = create_user_service(db=db, user=admin_data)
        print(f"Admin user created successfully with ID: {admin_user.id}")

    except Exception as e:
        print(f"Error creating admin user: {str(e)}")
    finally:
        db.close()


def create_regular_user():
    db = SessionLocal()
    try:
        regular_email = "regular@example.com"
        existing_user = get_user_by_email_service(db=db, email=regular_email)
        if existing_user:
            print(f"Regular user already exists with email: {regular_email}")
            return
        regular_data = UserCreate(
            username="regular",
            email=regular_email,
            password="userpass123",
            is_admin=False,
            is_active=True,
        )
        regular_user = create_user_service(db=db, user=regular_data)
        print(f"Regular user created successfully with ID: {regular_user.id}")
    except Exception as e:
        print(f"Error creating regular user: {str(e)}")
    finally:
        db.close()


if __name__ == "__main__":
    create_admin_user()
    create_regular_user()
