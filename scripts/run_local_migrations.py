import os
import subprocess
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def run_local_migrations():
    """Execute migrations on a local database connection."""
    # Store original DATABASE_URL
    original_db_url = os.environ.get("DATABASE_URL", "")
    
    try:
        # Set the DATABASE_URL to a local connection
        # Modify this to match your local database credentials
        os.environ["DATABASE_URL"] = "postgresql://postgres:password@localhost:5432/digital-wallet"
        
        print(f"Using local database connection: {os.environ['DATABASE_URL']}")
        
        # Run the migrations
        result = subprocess.run(["alembic", "upgrade", "head"], check=True)
        print("Migrations executed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing migrations: {e}")
        return False
    finally:
        # Restore original DATABASE_URL if there was one
        if original_db_url:
            os.environ["DATABASE_URL"] = original_db_url


if __name__ == "__main__":
    run_local_migrations()
