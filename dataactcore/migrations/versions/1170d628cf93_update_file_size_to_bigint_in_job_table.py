"""Update file_size to BigInt in Job table

Revision ID: 1170d628cf93
Revises: 4bbc47f2b48d
Create Date: 2019-01-28 14:11:34.855541

"""

# revision identifiers, used by Alembic.
revision = '1170d628cf93'
down_revision = '4bbc47f2b48d'
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
    op.alter_column('job', 'file_size',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade_data_broker():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('job', 'file_size',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    # ### end Alembic commands ###

