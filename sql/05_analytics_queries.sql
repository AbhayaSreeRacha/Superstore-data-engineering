--Total Revenue Analysis
SELECT SUM(sales) AS total_sales FROM order_items;

--Top Revenue Generating Products
SELECT product_id, SUM(sales) AS revenue FROM order_items GROUP BY product_id ORDER BY revenue DESC LIMIT 10;

--Regional Sales Performance Analysis
SELECT region, SUM(sales) AS Total_Sales FROM superstore_raw GROUP BY region;

-- Customer Segment Profitability Analysis
SELECT segment, SUM(sales) as Total_Sales FROM superstore_raw GROUP BY segment;

-- Monthly Revenue Trend Analysis
SELECT DATE_TRUNC('month', order_date) AS month, SUM(sales) AS monthly_sales, SUM(profit) AS monthly_profit FROM orders JOIN order_items USING (order_id) GROUP BY month ORDER BY month LIMIT 12;