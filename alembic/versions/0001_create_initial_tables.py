from alembic import op
import sqlalchemy as sa
revision = '0001_create_initial_tables'
down_revision = None
def upgrade():
    op.create_table('models', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('name', sa.String(), nullable=False), sa.Column('description', sa.Text(), nullable=True), sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_table('assets', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('filename', sa.String(), nullable=False), sa.Column('content_type', sa.String(), nullable=True), sa.Column('size', sa.Integer(), nullable=True), sa.Column('s3_key', sa.String(), nullable=False), sa.Column('thumbnail_key', sa.String(), nullable=True), sa.Column('processed', sa.Boolean(), nullable=True), sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()), sa.Column('model_id', sa.Integer(), sa.ForeignKey('models.id'), nullable=True))
def downgrade():
    op.drop_table('assets'); op.drop_table('models')
