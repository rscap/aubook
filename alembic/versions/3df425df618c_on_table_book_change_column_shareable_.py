"""on table book change column shareable from string to boolean

Revision ID: 3df425df618c
Revises: 
Create Date: 2016-12-19 15:10:59.189147

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3df425df618c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('book','shareable', type_=sa.Boolean())


def downgrade():
    pass
