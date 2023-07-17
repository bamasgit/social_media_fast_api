"""create content column for posts

Revision ID: ca3585fb11a7
Revises: 898daded9db8
Create Date: 2023-07-17 10:17:21.179452

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm


# revision identifiers, used by Alembic.
revision = 'ca3585fb11a7'
down_revision = '898daded9db8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
