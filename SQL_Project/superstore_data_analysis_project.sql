DROP TABLE IF EXISTS sales_data;

CREATE TABLE sales_data (
    row_id BIGINT PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    order_date DATE NOT NULL,
    ship_date DATE NOT NULL,
    ship_mode VARCHAR(50),
    customer_id VARCHAR(50),
    customer_name VARCHAR(100),
    segment VARCHAR(50),
    country VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code VARCHAR(20),
    region VARCHAR(50),
    product_id VARCHAR(50),
    category VARCHAR(100),
    sub_category VARCHAR(100),
    product_name VARCHAR(255),
    sales NUMERIC(12, 2)
);
-- 1.Preview The Dataset
SELECT * FROM sales_data;

-- 2.Dataset Shape
SELECT COUNT(*) AS row_count
FROM sales_data;

-- 3.Check How Many Unqiue Values Present In Dataset
SELECT COUNT(DISTINCT order_id) AS unique_rows
FROM sales_data;

-- 4.Check How Many Null Values Present In Dataset
SELECT COUNT(*) - COUNT(order_id) AS null_order_id,
COUNT(*) - COUNT(order_date) AS null_order_date,
COUNT(*) - COUNT(ship_date) AS null_ship_date,
COUNT(*) - COUNT(ship_mode) AS null_ship_mode,
COUNT(*) - COUNT(customer_id) AS null_customer_id,
COUNT(*) - COUNT(customer_name) AS null_customer_name,
COUNT(*) - COUNT(segment) AS null_segment,
COUNT(*) - COUNT(country) AS null_country,
COUNT(*) - COUNT(city) AS null_city,
COUNT(*) - COUNT(state) AS null_state,
COUNT(*) - COUNT(postal_code) AS null_postal_code,
COUNT(*) - COUNT(region) AS null_region,
COUNT(*) - COUNT(product_id) AS null_product_id,
COUNT(*) - COUNT(category) AS null_category,
COUNT(*) - COUNT(sub_category) AS null_sub_category,
COUNT(*) - COUNT(product_name) AS null_product_name,
COUNT(*) - COUNT(sales) AS null_sales
FROM sales_data;

-- 5.Check How Many Duplicates Rows Present In Dataset
SELECT SUM(duplicate_count - 1) AS total_extra_duplicate_rows
FROM (
    SELECT COUNT(*) AS duplicate_count
    FROM sales_data
    GROUP BY order_id, order_date, ship_date, ship_mode, customer_id, customer_name, segment, country, city, state, postal_code, region, product_id, category, sub_category, product_name, sales
    HAVING COUNT(*) > 1
) AS duplicate_groups;

-- 6.Remove Duplicates Rows 
WITH CTE_Duplicates AS (
    SELECT ctid,
           ROW_NUMBER() OVER (
               PARTITION BY order_id, order_date, ship_date, ship_mode, customer_id, customer_name, segment, country, city, state, postal_code, region, product_id, category, sub_category, product_name, sales
               ORDER BY order_id
           ) AS rnk
    FROM sales_data
)
DELETE FROM sales_data
USING CTE_Duplicates
WHERE sales_data.ctid = CTE_Duplicates.ctid
  AND rnk > 1;

-- 7.Fill The Missing Values 
UPDATE sales_data
SET postal_code = COALESCE(postal_code,'missing') 
WHERE postal_code IS NULL;

-- 8.Check How Many object columns Contains white spaces and blank
SELECT COUNT(*) FROM sales_data
WHERE LENGTH(TRIM(order_id)) = 0 OR
LENGTH(TRIM(ship_mode)) = 0 OR 
LENGTH(TRIM(customer_id)) = 0 OR
LENGTH(TRIM(customer_name)) = 0 OR
LENGTH(TRIM(segment)) = 0 OR
LENGTH(TRIM(country)) = 0 OR
LENGTH(TRIM(city)) = 0 OR
LENGTH(TRIM(state)) = 0 OR
LENGTH(TRIM(region)) = 0 OR
LENGTH(TRIM(product_id)) = 0 OR
LENGTH(TRIM(category)) = 0 OR
LENGTH(TRIM(sub_category)) = 0 OR
LENGTH(TRIM(product_name)) =  0;

