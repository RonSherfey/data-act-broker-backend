"""Dropping FPDS UEI name cols

Revision ID: 9e295cff8733
Revises: 9a73f1a0ee98
Create Date: 2021-07-23 15:29:23.990917

"""

# revision identifiers, used by Alembic.
revision = '9e295cff8733'
down_revision = '9a73f1a0ee98'
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
    op.drop_column('detached_award_procurement', 'awardee_or_recipient_uei_n')
    op.drop_column('detached_award_procurement', 'ultimate_parent_uei_name')
    # ### end Alembic commands ###


def downgrade_data_broker():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('detached_award_procurement', sa.Column('ultimate_parent_uei_name', sa.TEXT(), autoincrement=False, nullable=True))
    op.add_column('detached_award_procurement', sa.Column('awardee_or_recipient_uei_n', sa.TEXT(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###

