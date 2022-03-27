"""empty message

Revision ID: 8a2960cce91a
Revises: db2c2794c95e
Create Date: 2022-02-28 14:11:46.164779

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a2960cce91a'
down_revision = 'db2c2794c95e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('seo_traffic_categories', sa.Column('month_year', sa.String(length=300), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('seo_traffic_categories', 'month_year')
    # ### end Alembic commands ###