-- 9.Columns Preprocessing
UPDATE sales_data
SET order_id = TRIM(LOWER(order_id)),
	ship_mode = TRIM(LOWER(ship_mode)),
	customer_id = TRIM(LOWER(customer_id)),
	customer_name = TRIM(LOWER(customer_name)),
	segment = TRIM(LOWER(segment)),
	country = TRIM(LOWER(country)),
	city = TRIM(LOWER(city)),
	state = TRIM(LOWER(state)),
	region = TRIM(LOWER(region)),
	product_id = TRIM(LOWER(product_id)),
	category = TRIM(LOWER(category)),
	sub_category = TRIM(LOWER(sub_category)),
	product_name = TRIM(LOWER(product_name));

-- 10.Check numeric columns statistical Summary
SELECT COUNT(sales) AS count_sales,
AVG(sales) AS average_sales,
MIN(sales) AS minimum_sales,
STDDEV_SAMP(sales) AS std_sales,
PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY sales) AS Q1,
PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY sales) AS Q2,
PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY sales) AS Q3,
MAX(sales) AS maximum_sales
FROM sales_data;

-- 11.outliers detection
SELECT * FROM sales_data
WHERE sales > (SELECT AVG(sales) * 3 FROM sales_data);
SELECT * FROM sales_data;

-- 12.Check Starting And Ending Year for order date
SELECT MIN(order_date) AS start_year,
MAX(order_date) AS ending_year
FROM sales_data;

-- 13.Check Starting And Ending Year for Ship date
SELECT MIN(ship_date) AS starting_ship_year,
MAX(ship_date) AS ending_ship_year
FROM sales_data;

-- 14.Check which category is most frequent in sales
SELECT category,COUNT(*)
FROM sales_data
GROUP BY category
ORDER BY COUNT(*) DESC LIMIT 1;

-- 15.Check The Dataset Size
SELECT pg_size_pretty(pg_total_relation_size('sales_data')) AS total_size;

-- 16.What is the difference between mean and median
SELECT AVG(sales) - PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY sales) AS diff
FROM sales_data;

-- 17..What is the percentage (%) contribution of each category to the total business
SELECT category,SUM(sales),
	ROUND(SUM(sales) * 100.0 / SUM(SUM(sales)) OVER(),2) AS percentage_share
FROM sales_data
GROUP BY category
ORDER BY percentage_share DESC;

-- 18.What is the percentage contribution of each sub category to the total business
SELECT sub_category,SUM(sales),
	ROUND(SUM(sales) * 100.0 / SUM(SUM(sales)) OVER(),2) AS percentage_share
FROM sales_data
GROUP BY sub_category
ORDER BY percentage_share DESC;

-- 19.Check Both category and sub_category percentage contribution of total business
SELECT category,sub_category,SUM(sales) AS total_sales,
	ROUND(SUM(sales) * 100.0 / SUM(SUM(sales)) OVER(),2) AS percentage_share_category_and_sub_category
FROM sales_data
GROUP BY category,sub_category
ORDER BY percentage_share_category_and_sub_category DESC;

-- 20.Check Top 2 Highest category In sales
SELECT category,SUM(sales) AS total_sales
FROM sales_data
GROUP BY category
ORDER BY total_sales DESC LIMIT 2;

-- 21.Check Top 5 Highest sub category in sales
SELECT sub_category,SUM(sales) AS total_sub_category_sales
FROM sales_data
GROUP BY sub_category
ORDER BY total_sub_category_sales DESC LIMIT 5;

-- 22.Check Top 5 Lowest sub category in sales
SELECT sub_category,SUM(sales) AS total_sales_lowest
FROM sales_data
GROUP BY sub_category
ORDER BY total_sales_lowest ASC LIMIT 5;

-- 23.Check Which Product is Most Frequent
SELECT product_name,COUNT(*) AS count_of_product
FROM sales_data
GROUP BY product_name
ORDER BY COUNT(*) DESC LIMIT 1;

-- 24.Check Top 5 Product Contirubution in sales
SELECT product_name,SUM(sales) AS total_sale
FROM sales_data
GROUP BY product_name
ORDER BY total_sale DESC LIMIT 5;

-- 25.Check The top 5 product contribution in sales contains category and sub category
SELECT product_name,category,sub_category,SUM(sales),
	ROUND(SUM(sales) * 100.0 / SUM(SUM(sales)) OVER(),2) AS percentage_share
