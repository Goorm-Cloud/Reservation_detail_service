"""init

Revision ID: e486c938a935
Revises: 
Create Date: 2025-02-21 11:28:05.640889

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e486c938a935'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('parkinglot', schema=None) as batch_op:
        batch_op.alter_column('parkinglot_time',
               existing_type=sa.TIME(),
               type_=sa.DateTime(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('parkinglot', schema=None) as batch_op:
        batch_op.alter_column('parkinglot_time',
               existing_type=sa.DateTime(),
               type_=sa.TIME(),
               existing_nullable=True)

    # ### end Alembic commands ###
