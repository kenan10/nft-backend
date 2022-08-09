"""add unique access list constraint

Revision ID: eae830bdf7fe
Revises: 9df310e3ab96
Create Date: 2022-08-09 21:55:53.861549

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eae830bdf7fe'
down_revision = '9df310e3ab96'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('unique_access_list', 'list', ['name', 'collection_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('unique_access_list', 'list', type_='unique')
    # ### end Alembic commands ###
