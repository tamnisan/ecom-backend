"""empty message

Revision ID: 48d1db7c86e2
Revises: f4c4048f83fe
Create Date: 2026-06-25 22:50:17.871367

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '48d1db7c86e2'
down_revision: Union[str, Sequence[str], None] = 'f4c4048f83fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Rename the existing 'user' table (which holds product data) to 'product'
    op.rename_table('user', 'product')

    # 2. Create the brand new 'user' table for actual users
    op.create_table('user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('user_pincode', sa.Integer(), nullable=False),
        sa.Column('wallet', sa.Integer(), server_default=sa.text('0'), nullable=False),
        sa.Column('completed_order', sa.Integer(), server_default=sa.text('0'), nullable=False),
        sa.Column('pending_order', sa.Integer(), server_default=sa.text('0'), nullable=False),
        sa.Column('failed_order', sa.Integer(), server_default=sa.text('0'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )


def downgrade() -> None:
    # 1. Drop the newly created user table
    op.drop_table('user')

    # 2. Rename the 'product' table back to 'user'
    op.rename_table('product', 'user')