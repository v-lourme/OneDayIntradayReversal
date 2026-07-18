from pathlib import Path


# PostgreSQL

DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "onereversal"

# Paths

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"