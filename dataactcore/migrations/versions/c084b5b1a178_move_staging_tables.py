"""move_staging_tables

Revision ID: c084b5b1a178
Revises: c75b5f18b7e4
Create Date: 2016-06-16 21:30:32.166590

"""

# revision identifiers, used by Alembic.
revision = 'c084b5b1a178'
down_revision = 'c75b5f18b7e4'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from dataactcore.config import CONFIG_DB
from sqlalchemy import create_engine
from sqlalchemy import Table, MetaData


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
    op.create_table('appropriation',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('appropriation_id', sa.Integer(), nullable=False),
    sa.Column('submission_id', sa.Integer(), nullable=False),
    sa.Column('job_id', sa.Integer(), nullable=False),
    sa.Column('row', sa.Integer(), nullable=False),
    sa.Column('adjustmentstounobligatedbalancebroughtforward_cpe', sa.Numeric(), nullable=True),
    sa.Column('agencyidentifier', sa.Text(), nullable=True),
    sa.Column('allocationtransferagencyidentifier', sa.Text(), nullable=True),
    sa.Column('availabilitytypecode', sa.Text(), nullable=True),
    sa.Column('beginningperiodofavailability', sa.Text(), nullable=True),
    sa.Column('borrowingauthorityamounttotal_cpe', sa.Numeric(), nullable=True),
    sa.Column('budgetauthorityappropriatedamount_cpe', sa.Numeric(), nullable=True),
    sa.Column('budgetauthorityavailableamounttotal_cpe', sa.Numeric(), nullable=True),
    sa.Column('budgetauthorityunobligatedbalancebroughtforward_fyb', sa.Numeric(), nullable=True),
    sa.Column('contractauthorityamounttotal_cpe', sa.Numeric(), nullable=True),
    sa.Column('deobligationsrecoveriesrefundsbytas_cpe', sa.Numeric(), nullable=True),
    sa.Column('endingperiodofavailability', sa.Text(), nullable=True),
    sa.Column('grossoutlayamountbytas_cpe', sa.Numeric(), nullable=True),
    sa.Column('mainaccountcode', sa.Text(), nullable=True),
    sa.Column('obligationsincurredtotalbytas_cpe', sa.Numeric(), nullable=True),
    sa.Column('otherbudgetaryresourcesamount_cpe', sa.Numeric(), nullable=True),
    sa.Column('spendingauthorityfromoffsettingcollectionsamounttotal_cpe', sa.Numeric(), nullable=True),
    sa.Column('statusofbudgetaryresourcestotal_cpe', sa.Numeric(), nullable=True),
    sa.Column('subaccountcode', sa.Text(), nullable=True),
    sa.Column('unobligatedbalance_cpe', sa.Numeric(), nullable=True),
    sa.Column('tas', sa.Text(), nullable=False),
    sa.Column('valid_record', sa.Boolean(), server_default='True', nullable=False),
    sa.PrimaryKeyConstraint('appropriation_id')
    )
    op.create_index(op.f('ix_appropriation_job_id'), 'appropriation', ['job_id'], unique=False)
    op.create_index(op.f('ix_appropriation_submission_id'), 'appropriation', ['submission_id'], unique=False)
    op.create_index(op.f('ix_appropriation_tas'), 'appropriation', ['tas'], unique=False)
    op.create_table('award_financial',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('award_financial_id', sa.Integer(), nullable=False),
    sa.Column('submission_id', sa.Integer(), nullable=False),
    sa.Column('job_id', sa.Integer(), nullable=False),
    sa.Column('row', sa.Integer(), nullable=False),
    sa.Column('agencyidentifier', sa.Text(), nullable=True),
    sa.Column('allocationtransferagencyidentifier', sa.Text(), nullable=True),
    sa.Column('availabilitytypecode', sa.Text(), nullable=True),
    sa.Column('beginningperiodofavailability', sa.Text(), nullable=True),
    sa.Column('bydirectreimbursablefundingsource', sa.Text(), nullable=True),
    sa.Column('deobligationsrecoveriesrefundsofprioryearbyaward_cpe', sa.Numeric(), nullable=True),
    sa.Column('endingperiodofavailability', sa.Text(), nullable=True),
    sa.Column('fain', sa.Text(), nullable=True),
    sa.Column('grossoutlayamountbyaward_cpe', sa.Numeric(), nullable=True),
    sa.Column('grossoutlayamountbyaward_fyb', sa.Numeric(), nullable=True),
    sa.Column('grossoutlaysdeliveredorderspaidtotal_cpe', sa.Numeric(), nullable=True),
    sa.Column('grossoutlaysdeliveredorderspaidtotal_fyb', sa.Numeric(), nullable=True),
    sa.Column('grossoutlaysundeliveredordersprepaidtotal_cpe', sa.Numeric(), nullable=True),
    sa.Column('grossoutlaysundeliveredordersprepaidtotal_fyb', sa.Numeric(), nullable=True),
    sa.Column('mainaccountcode', sa.Text(), nullable=True),
    sa.Column('objectclass', sa.Text(), nullable=True),
    sa.Column('obligationsdeliveredordersunpaidtotal_cpe', sa.Numeric(), nullable=True),
    sa.Column('obligationsdeliveredordersunpaidtotal_fyb', sa.Numeric(), nullable=True),
    sa.Column('obligationsincurredtotalbyaward_cpe', sa.Numeric(), nullable=True),
    sa.Column('obligationsundeliveredordersunpaidtotal_cpe', sa.Numeric(), nullable=True),
    sa.Column('obligationsundeliveredordersunpaidtotal_fyb', sa.Numeric(), nullable=True),
    sa.Column('parentawardid', sa.Text(), nullable=True),
    sa.Column('piid', sa.Text(), nullable=True),
    sa.Column('programactivitycode', sa.Text(), nullable=True),
    sa.Column('programactivityname', sa.Text(), nullable=True),
    sa.Column('subaccountcode', sa.Text(), nullable=True),
    sa.Column('transactionobligatedamount', sa.Numeric(), nullable=True),
    sa.Column('uri', sa.Text(), nullable=True),
    sa.Column('ussgl480100_undeliveredordersobligationsunpaid_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl480100_undeliveredordersobligationsunpaid_fyb', sa.Numeric(), nullable=True),
    sa.Column('ussgl480200_undeliveredordersobligationsprepaidadv_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl480200_undeliveredordersobligationsprepaidadvanced_fyb', sa.Numeric(), nullable=True),
    sa.Column('ussgl483100_undeliveredordersobligtransferredunpaid_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl483200_undeliveredordersobligtransferredppdadv_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl487100_downadjsprioryrunpaidundelivordersobligrec_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl487200_downadjsprioryrppdadvundelivordersobligref_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl488100_upadjsprioryearundelivordersobligunpaid_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl488200_upadjsprioryrundelivordersobligprepaidadv_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl490100_deliveredordersobligationsunpaid_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl490100_deliveredordersobligationsunpaid_fyb', sa.Numeric(), nullable=True),
    sa.Column('ussgl490200_deliveredordersobligationspaid_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl490800_authorityoutlayednotyetdisbursed_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl490800_authorityoutlayednotyetdisbursed_fyb', sa.Numeric(), nullable=True),
    sa.Column('ussgl493100_deliveredordersobligstransferredunpaid_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl497100_downadjsprioryrunpaiddelivordersobligrec_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl497200_downadjsprioryrpaiddelivordersobligrefclt_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl498100_upadjsprioryeardeliveredordersobligunpaid_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl498200_upadjsprioryrdelivordersobligpaid_cpe', sa.Numeric(), nullable=True),
    sa.Column('tas', sa.Text(), nullable=False),
    sa.Column('valid_record', sa.Boolean(), server_default='True', nullable=False),
    sa.PrimaryKeyConstraint('award_financial_id')
    )
    op.create_index(op.f('ix_award_financial_fain'), 'award_financial', ['fain'], unique=False)
    op.create_index(op.f('ix_award_financial_job_id'), 'award_financial', ['job_id'], unique=False)
    op.create_index(op.f('ix_award_financial_piid'), 'award_financial', ['piid'], unique=False)
    op.create_index(op.f('ix_award_financial_submission_id'), 'award_financial', ['submission_id'], unique=False)
    op.create_index('ix_award_financial_tas_oc_pa', 'award_financial', ['tas', 'objectclass', 'programactivitycode'], unique=False)
    op.create_index(op.f('ix_award_financial_uri'), 'award_financial', ['uri'], unique=False)
    op.create_table('award_financial_assistance',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('award_financial_assistance_id', sa.Integer(), nullable=False),
    sa.Column('submission_id', sa.Integer(), nullable=False),
    sa.Column('job_id', sa.Integer(), nullable=False),
    sa.Column('row', sa.Integer(), nullable=False),
    sa.Column('actiondate', sa.Text(), nullable=True),
    sa.Column('actiontype', sa.Text(), nullable=True),
    sa.Column('assistancetype', sa.Text(), nullable=True),
    sa.Column('awarddescription', sa.Text(), nullable=True),
    sa.Column('awardeeorrecipientlegalentityname', sa.Text(), nullable=True),
    sa.Column('awardeeorrecipientuniqueidentifier', sa.Text(), nullable=True),
    sa.Column('awardingagencycode', sa.Text(), nullable=True),
    sa.Column('awardingagencyname', sa.Text(), nullable=True),
    sa.Column('awardingofficecode', sa.Text(), nullable=True),
    sa.Column('awardingofficename', sa.Text(), nullable=True),
    sa.Column('awardingsubtieragencycode', sa.Text(), nullable=True),
    sa.Column('awardingsubtieragencyname', sa.Text(), nullable=True),
    sa.Column('awardmodificationamendmentnumber', sa.Text(), nullable=True),
    sa.Column('businessfundsindicator', sa.Text(), nullable=True),
    sa.Column('businesstypes', sa.Text(), nullable=True),
    sa.Column('cfda_number', sa.Text(), nullable=True),
    sa.Column('cfda_title', sa.Text(), nullable=True),
    sa.Column('correctionlatedeleteindicator', sa.Text(), nullable=True),
    sa.Column('facevalueloanguarantee', sa.Numeric(), nullable=True),
    sa.Column('fain', sa.Text(), nullable=True),
    sa.Column('federalactionobligation', sa.Numeric(), nullable=True),
    sa.Column('fiscalyearandquartercorrection', sa.Text(), nullable=True),
    sa.Column('fundingagencycode', sa.Text(), nullable=True),
    sa.Column('fundingagencyname', sa.Text(), nullable=True),
    sa.Column('fundingagencyofficename', sa.Text(), nullable=True),
    sa.Column('fundingofficecode', sa.Text(), nullable=True),
    sa.Column('fundingsubtieragencycode', sa.Text(), nullable=True),
    sa.Column('fundingsubtieragencyname', sa.Text(), nullable=True),
    sa.Column('legalentityaddressline1', sa.Text(), nullable=True),
    sa.Column('legalentityaddressline2', sa.Text(), nullable=True),
    sa.Column('legalentityaddressline3', sa.Text(), nullable=True),
    sa.Column('legalentitycitycode', sa.Text(), nullable=True),
    sa.Column('legalentitycityname', sa.Text(), nullable=True),
    sa.Column('legalentitycongressionaldistrict', sa.Text(), nullable=True),
    sa.Column('legalentitycountrycode', sa.Text(), nullable=True),
    sa.Column('legalentitycountycode', sa.Text(), nullable=True),
    sa.Column('legalentitycountyname', sa.Text(), nullable=True),
    sa.Column('legalentityforeigncityname', sa.Text(), nullable=True),
    sa.Column('legalentityforeignpostalcode', sa.Text(), nullable=True),
    sa.Column('legalentityforeignprovincename', sa.Text(), nullable=True),
    sa.Column('legalentitystatecode', sa.Text(), nullable=True),
    sa.Column('legalentitystatename', sa.Text(), nullable=True),
    sa.Column('legalentityzip5', sa.Text(), nullable=True),
    sa.Column('legalentityziplast4', sa.Text(), nullable=True),
    sa.Column('nonfederalfundingamount', sa.Numeric(), nullable=True),
    sa.Column('originalloansubsidycost', sa.Numeric(), nullable=True),
    sa.Column('periodofperformancecurrentenddate', sa.Text(), nullable=True),
    sa.Column('periodofperformancestartdate', sa.Text(), nullable=True),
    sa.Column('primaryplaceofperformancecityname', sa.Text(), nullable=True),
    sa.Column('primaryplaceofperformancecode', sa.Text(), nullable=True),
    sa.Column('primaryplaceofperformancecongressionaldistrict', sa.Text(), nullable=True),
    sa.Column('primaryplaceofperformancecountrycode', sa.Text(), nullable=True),
    sa.Column('primaryplaceofperformancecountyname', sa.Text(), nullable=True),
    sa.Column('primaryplaceofperformanceforeignlocationdescription', sa.Text(), nullable=True),
    sa.Column('primaryplaceofperformancestatename', sa.Text(), nullable=True),
    sa.Column('primaryplaceofperformancezipplus4', sa.Text(), nullable=True),
    sa.Column('recordtype', sa.Integer(), nullable=True),
    sa.Column('sai_number', sa.Text(), nullable=True),
    sa.Column('totalfundingamount', sa.Numeric(), nullable=True),
    sa.Column('uri', sa.Text(), nullable=True),
    sa.Column('valid_record', sa.Boolean(), server_default='True', nullable=False),
    sa.PrimaryKeyConstraint('award_financial_assistance_id')
    )
    op.create_index(op.f('ix_award_financial_assistance_fain'), 'award_financial_assistance', ['fain'], unique=False)
    op.create_index(op.f('ix_award_financial_assistance_job_id'), 'award_financial_assistance', ['job_id'], unique=False)
    op.create_index(op.f('ix_award_financial_assistance_submission_id'), 'award_financial_assistance', ['submission_id'], unique=False)
    op.create_index(op.f('ix_award_financial_assistance_uri'), 'award_financial_assistance', ['uri'], unique=False)
    op.create_table('object_class_program_activity',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('object_class_program_activity_id', sa.Integer(), nullable=False),
    sa.Column('submission_id', sa.Integer(), nullable=False),
    sa.Column('job_id', sa.Integer(), nullable=False),
    sa.Column('row', sa.Integer(), nullable=False),
    sa.Column('agencyidentifier', sa.Text(), nullable=True),
    sa.Column('allocationtransferagencyidentifier', sa.Text(), nullable=True),
    sa.Column('availabilitytypecode', sa.Text(), nullable=True),
    sa.Column('beginningperiodofavailability', sa.Text(), nullable=True),
    sa.Column('bydirectreimbursablefundingsource', sa.Text(), nullable=True),
    sa.Column('deobligationsrecoveriesrefundsprioryrbyprogobjectclass_cpe', sa.Numeric(), nullable=True),
    sa.Column('endingperiodofavailability', sa.Text(), nullable=True),
    sa.Column('grossoutlayamountbyprogramobjectclass_cpe', sa.Numeric(), nullable=True),
    sa.Column('grossoutlayamountbyprogramobjectclass_fyb', sa.Numeric(), nullable=True),
    sa.Column('grossoutlaysdeliveredorderspaidtotal_cpe', sa.Numeric(), nullable=True),
    sa.Column('grossoutlaysdeliveredorderspaidtotal_fyb', sa.Numeric(), nullable=True),
    sa.Column('grossoutlaysundeliveredordersprepaidtotal_cpe', sa.Numeric(), nullable=True),
    sa.Column('grossoutlaysundeliveredordersprepaidtotal_fyb', sa.Numeric(), nullable=True),
    sa.Column('mainaccountcode', sa.Text(), nullable=True),
    sa.Column('objectclass', sa.Text(), nullable=True),
    sa.Column('obligationsdeliveredordersunpaidtotal_cpe', sa.Numeric(), nullable=True),
    sa.Column('obligationsdeliveredordersunpaidtotal_fyb', sa.Numeric(), nullable=True),
    sa.Column('obligationsincurredbyprogramobjectclass_cpe', sa.Numeric(), nullable=True),
    sa.Column('obligationsundeliveredordersunpaidtotal_cpe', sa.Numeric(), nullable=True),
    sa.Column('obligationsundeliveredordersunpaidtotal_fyb', sa.Numeric(), nullable=True),
    sa.Column('programactivitycode', sa.Text(), nullable=True),
    sa.Column('programactivityname', sa.Text(), nullable=True),
    sa.Column('subaccountcode', sa.Text(), nullable=True),
    sa.Column('ussgl480100_undeliveredordersobligationsunpaid_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl480100_undeliveredordersobligationsunpaid_fyb', sa.Numeric(), nullable=True),
    sa.Column('ussgl480200_undeliveredordersobligationsprepaidadv_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl480200_undeliveredordersobligationsprepaidadv_fyb', sa.Numeric(), nullable=True),
    sa.Column('ussgl483100_undeliveredordersobligtransferredunpaid_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl483200_undeliveredordersobligtransferredppdadv_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl487100_downadjsprioryrunpaidundelivordersobligrec_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl487200_downadjsprioryrppdadvundelivordersobligref_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl488100_upadjsprioryearundelivordersobligunpaid_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl488200_upadjsprioryrundelivordersobligprepaidadv_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl490100_deliveredordersobligationsunpaid_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl490100_deliveredordersobligationsunpaid_fyb', sa.Numeric(), nullable=True),
    sa.Column('ussgl490200_deliveredordersobligationspaid_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl490800_authorityoutlayednotyetdisbursed_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl490800_authorityoutlayednotyetdisbursed_fyb', sa.Numeric(), nullable=True),
    sa.Column('ussgl493100_deliveredordersobligstransferredunpaid_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl497100_downadjsprioryrunpaiddelivordersobligrec_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl497200_downadjsprioryrpaiddelivordersobligrefclt_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl498100_upadjsprioryeardeliveredordersobligunpaid_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl498200_upadjsprioryrdelivordersobligpaid_cpe', sa.Numeric(), nullable=True),
    sa.Column('tas', sa.Text(), nullable=False),
    sa.Column('valid_record', sa.Boolean(), server_default='True', nullable=False),
    sa.PrimaryKeyConstraint('object_class_program_activity_id')
    )
    op.create_index(op.f('ix_object_class_program_activity_job_id'), 'object_class_program_activity', ['job_id'], unique=False)
    op.create_index(op.f('ix_object_class_program_activity_submission_id'), 'object_class_program_activity', ['submission_id'], unique=False)
    op.create_index('ix_oc_pa_tas_oc_pa', 'object_class_program_activity', ['tas', 'objectclass', 'programactivitycode'], unique=False)
    ### end Alembic commands ###


