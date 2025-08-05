"""Script to run database migrations."""
import sys
import os
from pathlib import Path

# Añadir el directorio raíz al PYTHONPATH
root_dir = Path(__file__).parent.parent.parent
sys.path.append(str(root_dir))

from alembic import command
from alembic.config import Config
from app.db.alembic import config

def run_migrations():
    """Run all pending migrations."""
    try:
        command.upgrade(config, "head")
        print("Migrations completed successfully!")
    except Exception as e:
        print(f"Error running migrations: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_migrations()
