"""add constraint for token table

Revision ID: d4046659aef7
Revises: c2351807e53c
Create Date: 2022-08-09 09:26:25.330093

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4046659aef7'
down_revision = 'c2351807e53c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('unique_token', 'token', ['nft_id', 'collection_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('unique_token', 'token', type_='unique')
    # ### end Alembic commands ###