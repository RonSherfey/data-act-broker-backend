"""Adding additional_reporting to award_procurement table

Revision ID: 737cae4d1c76
Revises: 3fd9a578c9c5
Create Date: 2020-05-21 10:12:14.687816

"""

# revision identifiers, used by Alembic.
revision = '737cae4d1c76'
down_revision = '3fd9a578c9c5'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_data_broker():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('award_procurement', sa.Column('additional_reporting', sa.Text(), nullable=True))
    op.add_column('certified_award_procurement', sa.Column('additional_reporting', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade_data_broker():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('certified_award_procurement', 'additional_reporting')
    op.drop_column('award_procurement', 'additional_reporting')
    # ### end Alembic commands ###

