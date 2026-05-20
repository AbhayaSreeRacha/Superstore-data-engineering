-- Product profitability ranking using DENSE_RANK()
select p.product_name, ROUND(SUM(oi.profit),2) AS Total_Profit, DENSE_RANK() OVER(order by SUM(oi.profit) DESC) AS Profit_Rank from products p join order_items oi on p.product_id = oi.product_id group by p.product_name;

-- Running revenue analysis Cumulative SUM
select date_trunc('month', o.order_date) AS month, ROUND(SUM(oi.sales),2) AS Monthly_Sales,  ROUND(SUM(SUM(oi.sales)) OVER(order by date_trunc('month', o.order_date)),2) AS Running_Revenue from orders o join order_items oi on o.order_id = oi.order_id group by date_trunc('month', o.order_date) order by month;

-- Regional sales benchmarking using PARTITION BY
select o.region, p.category, ROUND(SUM(oi.sales),2) AS Total_Sales, ROUND(AVG(SUM(oi.sales)) OVER(PARTITION BY o.region),2) AS Regional_Average_Sales from orders o join order_items oi on o.order_id = oi.order_id join products p on oi.product_id = p.product_id group by o.region, p.category;

-- Month-over-month sales comparison using LAG()
select month, monthly_sales, LAG(monthly_sales) OVER(order by month) AS Previous_Month_Sales from (select date_trunc('month', o.order_date) AS month, ROUND(SUM(oi.sales),2) AS Monthly_Sales from orders o join order_items oi on o.order_id = oi.order_id group by date_trunc('month', o.order_date))t;

-- Predictive revenue trend analysis using LEAD()
select month, monthly_sales, LEAD(monthly_sales) OVER(order by month) AS Next_Month_Sales from (select date_trunc('month',o.order_date) AS month, ROUND(SUM(oi.sales),2) AS Monthly_Sales from orders o join order_items oi on o.order_id = oi.order_id group by date_trunc('month',o.order_date))t;

-- Customer revenue segmentation using NTILE()
select c.customer_name, ROUND(SUM(oi.sales),2) AS Total_Sales, NTILE(4) OVER(order by SUM(oi.sales) DESC) AS Customer_Tier from customers c join orders o on c.customer_id = o.customer_id join order_items oi on o.order_id = oi.order_id group by c.customer_name;