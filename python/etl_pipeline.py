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
# print(df.columns)

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

    #conn.execute(text("""
    #TRUNCATE TABLE
    #    order_items,
    #    orders,
    #    products,
    #    customers
    #RESTART IDENTITY CASCADE;
    #"""))

#    conn.commit()

    #print("Existing tables truncated")

    # -------------------------------
    # LOAD CUSTOMERS
    # -------------------------------

    #conn.execute(text("""
    #INSERT INTO customers
    #SELECT DISTINCT ON(customer_id)
    #    customer_id,
    #    customer_name,
    #    segment,
    #    country,
    #    region
    #FROM superstore_raw;
    #"""))

    customer_result = conn.execute(text("""
    
    INSERT INTO customers (
        customer_id,
        customer_name,
        segment,
        country,
        region
    )

    SELECT DISTINCT ON (s.customer_id)
        s.customer_id,
        s.customer_name,
        s.segment,
        s.country,
        s.region
    FROM superstore_raw s WHERE NOT EXISTS (
        SELECT 1 FROM customers c WHERE c.customer_id = s.customer_id)

    ORDER BY s.customer_id;
    """))
    
    print(f"New customers inserted: {customer_result.rowcount}")

    # -------------------------------
    # LOAD PRODUCTS
    # -------------------------------

    #conn.execute(text("""
    #INSERT INTO products
    #SELECT DISTINCT ON(product_id)
    #    product_id,
    #    product_name,
    #    category,
    #    sub_category
    #FROM superstore_raw;
    #"""))
    
    product_result =conn.execute(text("""
    
    INSERT INTO products (
        product_id,
        product_name,
        category,
        sub_category
    )

    SELECT DISTINCT ON (s.product_id)
        s.product_id,
        s.product_name,
        s.category,
        s.sub_category
    FROM superstore_raw s WHERE NOT EXISTS (
        SELECT 1 FROM products p WHERE p.product_id = s.product_id)

    ORDER BY s.product_id;
    """))
    
    print(f"New products inserted: {product_result.rowcount}")

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
    #conn.execute(text("""
    #INSERT INTO orders
    #SELECT DISTINCT ON(order_id)
    #    order_id,
    #    TO_DATE(order_date, 'MM/DD/YYYY'),
    #    TO_DATE(ship_date, 'MM/DD/YYYY'),
    #    ship_mode,
    #    customer_id,
    #    region,
    #    postal_code
    #FROM superstore_raw
    #ORDER BY order_id;
    #"""))
    
    order_result = conn.execute(text("""
    
    INSERT INTO orders (
        order_id,
        order_date,
        ship_date,
        ship_mode,
        customer_id,
        region,
        postal_code
    )

    SELECT DISTINCT ON (s.order_id)
        s.order_id,
        TO_DATE(s.order_date, 'MM/DD/YYYY'),
        TO_DATE(s.ship_date, 'MM/DD/YYYY'),
        s.ship_mode,
        s.customer_id,
        s.region,
        s.postal_code
    FROM superstore_raw s 
    WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.order_id = s.order_id)

    ORDER BY s.order_id;
    """))
    
    print(f"New orders inserted: {order_result.rowcount}")

    # -------------------------------
    # LOAD ORDER ITEMS
    # -------------------------------

    #conn.execute(text("""
    #INSERT INTO order_items
    #SELECT
    #    row_id,
    #    order_id,
    #    product_id,
    #    sales,
    #    quantity,
    #    discount,
    #    profit
    #FROM superstore_raw;
    #"""))
    
    order_item_result = conn.execute(text("""
    
    INSERT INTO order_items (
        row_id,
        order_id,
        product_id,
        sales,
        quantity,
        discount,
        profit
    )

    SELECT
        s.row_id,
        s.order_id,
        s.product_id,
        s.sales,
        s.quantity,
        s.discount,
        s.profit
    FROM superstore_raw s WHERE NOT EXISTS (
        SELECT 1 FROM order_items oi WHERE oi.row_id = s.row_id);
    """))
    print(f"New order items inserted: {order_item_result.rowcount}")
    
conn.commit()

#print("ETL pipeline executed successfully")
    
#print("ETL pipeline executed successfully")

total_new_rows = (
        customer_result.rowcount +
        product_result.rowcount +
        order_result.rowcount +
        order_item_result.rowcount
    )

print(f"Total new rows inserted: {total_new_rows}")

if total_new_rows == 0:
        print("No new records found")

else:
        print("Incremental load completed successfully")

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

#result = conn.execute(text("SELECT COUNT(*) FROM customers"))
#print(result.scalar())

print(validation)

print("Pipeline completed successfully")