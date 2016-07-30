"""add_field_name_map

Revision ID: f9881b041355
Revises: ac6c35049702
Create Date: 2016-05-16 10:52:29.934000

"""

# revision identifiers, used by Alembic.
revision = 'f9881b041355'
down_revision = 'ac6c35049702'
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
    pass
    ### end Alembic commands ###


def downgrade_job_tracker():
    ### commands auto generated by Alembic - please adjust! ###
    pass
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


def upgrade_staging():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('field_name_map',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('field_name_map_id', sa.Integer(), nullable=False),
    sa.Column('table_name', sa.Text(), nullable=True),
    sa.Column('column_to_field_map', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('field_name_map_id')
    )
    ### end Alembic commands ###

def downgrade_staging():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('field_name_map')
    ### end Alembic commands ###

