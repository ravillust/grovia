# =========================================================================
# KODE PERBAIKAN PATH (BARIS 1 HINGGA 9) - HARUS BERADA DI POSISI PALING ATAS
# =========================================================================
import sys
import os
from pathlib import Path

# Memperbaiki Python Path agar Alembic dapat menemukan modul "app"
file_path = Path(__file__).resolve()
# parents[1] mengacu pada direktori root proyek (grovia-backend)
project_root = file_path.parents[1]
sys.path.insert(0, str(project_root))
# =========================================================================

# --- Impor Lokal Aplikasi Anda ---
# Memastikan semua model diimpor agar metadatanya dimuat oleh Alembic
from app.database import Base 
from app.models import user, detection, disease 

# Target metadata Alembic adalah Base.metadata dari SQLAlchemy
target_metadata = Base.metadata

# --- Impor Standar Alembic/SQLAlchemy ---
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# ini adalah Config object dari alembic.ini
config = context.config

# Membaca konfigurasi logging dari alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- Fungsi dan Logika Utama Alembic ---

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a database to exist.

    Calls context.execute() here need to be commented out
    since there's no database connection.

    """
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
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()