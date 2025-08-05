"""Script to run database migrations"""
from alembic.config import Config
from alembic import command
import os
import sys

def main():
    # Get the directory containing this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create Alembic configuration
    alembic_cfg = Config(os.path.join(current_dir, "alembic.ini"))
    
    try:
        # Run the migration
        command.upgrade(alembic_cfg, "head")
        print("Migration completed successfully!")
    except Exception as e:
        print(f"Error running migration: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
