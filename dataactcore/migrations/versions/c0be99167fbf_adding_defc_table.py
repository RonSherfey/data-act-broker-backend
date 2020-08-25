""" Adding DEFC table

Revision ID: c0be99167fbf
Revises: 7b70f7defa50
Create Date: 2020-08-20 20:14:46.265694

"""

# revision identifiers, used by Alembic.
revision = 'c0be99167fbf'
down_revision = '7b70f7defa50'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_data_broker():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('defc',
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('defc_id', sa.Integer(), nullable=False),
        sa.Column('code', sa.Text(), nullable=False),
        sa.Column('group', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('defc_id')
    )
    op.create_index(op.f('ix_defc_code'), 'defc', ['code'], unique=True)
    # ### end Alembic commands ###


def downgrade_data_broker():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_defc_code'), table_name='defc')
    op.drop_table('defc')
    # ### end Alembic commands ###

