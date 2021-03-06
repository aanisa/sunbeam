"""empty message

Revision ID: 3fa0f5388a6b
Revises: d0e6392c497e
Create Date: 2017-01-05 16:07:03.753346

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3fa0f5388a6b'
down_revision = 'd0e6392c497e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('apply_blueprint_classroom',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('school_id', sa.Integer(), nullable=True),
    sa.Column('tc_classroom_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.ForeignKeyConstraint(['school_id'], [u'apply_blueprint_school.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column(u'apply_blueprint_school', sa.Column('tc_session_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column(u'apply_blueprint_school', 'tc_session_id')
    op.drop_table('apply_blueprint_classroom')
    # ### end Alembic commands ###
