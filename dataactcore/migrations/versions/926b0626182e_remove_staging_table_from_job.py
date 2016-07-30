"""remove_staging_table_from_job

Revision ID: 926b0626182e
Revises: 652047b81988
Create Date: 2016-06-17 11:31:56.044000

"""

# revision identifiers, used by Alembic.
revision = '926b0626182e'
down_revision = '652047b81988'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()



def upgrade_data_broker():
    pass

def downgrade_data_broker():
    pass

def upgrade_error_data():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_error_data():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def upgrade_job_tracker():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('job', 'staging_table')
    ### end Alembic commands ###


def downgrade_job_tracker():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('job', sa.Column('staging_table', sa.TEXT(), autoincrement=False, nullable=True))
    ### end Alembic commands ###


def upgrade_user_manager():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_user_manager():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def upgrade_validation():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_validation():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###

