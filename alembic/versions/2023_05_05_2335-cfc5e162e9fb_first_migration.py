"""First migration

Revision ID: cfc5e162e9fb
Revises: 
Create Date: 2023-05-05 23:35:54.702949+00:00

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision = 'cfc5e162e9fb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('toolschema',
    sa.Column('json_', sa.JSON(), nullable=True),
    sa.Column('results_schema', sa.JSON(), nullable=True),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('url', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('verb', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.PrimaryKeyConstraint('name'),
    sa.UniqueConstraint('name')
    )
    op.create_table('param',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('tool_schema_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('options', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('length', sa.Integer(), nullable=True),
    sa.Column('max_length', sa.Integer(), nullable=True),
    sa.Column('min_length', sa.Integer(), nullable=True),
    sa.Column('min_value', sa.Integer(), nullable=True),
    sa.Column('max_value', sa.Integer(), nullable=True),
    sa.Column('required', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['tool_schema_name'], ['toolschema.name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('param')
    op.drop_table('toolschema')
    # ### end Alembic commands ###
