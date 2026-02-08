"""make kvk and wgp to floats

Revision ID: efd36060aa56
Revises: 1cd0f313040b
Create Date: 2026-02-08 12:30:32.534153

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'efd36060aa56'
down_revision: Union[str, Sequence[str], None] = '1cd0f313040b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Convert kvk_value from VARCHAR to FLOAT
    op.alter_column('order_positions', 'kvk_value',
        existing_type=sa.VARCHAR(),
        type_=sa.Float(),
        existing_nullable=True,
        postgresql_using='kvk_value::double precision',
    )

    # Convert wgp_value from VARCHAR to FLOAT
    op.alter_column('order_positions', 'wgp_value',
        existing_type=sa.VARCHAR(),
        type_=sa.Float(),
        existing_nullable=True,
        postgresql_using='wgp_value::double precision',
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Convert wgp_value back to VARCHAR
    op.alter_column('order_positions', 'wgp_value',
        existing_type=sa.Float(),
        type_=sa.VARCHAR(),
        existing_nullable=True,
        postgresql_using='wgp_value::text',
    )

    # Convert kvk_value back to VARCHAR
    op.alter_column('order_positions', 'kvk_value',
        existing_type=sa.Float(),
        type_=sa.VARCHAR(),
        existing_nullable=True,
        postgresql_using='kvk_value::text',
    )
