import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.database import SessionLocal
from schemas.user_schema import UserCreate
from services.user_service import (
    create_user_service,
    get_user_by_email_service,
)


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


if __name__ == "__main__":
    create_admin_user()
