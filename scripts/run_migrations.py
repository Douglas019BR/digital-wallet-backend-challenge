import os
import subprocess
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def run_migrations():
    """Execute as migrações do Alembic."""
    try:
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        print("Migrations executed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing migrations: {e}")
        return False


if __name__ == "__main__":
    run_migrations()
