"""create posts table

Revision ID: b018e6182c95
Revises: 
Create Date: 2022-09-24 20:19:00.520670

"""
from math import fabs
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b018e6182c95'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True)
    , sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
