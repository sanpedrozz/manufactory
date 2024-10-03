"""Remove cameras, place_camera_link tables and camera column from alarm_messages

Revision ID: 07a2be7f77f1
Revises: a9bf16e95025
Create Date: 2024-10-03 16:24:14.153718

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '07a2be7f77f1'
down_revision: Union[str, None] = 'a9bf16e95025'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('place_camera_link')
    op.drop_table('cameras')
    op.drop_column('alarm_messages', 'camera')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('alarm_messages', sa.Column('camera', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.create_table('cameras',
    sa.Column('id', sa.BIGINT(), server_default=sa.text("nextval('cameras_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('camera_info', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('comment', sa.TEXT(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='cameras_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('place_camera_link',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('place_id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('camera_id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['camera_id'], ['cameras.id'], name='place_camera_link_camera_id_fkey'),
    sa.ForeignKeyConstraint(['place_id'], ['places.id'], name='place_camera_link_place_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='place_camera_link_pkey')
    )
    # ### end Alembic commands ###