"""add user table

Revision ID: 64568b70c5f0
Revises: 8044239483b3
Create Date: 2022-09-24 20:58:07.329403

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64568b70c5f0'
down_revision = '8044239483b3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
