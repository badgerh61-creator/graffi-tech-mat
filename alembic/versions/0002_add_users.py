from alembic import op
import sqlalchemy as sa
revision = '0002_add_users'
down_revision = '0001_create_initial_tables'
def upgrade():
    op.create_table('users', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('email', sa.String(), nullable=False, unique=True), sa.Column('hashed_password', sa.String(), nullable=False), sa.Column('is_active', sa.Integer(), nullable=True), sa.Column('is_admin', sa.Integer(), nullable=True), sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()))
def downgrade():
    op.drop_table('users')
