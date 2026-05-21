#DB_USER = "postgres"
#DB_PASSWORD = "Abh1r@cha"
#DB_HOST = "localhost"
#DB_PORT = "5432"
#DB_NAME = "retail_analytics"

#CSV_PATH = r"data/Superstore.csv"
#CSV_PATH = r"C:\Projects\superstore.csv"

from pathlib import Path

DB_USER = "postgres"
DB_PASSWORD = "Abh1r%40cha"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "retail_analytics"

BASE_DIR = Path(__file__).resolve().parent.parent
SCHEMA_PATH = BASE_DIR / "sql" / "03_create_tables.sql"

CSV_PATH = BASE_DIR / "data" / "Superstore.csv"