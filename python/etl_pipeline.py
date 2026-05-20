import pandas as pd
from sqlalchemy import create_engine, text

# -------------------------------
# DATABASE CONNECTION
# -------------------------------

username = "postgres"
password = "Abh1r%40cha"
host = "localhost"
port = "5432"
database = "retail_analytics"

engine = create_engine(
    f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
)

print("Database connection successful")

# -------------------------------
# LOAD CSV
# -------------------------------

csv_path = r"C:\Projects\superstore.csv"

df = pd.read_csv(csv_path,encoding='latin1')

# -------------------------------
# STANDARDIZE COLUMN NAMES
# -------------------------------

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
)

print("Column names standardized")
print(df.columns)

print("CSV loaded successfully")
print(f"Total rows loaded: {len(df)}")

# -------------------------------
# LOAD INTO STAGING TABLE
# -------------------------------

df.to_sql(
    "superstore_raw",
    engine,
    if_exists="replace",
    index=False
)

print("Data loaded into superstore_raw table")

# -------------------------------
# ETL TRANSFORMATION QUERIES
# -------------------------------

#with engine.connect() as conn:
with engine.begin() as conn:

    # -------------------------------
    # CLEAR EXISTING DATA
    # -------------------------------

    conn.execute(text("""
    TRUNCATE TABLE
        order_items,
        orders,
        products,
        customers
    RESTART IDENTITY CASCADE;
    """))

#    conn.commit()

    print("Existing tables truncated")

    # -------------------------------
    # LOAD CUSTOMERS
    # -------------------------------

    conn.execute(text("""
    INSERT INTO customers
    SELECT DISTINCT ON(customer_id)
        customer_id,
        customer_name,
        segment,
        country,
        region
    FROM superstore_raw;
    """))

    # -------------------------------
    # LOAD PRODUCTS
    # -------------------------------

    conn.execute(text("""
    INSERT INTO products
    SELECT DISTINCT ON(product_id)
        product_id,
        product_name,
        category,
        sub_category
    FROM superstore_raw;
    """))

    # -------------------------------
    # LOAD ORDERS
    # -------------------------------

    #conn.execute(text("""
    #INSERT INTO orders
    #SELECT DISTINCT ON(order_id)
    #    order_id,
    #    order_date::DATE,
    #    ship_date::DATE,
    #    ship_mode,
    #    customer_id,
    #    region,
    #    postal_code
    #FROM superstore_raw;
    #"""))
    conn.execute(text("""
    INSERT INTO orders
    SELECT DISTINCT ON(order_id)
        order_id,
        TO_DATE(order_date, 'MM/DD/YYYY'),
        TO_DATE(ship_date, 'MM/DD/YYYY'),
        ship_mode,
        customer_id,
        region,
        postal_code
    FROM superstore_raw
    ORDER BY order_id;
    """))
    # -------------------------------
    # LOAD ORDER ITEMS
    # -------------------------------

    conn.execute(text("""
    INSERT INTO order_items
    SELECT
        row_id,
        order_id,
        product_id,
        sales,
        quantity,
        discount,
        profit
    FROM superstore_raw;
    """))

conn.commit()

#print("ETL pipeline executed successfully")
    
print("ETL pipeline executed successfully")

# -------------------------------
# ETL Load Verification
# -------------------------------

#query = """
#SELECT COUNT(*) AS total_rows
#FROM order_items;
#"""

query = """
SELECT 'customers' AS table_name, COUNT(*) AS total_rows
FROM customers

UNION ALL

SELECT 'products', COUNT(*)
FROM products

UNION ALL

SELECT 'orders', COUNT(*)
FROM orders

UNION ALL

SELECT 'order_items', COUNT(*)
FROM order_items;
"""

validation = pd.read_sql(query, engine)

print(validation)

print("Pipeline completed successfully")