"""add nullable false requirements for foregin keys

Revision ID: e7708affc878
Revises: 44a85411beed
Create Date: 2022-08-10 12:00:09.621220

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e7708affc878'
down_revision = '44a85411beed'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('list', 'list_type_id',
               existing_type=mysql.BIGINT(),
               nullable=False)
    op.alter_column('list', 'collection_id',
               existing_type=mysql.BIGINT(),
               nullable=False)
    op.alter_column('list_item', 'wallet_id',
               existing_type=mysql.BIGINT(),
               nullable=False)
    op.alter_column('list_item', 'list_id',
               existing_type=mysql.BIGINT(),
               nullable=False)
    op.alter_column('token', 'wallet_id',
               existing_type=mysql.BIGINT(),
               nullable=False)
    op.alter_column('token', 'collection_id',
               existing_type=mysql.BIGINT(),
               nullable=False)
    op.alter_column('token_detail', 'token_id',
               existing_type=mysql.BIGINT(),
               nullable=False)
    op.alter_column('token_detail', 'token_detail_type_id',
               existing_type=mysql.BIGINT(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('token_detail', 'token_detail_type_id',
               existing_type=mysql.BIGINT(),
               nullable=True)
    op.alter_column('token_detail', 'token_id',
               existing_type=mysql.BIGINT(),
               nullable=True)
    op.alter_column('token', 'collection_id',
               existing_type=mysql.BIGINT(),
               nullable=True)
    op.alter_column('token', 'wallet_id',
               existing_type=mysql.BIGINT(),
               nullable=True)
    op.alter_column('list_item', 'list_id',
               existing_type=mysql.BIGINT(),
               nullable=True)
    op.alter_column('list_item', 'wallet_id',
               existing_type=mysql.BIGINT(),
               nullable=True)
    op.alter_column('list', 'collection_id',
               existing_type=mysql.BIGINT(),
               nullable=True)
    op.alter_column('list', 'list_type_id',
               existing_type=mysql.BIGINT(),
               nullable=True)
    # ### end Alembic commands ###
