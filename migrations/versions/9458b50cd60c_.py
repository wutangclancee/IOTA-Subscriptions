"""empty message

Revision ID: 9458b50cd60c
Revises: 
Create Date: 2018-04-29 17:06:02.455987

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9458b50cd60c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('transactions', 'id',
               existing_type=mysql.VARCHAR(length=128),
               nullable=True)
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=False))
    op.add_column('users', sa.Column('is_anonymous', sa.Boolean(), nullable=False))
    op.add_column('users', sa.Column('is_authenticated', sa.Boolean(), nullable=False))
    op.create_unique_constraint(None, 'users', ['is_authenticated'])
    op.create_unique_constraint(None, 'users', ['is_anonymous'])
    op.create_unique_constraint(None, 'users', ['is_active'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'is_authenticated')
    op.drop_column('users', 'is_anonymous')
    op.drop_column('users', 'is_active')
    op.alter_column('transactions', 'id',
               existing_type=mysql.VARCHAR(length=128),
               nullable=False)
    # ### end Alembic commands ###
