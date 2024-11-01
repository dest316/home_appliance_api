"""database creation

Revision ID: 4d91389a33e7
Revises: 
Create Date: 2024-10-23 01:11:05.725641

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d91389a33e7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cities',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('products',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('price', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stores',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('address', sa.String(), nullable=False),
                    sa.Column('city_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['city_id'], ['cities.id'], ),
                    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trades',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('date', sa.TIMESTAMP(), nullable=False),
                    sa.Column('store_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ),
                    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trades_products',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('trade_id', sa.Integer(), nullable=True),
                    sa.Column('product_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
                    sa.ForeignKeyConstraint(['trade_id'], ['trades.id'], ),
                    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('trades_products')
    op.drop_table('trades')
    op.drop_table('stores')
    op.drop_table('products')
    op.drop_table('cities')
    # ### end Alembic commands ###