def downgrade_validation():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_oc_pa_tas_oc_pa', table_name='object_class_program_activity')
    op.drop_index(op.f('ix_object_class_program_activity_submission_id'), table_name='object_class_program_activity')
    op.drop_index(op.f('ix_object_class_program_activity_job_id'), table_name='object_class_program_activity')
    op.drop_table('object_class_program_activity')
    op.drop_index(op.f('ix_award_financial_assistance_uri'), table_name='award_financial_assistance')
    op.drop_index(op.f('ix_award_financial_assistance_submission_id'), table_name='award_financial_assistance')
    op.drop_index(op.f('ix_award_financial_assistance_job_id'), table_name='award_financial_assistance')
    op.drop_index(op.f('ix_award_financial_assistance_fain'), table_name='award_financial_assistance')
    op.drop_table('award_financial_assistance')
    op.drop_index(op.f('ix_award_financial_uri'), table_name='award_financial')
    op.drop_index('ix_award_financial_tas_oc_pa', table_name='award_financial')
    op.drop_index(op.f('ix_award_financial_submission_id'), table_name='award_financial')
    op.drop_index(op.f('ix_award_financial_piid'), table_name='award_financial')
    op.drop_index(op.f('ix_award_financial_job_id'), table_name='award_financial')
    op.drop_index(op.f('ix_award_financial_fain'), table_name='award_financial')
    op.drop_table('award_financial')
    op.drop_index(op.f('ix_appropriation_tas'), table_name='appropriation')
    op.drop_index(op.f('ix_appropriation_submission_id'), table_name='appropriation')
    op.drop_index(op.f('ix_appropriation_job_id'), table_name='appropriation')
    op.drop_table('appropriation')
    ### end Alembic commands ###

