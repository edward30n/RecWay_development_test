"""Add email_verified_at column to users table

This migration adds the email_verified_at column to track when users verify their email.
"""
from sqlalchemy import Column, DateTime
from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Añadir la columna email_verified_at
    op.add_column('users', sa.Column('email_verified_at', sa.DateTime(timezone=True), nullable=True))

def downgrade():
    # Eliminar la columna email_verified_at
    op.drop_column('users', 'email_verified_at')
