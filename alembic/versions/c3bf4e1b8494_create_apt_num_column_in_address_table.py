"""create apt_num column in address table

Revision ID: c3bf4e1b8494
Revises: 5e2b6e907cc5
Create Date: 2023-04-07 15:08:09.778879

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3bf4e1b8494'
down_revision = '5e2b6e907cc5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('address', sa.Column('apt_num', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('address', 'apt_num')
