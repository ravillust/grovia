# =========================================================================
# KODE PERBAIKAN PATH - HARUS DI PALING ATAS
# =========================================================================
import sys
from pathlib import Path

# Tambahkan root project ke Python path
file_path = Path(__file__).resolve()
project_root = file_path.parents[1]
sys.path.insert(0, str(project_root))

# =========================================================================
# IMPORT STANDARD ALEMBIC
# =========================================================================
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, String
from alembic import context

# Alembic config object
config = context.config

# Setup logging dari alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# =========================================================================
# IMPORT MODELS - Hanya model yang dipakai
# =========================================================================
from app.database import Base

# Import model yang dipakai: User dan DetectionHistory
print("\n" + "="*70)
print("[IMPORT] Importing Models...")
print("="*70)

try:
    from app.models.user import User
    print("[SUCCESS] User model imported")
except ImportError as e:
    print(f"[ERROR] Failed to import User: {e}")

try:
    from app.models.detection_history import DetectionHistory
    print("[SUCCESS] DetectionHistory model imported")
except ImportError as e:
    print(f"[ERROR] Failed to import DetectionHistory: {e}")

# Set target metadata untuk Alembic
target_metadata = Base.metadata

print(f"\n[INFO] Total tables registered: {len(target_metadata.tables)}")
for table_name in target_metadata.tables.keys():
    print(f"   • {table_name}")
print("="*70 + "\n")

# =========================================================================
# FUNGSI DEBUG - Cek kolom String tanpa panjang
# =========================================================================
def check_string_columns():
    """Validasi semua String columns punya panjang"""
    print("\n" + "="*70)
    print("[VALIDATE] VALIDATING STRING COLUMNS")
    print("="*70)
    
    has_error = False
    error_details = []
    
    for table_name, table in target_metadata.tables.items():
        print(f"\n[TABLE] Table: {table_name}")
        
        for column in table.columns:
            if isinstance(column.type, String):
                if column.type.length is None:
                    print(f"   [ERROR] '{column.name}': String WITHOUT length!")
                    error_details.append({
                        'table': table_name,
                        'column': column.name
                    })
                    has_error = True
                else:
                    print(f"   [OK] '{column.name}': String({column.type.length})")
            else:
                col_type_name = column.type.__class__.__name__
                print(f"   [INFO] '{column.name}': {col_type_name}")
    
    print("\n" + "="*70)
    if has_error:
        print("[WARNING] ERROR: Found String columns without length!")
        print("\n[FIX] FIX THESE COLUMNS:")
        for err in error_details:
            print(f"   • Table '{err['table']}', Column '{err['column']}'")
            print(f"     Fix: Change Column(String) to Column(String(length))")
        print("\n" + "="*70)
    else:
        print("[SUCCESS] SUCCESS: All String columns have proper length!")
        print("="*70)
    
    print()
    return not has_error

# =========================================================================
# ALEMBIC MIGRATION FUNCTIONS
# =========================================================================

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
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
    """Run migrations in 'online' mode."""
    
    # Validasi String columns terlebih dahulu
    is_valid = check_string_columns()
    
    if not is_valid:
        print("[STOP] STOPPING: Fix String column issues first!")
        print("Check the error messages above for details.\n")
        raise Exception("String columns without length detected.")
    
    # Buat engine dan jalankan migration
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    
    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )
        
        with context.begin_transaction():
            context.run_migrations()


# =========================================================================
# ENTRY POINT
# =========================================================================
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()