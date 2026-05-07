"""add_user_profile_fields

Revision ID: 16913dd34141
Revises: 21073476d040
Create Date: 2026-05-07 23:08:56.975761

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '16913dd34141'
down_revision: Union[str, Sequence[str], None] = '21073476d040'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('user', sa.Column('nickname', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.add_column('user', sa.Column('avatar_url', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.add_column('user', sa.Column('bio', sqlmodel.sql.sqltypes.AutoString(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('user', 'bio')
    op.drop_column('user', 'avatar_url')
    op.drop_column('user', 'nickname')
