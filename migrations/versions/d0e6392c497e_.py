"""empty message

Revision ID: d0e6392c497e
Revises: e716026b822f
Create Date: 2017-01-05 14:04:55.014237

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'd0e6392c497e'
down_revision = 'e716026b822f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('apply_blueprint_email',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('address', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('apply_blueprint_email_school',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('email_id', sa.Integer(), nullable=True),
    sa.Column('school_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['email_id'], ['apply_blueprint_email.id'], ),
    sa.ForeignKeyConstraint(['school_id'], ['apply_blueprint_school.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    # added by dan
    checklist_status = postgresql.ENUM("New Application", "Offer Accepted", "In Process", "Offer Out", "Offer Rejected", "Waitlisted", "Rejected", name='checklist_status_enum')
    checklist_status.create(op.get_bind())
    # end

    op.add_column(u'apply_blueprint_checklist', sa.Column('status', sa.Enum("New Application", "Offer Accepted", "In Process", "Offer Out", "Offer Rejected", "Waitlisted", "Rejected", name='checklist_status_enum'), nullable=True))
    op.drop_column(u'apply_blueprint_school', 'email')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(u'apply_blueprint_school', sa.Column('email', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.drop_column(u'apply_blueprint_checklist', 'status')
    op.drop_table('apply_blueprint_email_school')
    op.drop_table('apply_blueprint_email')
    # ### end Alembic commands ###
