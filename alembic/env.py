from logging.config import fileConfig
import os, sys
from alembic import context
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.app.core.config import settings
from backend.app.db.session import Base

config = context.config
fileConfig(config.config_file_name)
from backend.app import models  # ensure all models are imported for Alembic

db_url = os.getenv('DATABASE_URL') or settings.DATABASE_URL
config.set_main_option('sqlalchemy.url', db_url)

target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option('sqlalchemy.url')
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    from sqlalchemy import create_engine
    connectable = create_engine(config.get_main_option('sqlalchemy.url'))
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
