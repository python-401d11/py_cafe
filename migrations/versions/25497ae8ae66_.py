"""empty message

Revision ID: 25497ae8ae66
Revises: 9bee782d5c72
Create Date: 2019-03-18 21:48:12.783527

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25497ae8ae66'
down_revision = '9bee782d5c72'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('email', sa.String(length=256), nullable=True),
    sa.Column('password', sa.String(length=256), nullable=True),
    sa.Column('type', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_foreign_key(None, 'customers', 'users', ['id'], ['id'])
    op.drop_column('customers', 'password')
    op.drop_column('customers', 'email')
    op.drop_column('customers', 'name')
    op.create_foreign_key(None, 'managers', 'users', ['id'], ['id'])
    op.drop_column('managers', 'password')
    op.drop_column('managers', 'email')
    op.drop_column('managers', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('managers', sa.Column('name', sa.VARCHAR(length=256), autoincrement=False, nullable=True))
    op.add_column('managers', sa.Column('email', sa.VARCHAR(length=256), autoincrement=False, nullable=True))
    op.add_column('managers', sa.Column('password', sa.VARCHAR(length=256), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'managers', type_='foreignkey')
    op.add_column('customers', sa.Column('name', sa.VARCHAR(length=256), autoincrement=False, nullable=True))
    op.add_column('customers', sa.Column('email', sa.VARCHAR(length=256), autoincrement=False, nullable=True))
    op.add_column('customers', sa.Column('password', sa.VARCHAR(length=256), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'customers', type_='foreignkey')
    op.drop_table('users')
    # ### end Alembic commands ###