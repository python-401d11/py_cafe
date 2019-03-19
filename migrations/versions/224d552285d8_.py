"""empty message

Revision ID: 224d552285d8
Revises: ce66d77e8a63
Create Date: 2019-03-19 11:04:47.053201

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '224d552285d8'
down_revision = 'ce66d77e8a63'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('customers_id_fkey', 'customers', type_='foreignkey')
    op.create_foreign_key(None, 'customers', 'users', ['id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.drop_constraint('employees_id_fkey', 'employees', type_='foreignkey')
    op.create_foreign_key(None, 'employees', 'users', ['id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.drop_constraint('managers_id_fkey', 'managers', type_='foreignkey')
    op.create_foreign_key(None, 'managers', 'users', ['id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'managers', type_='foreignkey')
    op.create_foreign_key('managers_id_fkey', 'managers', 'users', ['id'], ['id'])
    op.drop_constraint(None, 'employees', type_='foreignkey')
    op.create_foreign_key('employees_id_fkey', 'employees', 'users', ['id'], ['id'])
    op.drop_constraint(None, 'customers', type_='foreignkey')
    op.create_foreign_key('customers_id_fkey', 'customers', 'users', ['id'], ['id'])
    # ### end Alembic commands ###