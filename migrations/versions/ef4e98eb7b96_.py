"""empty message

Revision ID: ef4e98eb7b96
Revises: 4be33d7d336a
Create Date: 2025-04-04 01:21:32.825615

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef4e98eb7b96'
down_revision = '4be33d7d336a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=50), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite', schema=None) as batch_op:
        batch_op.drop_column('name')

    # ### end Alembic commands ###
