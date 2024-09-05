"""Added archive attributes to sign key    

Revision ID: 444f9f1f0ac1
Revises: e952dc755f9d
Create Date: 2024-08-01 17:12:24.775826

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '444f9f1f0ac1'
down_revision = 'e952dc755f9d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sign_keys', sa.Column('active', sa.Boolean(), nullable=False, server_default=str(True)))
    op.add_column('sign_keys', sa.Column('archived', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sign_keys', 'archived')
    op.drop_column('sign_keys', 'active')
    # ### end Alembic commands ###
