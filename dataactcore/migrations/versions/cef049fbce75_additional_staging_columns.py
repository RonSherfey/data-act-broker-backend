"""additional_staging_columns

Revision ID: cef049fbce75
Revises: 94f7bda375e2
Create Date: 2016-06-06 12:55:47.659135

"""

# revision identifiers, used by Alembic.
revision = 'cef049fbce75'
down_revision = '94f7bda375e2'
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
    op.add_column('appropriation', sa.Column('job_id', sa.Integer(), nullable=False))
    op.add_column('appropriation', sa.Column('row', sa.Integer(), nullable=False))
    op.add_column('appropriation', sa.Column('submission_id', sa.Integer(), nullable=False))
    op.create_index(op.f('ix_appropriation_job_id'), 'appropriation', ['job_id'], unique=False)
    op.create_index(op.f('ix_appropriation_submission_id'), 'appropriation', ['submission_id'], unique=False)
    op.add_column('award_financial', sa.Column('job_id', sa.Integer(), nullable=False))
    op.add_column('award_financial', sa.Column('row', sa.Integer(), nullable=False))
    op.add_column('award_financial', sa.Column('submission_id', sa.Integer(), nullable=False))
    op.create_index(op.f('ix_award_financial_job_id'), 'award_financial', ['job_id'], unique=False)
    op.create_index(op.f('ix_award_financial_submission_id'), 'award_financial', ['submission_id'], unique=False)
    op.add_column('award_financial_assistance', sa.Column('job_id', sa.Integer(), nullable=False))
    op.add_column('award_financial_assistance', sa.Column('row', sa.Integer(), nullable=False))
    op.add_column('award_financial_assistance', sa.Column('submission_id', sa.Integer(), nullable=False))
    op.create_index(op.f('ix_award_financial_assistance_job_id'), 'award_financial_assistance', ['job_id'], unique=False)
    op.create_index(op.f('ix_award_financial_assistance_submission_id'), 'award_financial_assistance', ['submission_id'], unique=False)
    op.add_column('object_class_program_activity', sa.Column('job_id', sa.Integer(), nullable=False))
    op.add_column('object_class_program_activity', sa.Column('row', sa.Integer(), nullable=False))
    op.add_column('object_class_program_activity', sa.Column('submission_id', sa.Integer(), nullable=False))
    op.create_index(op.f('ix_object_class_program_activity_job_id'), 'object_class_program_activity', ['job_id'], unique=False)
    op.create_index(op.f('ix_object_class_program_activity_submission_id'), 'object_class_program_activity', ['submission_id'], unique=False)
    ### end Alembic commands ###


def downgrade_staging():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_object_class_program_activity_submission_id'), table_name='object_class_program_activity')
    op.drop_index(op.f('ix_object_class_program_activity_job_id'), table_name='object_class_program_activity')
    op.drop_column('object_class_program_activity', 'submission_id')
    op.drop_column('object_class_program_activity', 'row')
    op.drop_column('object_class_program_activity', 'job_id')
    op.drop_index(op.f('ix_award_financial_assistance_submission_id'), table_name='award_financial_assistance')
    op.drop_index(op.f('ix_award_financial_assistance_job_id'), table_name='award_financial_assistance')
    op.drop_column('award_financial_assistance', 'submission_id')
    op.drop_column('award_financial_assistance', 'row')
    op.drop_column('award_financial_assistance', 'job_id')
    op.drop_index(op.f('ix_award_financial_submission_id'), table_name='award_financial')
    op.drop_index(op.f('ix_award_financial_job_id'), table_name='award_financial')
    op.drop_column('award_financial', 'submission_id')
    op.drop_column('award_financial', 'row')
    op.drop_column('award_financial', 'job_id')
    op.drop_index(op.f('ix_appropriation_submission_id'), table_name='appropriation')
    op.drop_index(op.f('ix_appropriation_job_id'), table_name='appropriation')
    op.drop_column('appropriation', 'submission_id')
    op.drop_column('appropriation', 'row')
    op.drop_column('appropriation', 'job_id')
    ### end Alembic commands ###

