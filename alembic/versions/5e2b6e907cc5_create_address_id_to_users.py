"""create address_id to users

Revision ID: 5e2b6e907cc5
Revises: f052c5cd495f
Create Date: 2023-04-07 14:26:11.762351

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e2b6e907cc5'
down_revision = 'f052c5cd495f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('address_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'address_users_fk',
        source_table='users',
        referent_table='address',
        local_cols=['address_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    op.drop_constraint('address_users_fk', table_name='users')
    op.drop_column('users', 'address_id')
