"""add content colum to posts table

Revision ID: 8044239483b3
Revises: b018e6182c95
Create Date: 2022-09-24 20:29:37.111811

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8044239483b3'
down_revision = 'b018e6182c95'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
