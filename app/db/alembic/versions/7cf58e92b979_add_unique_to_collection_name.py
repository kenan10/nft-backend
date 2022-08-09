"""add unique to collection name

Revision ID: 7cf58e92b979
Revises: 38e7a650866a
Create Date: 2022-08-09 22:29:07.512921

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7cf58e92b979'
down_revision = '38e7a650866a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'collection', ['name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'collection', type_='unique')
    # ### end Alembic commands ###
