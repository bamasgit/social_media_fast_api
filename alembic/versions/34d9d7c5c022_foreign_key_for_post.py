"""foreign key for post

Revision ID: 34d9d7c5c022
Revises: 3318cb88e77d
Create Date: 2023-07-17 12:42:33.432787

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34d9d7c5c022'
down_revision = '3318cb88e77d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")
 
 
    pass


def downgrade() -> None:
    pass
