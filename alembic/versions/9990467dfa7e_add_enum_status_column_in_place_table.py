"""add enum status column in place table

Revision ID: 9990467dfa7e
Revises: 508218d45c1e
Create Date: 2025-01-06 19:12:37.965627

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import ENUM

# revision identifiers, used by Alembic.
revision: str = "9990467dfa7e"
down_revision: Union[str, None] = "508218d45c1e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Создание Enum типа в PostgreSQL
    place_status_enum = ENUM('ACTIVE', 'INACTIVE', 'DISABLED', 'TESTING', name='placestatus')
    place_status_enum.create(op.get_bind(), checkfirst=True)

    # Добавление столбца с типом Enum
    op.add_column(
        "place",
        sa.Column(
            "status",
            place_status_enum,
            nullable=False,
            server_default='DISABLED',  # Устанавливаем значение по умолчанию
        ),
    )


def downgrade() -> None:
    # Удаляем столбец
    op.drop_column("place", "status")

    # Удаляем тип Enum
    place_status_enum = ENUM('ACTIVE', 'INACTIVE', 'DISABLED', 'TESTING', name='placestatus')
    place_status_enum.drop(op.get_bind(), checkfirst=True)
