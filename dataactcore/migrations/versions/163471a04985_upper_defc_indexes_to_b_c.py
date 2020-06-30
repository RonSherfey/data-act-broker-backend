""" Upper DEFC indexes to B/C

Revision ID: 163471a04985
Revises: 05edb849e42a
Create Date: 2020-05-08 17:06:14.165839

"""

# revision identifiers, used by Alembic.
revision = '163471a04985'
down_revision = '05edb849e42a'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text
from sqlalchemy.dialects import postgresql

def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_data_broker():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_oc_pa_defc_upper', 'object_class_program_activity',
                    [text('UPPER(disaster_emergency_fund_code)')], unique=False)
    op.create_index('ix_af_defc_upper', 'award_financial',
                    [text('UPPER(disaster_emergency_fund_code)')], unique=False)
    # ### end Alembic commands ###


def downgrade_data_broker():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_af_defc_upper', table_name='award_financial')
    op.drop_index('ix_oc_pa_defc_upper', table_name='object_class_program_activity')
    # ### end Alembic commands ###

