"""Adding UEI elements to detached_award_procurement table

Revision ID: 77bd1ef8c53b
Revises: e72f2699bcaa
Create Date: 2021-05-11 13:24:50.207342

"""

# revision identifiers, used by Alembic.
revision = '77bd1ef8c53b'
down_revision = 'e72f2699bcaa'
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
    op.add_column('detached_award_procurement', sa.Column('awardee_or_recipient_uei', sa.Text(), nullable=True))
    op.add_column('detached_award_procurement', sa.Column('awardee_or_recipient_uei_n', sa.Text(), nullable=True))
    op.add_column('detached_award_procurement', sa.Column('ultimate_parent_uei', sa.Text(), nullable=True))
    op.add_column('detached_award_procurement', sa.Column('ultimate_parent_uei_name', sa.Text(), nullable=True))
    op.create_index(op.f('ix_detached_award_procurement_awardee_or_recipient_uei'), 'detached_award_procurement', ['awardee_or_recipient_uei'], unique=False)
    # ### end Alembic commands ###


def downgrade_data_broker():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_detached_award_procurement_awardee_or_recipient_uei'), table_name='detached_award_procurement')
    op.drop_column('detached_award_procurement', 'ultimate_parent_uei_name')
    op.drop_column('detached_award_procurement', 'ultimate_parent_uei')
    op.drop_column('detached_award_procurement', 'awardee_or_recipient_uei_n')
    op.drop_column('detached_award_procurement', 'awardee_or_recipient_uei')
    # ### end Alembic commands ###

