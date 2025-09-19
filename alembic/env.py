# alembic/env.py
from logging.config import fileConfig
import os
import sys
from dotenv import load_dotenv

# allow imports like `from app...` by adding project root to sys.path
PACKAGE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PACKAGE_ROOT)

from sqlalchemy import engine_from_config, pool # type: ignore
from alembic import context

# Alembic config
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# load .env from project root (safer than default current working dir)
dotenv_path = os.path.join(PACKAGE_ROOT, ".env")
load_dotenv(dotenv_path)

# get DATABASE_URL from .env (or fallback to alembic.ini value)
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    # set it into alembic config so engine_from_config will see it
    config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Import your Base and all model modules (so tables are registered on Base.metadata)
from app.core.database import Base  # <-- ensure this is where you defined declarative_base()
# import modules that define models so they are registered
import app.models.doctor_models
import app.models.patient_models
import app.models.department
# ... import any other model modules

# tell Alembic about metadata for autogenerate
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