FROM sales_data
GROUP BY product_name,category,sub_category
ORDER BY percentage_share DESC LIMIT 5;

-- 26.Check order Yearly Sales
SELECT EXTRACT(YEAR FROM order_date) AS order_year,
COUNT(*) AS total_quantity,SUM(sales) AS total_sales
FROM sales_data
GROUP BY 1
ORDER BY 2;

-- 27.Check quarter Wise sales
SELECT TO_CHAR(order_date,'YYYY-"Q"Q') AS quarter,
COUNT(*) AS total_quantity,SUM(sales) AS total_sales
FROM sales_data
GROUP BY 1
ORDER BY 1;

-- 28.Check Months Wise Sales
SELECT TO_CHAR(order_date,'month') AS month_wise,
COUNT(*) AS total_qunatity,SUM(sales) AS total_sales
FROM sales_data
GROUP BY 1
ORDER BY 1;

-- 29.Check Day Wise Sales
SELECT TO_CHAR(order_date,'day') AS day_wise,
COUNT(*) AS total_quantity,SUM(sales) AS total_sales
FROM sales_data
GROUP BY 1
ORDER BY 1;

-- 30.Check sales is high in weekday or weekend
SELECT CASE WHEN EXTRACT(ISODOW FROM order_date)
IN(6,7) THEN 'weekend' ELSE 'weekday' END AS day_type,
SUM(sales) AS total_sales
FROM sales_data
GROUP BY 1;

-- 31.Check Year Wise Growth of Sales
SELECT
	year,
	total,
	ROUND(
			(total - LAG(total) OVER(ORDER BY year)) * 100.0 /
			LAG(total) OVER(ORDER BY year),
			2
	) AS Year_to_Year_Growth
FROM (SELECT
		EXTRACT(YEAR FROM order_date) AS year,
		SUM(sales) AS total 
	FROM sales_data 
	GROUP BY 1
) t
ORDER BY year;
	

-- 32.Check Month to Month Growth of Sales
SELECT 
    month_name AS month,
    total, 
    ROUND(
        (total - LAG(total) OVER(ORDER BY month_num)) * 100.0 / 
        LAG(total) OVER (ORDER BY month_num), 
        2
    ) AS Month_to_Month_Growth 
FROM ( 
    SELECT 
        TO_CHAR(order_date, 'Month') AS month_name,
        EXTRACT(MONTH FROM order_date) AS month_num,
        SUM(sales) AS total 
    FROM sales_data 
    GROUP BY month_name,month_num
) t
ORDER BY month_num;

-- 33.Check The yearly Running Total 
SELECT EXTRACT(YEAR FROM order_date) AS year,sales,SUM(sales)
OVER(ORDER BY EXTRACT(YEAR FROM order_date)) AS running_total
FROM sales_data;

-- 34.Check The Monthly Running Total
SELECT TO_CHAR(order_date,'month') AS month,sales,SUM(sales)
OVER(ORDER BY EXTRACT(MONTH FROM order_date)) AS running_month_total
FROM sales_data;

-- 35.What is the highest Transcation in Each Category
SELECT * FROM (SELECT customer_id,category,sales,
DENSE_RANK() OVER(PARTITION BY category ORDER BY sales DESC) AS rnk
FROM sales_data) t
WHERE rnk <= 3;

-- 36.What is The Highest Transcation in Each Sub_category
SELECT * FROM (
				SELECT customer_id,sub_category,sales,
					DENSE_RANK() OVER(PARTITION BY sub_category ORDER BY sales DESC) AS rnk
				FROM sales_data 
				) t
WHERE rnk <= 3;

-- 37.What was The gap of days between each trasncation
SELECT customer_name,order_date,
	order_date - LAG(order_date) OVER(PARTITION BY customer_name ORDER BY order_date)
FROM sales_data;

-- 38..What is the percentage relationship of each record to the total sum of its category
SELECT customer_id,category,sales,
	ROUND(sales * 100.0 / SUM(sales) OVER (PARTITION BY category),2) AS pct_of_category
FROM sales_data;

-- 39.what is the percentage relationship of each record to the total sum of its sub category
SELECT customer_id,sub_category,sales,
	ROUND(sales * 100.0 / SUM(sales) OVER (PARTITION BY sub_category),2) AS pct_of_sub_category
FROM sales_data;

-- 40.Show The All Dataset Rows And Columns
SELECT * FROM sales_data;
