"""ref alarms tables

Revision ID: 6e532912dad1
Revises: e4f98c623c8c
Create Date: 2024-12-26 16:29:22.918075

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "6e532912dad1"
down_revision: Union[str, None] = "e4f98c623c8c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Удаляем внешние ключи
    op.drop_constraint('operations_history_place_id_fkey', 'operations_history', type_='foreignkey')
    op.drop_constraint('alarm_history_place_id_fkey', 'alarm_history', type_='foreignkey')
    op.drop_constraint('alarm_history_alarm_id_fkey', 'alarm_history', type_='foreignkey')

    # Удаляем таблицы
    op.drop_table("operations_history")
    op.drop_table("plc_data")
    op.drop_table("alarm_history")
    op.drop_table("alarm_messages")
    op.drop_table("places")


def downgrade() -> None:
    # Восстанавливаем таблицы
    op.create_table(
        "places",
        sa.Column("id", sa.BIGINT(), autoincrement=True, nullable=False),
        sa.Column("name", sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column(
            "message_thread_id",
            sa.VARCHAR(),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "ip", sa.VARCHAR(length=45), autoincrement=False, nullable=True
        ),
        sa.PrimaryKeyConstraint("id", name="places_pkey"),
    )
    op.create_table(
        "alarm_messages",
        sa.Column("id", sa.BIGINT(), autoincrement=True, nullable=False),
        sa.Column("message", sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column("tag", sa.TEXT(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name="alarm_messages_pkey"),
    )
    op.create_table(
        "alarm_history",
        sa.Column("id", sa.BIGINT(), autoincrement=True, nullable=False),
        sa.Column(
            "place_id", sa.BIGINT(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "alarm_id", sa.BIGINT(), autoincrement=False, nullable=False
        ),
        sa.Column("comments", sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column(
            "dt_created",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["alarm_id"],
            ["alarm_messages.id"],
            name="alarm_history_alarm_id_fkey",
        ),
        sa.ForeignKeyConstraint(
            ["place_id"], ["places.id"], name="alarm_history_place_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="alarm_history_pkey"),
    )
    op.create_table(
        "plc_data",
        sa.Column("id", sa.BIGINT(), autoincrement=True, nullable=False),
        sa.Column(
            "dt_created",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("value", sa.TEXT(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="plc_data_pkey"),
    )
    op.create_table(
        "operations_history",
        sa.Column("id", sa.BIGINT(), autoincrement=True, nullable=False),
        sa.Column(
            "place_id", sa.INTEGER(), autoincrement=False, nullable=True
        ),
        sa.Column("program", sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column("text", sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column(
            "dt_created",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["place_id"],
            ["places.id"],
            name="operations_history_place_id_fkey",
        ),
        sa.PrimaryKeyConstraint("id", name="operations_history_pkey"),
    )
