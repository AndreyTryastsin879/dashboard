"""empty message

Revision ID: db2c2794c95e
Revises: 831e077fe947
Create Date: 2022-02-28 12:12:30.406660

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db2c2794c95e'
down_revision = '831e077fe947'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('seo_traffic_categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('project_name', sa.String(length=300), nullable=True),
    sa.Column('traffic_category', sa.String(length=300), nullable=True),
    sa.Column('value', sa.Integer(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('seo_traffic_categories')
    # ### end Alembic commands ###
