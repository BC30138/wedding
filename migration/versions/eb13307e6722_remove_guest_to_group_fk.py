"""remove guest to group fk

Revision ID: eb13307e6722
Revises: bd28141af4e3
Create Date: 2023-02-13 18:57:36.028813

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb13307e6722'
down_revision = 'bd28141af4e3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('guests_group_id_fkey', 'guests', type_='foreignkey')
    op.drop_column('guests', 'group_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('guests', sa.Column('group_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('guests_group_id_fkey', 'guests', 'groups', ['group_id'], ['id'])
    # ### end Alembic commands ###
