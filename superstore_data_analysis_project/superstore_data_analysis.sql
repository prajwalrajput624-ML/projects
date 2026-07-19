DROP TABLE IF EXISTS superstore;

CREATE TABLE superstore (
    row_id INT PRIMARY KEY,
    order_id VARCHAR(25) NOT NULL,
    order_date DATE NOT NULL,
    ship_date DATE NOT NULL,
    ship_mode VARCHAR(25),
    customer_id VARCHAR(25),
    customer_name VARCHAR(50),
    segment VARCHAR(25),
    country VARCHAR(50),
    city VARCHAR(50),
    state VARCHAR(50),
    postal_code VARCHAR(20),
    region VARCHAR(25),
    product_id VARCHAR(25),
    category VARCHAR(25),
    sub_category VARCHAR(25),
    product_name VARCHAR(150),
    sales NUMERIC(10, 2),
    quantity INT,
    discount NUMERIC(4, 2),
    profit NUMERIC(10, 2)
);

-- 1.preview the dataset
SELECT * FROM superstore;

-- 2.dataset shape
SELECT COUNT(*) AS rows_counts
FROM superstore;

-- 3.Check How Many Unique Rows Present In Dataset
SELECT COUNT(DISTINCT row_id) AS unique_rows
FROM superstore;

-- 4.Check How Many Null Values Present In Dataset
SELECT COUNT(*) - COUNT(row_id) AS null_row_id,
COUNT(*) - COUNT(order_id) AS null_order_id,
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
COUNT(*) - COUNT(sales) AS null_sales,
COUNT(*) - COUNT(quantity) AS null_quantity,
COUNT(*) - COUNT(discount) AS null_discount,
COUNT(*) - COUNT(profit) AS null_profilt
FROM superstore;

-- 5.Check How Many Duplicates Rows Present In Dataset
SELECT row_id,order_id,order_date,ship_date,ship_mode,customer_id,
customer_name,segment,country,city,state,postal_code,region,product_id,
category,sub_category,product_name,sales,quantity,discount,profit,COUNT(*)
FROM superstore
GROUP BY row_id,order_id,order_date,ship_date,ship_mode,customer_id,
customer_name,segment,country,city,state,postal_code,region,product_id,
category,sub_category,product_name,sales,quantity,discount,profit
HAVING COUNT(*) > 1;

-- 6.Check The How Many objects columns Contains The white spaces and null blank In Dataset
SELECT COUNT(*) AS white_spaces_count
FROM superstore
WHERE LENGTH(TRIM(order_id)) = 0 
OR LENGTH(TRIM(ship_mode)) = 0
OR LENGTH(TRIM(customer_id)) = 0
OR LENGTH(TRIM(customer_name)) = 0
OR LENGTH(TRIM(segment)) = 0
OR LENGTH(TRIM(country)) = 0
OR LENGTH(TRIM(city)) = 0
OR LENGTH(TRIM(state)) = 0
OR LENGTH(TRIM(region)) = 0
OR LENGTH(TRIM(product_id)) = 0
OR LENGTH(TRIM(category)) = 0
OR LENGTH(TRIM(sub_category)) = 0
OR LENGTH(TRIM(product_name)) = 0;

-- 7.Convert All Object Columns In Lower-case
UPDATE superstore
SET order_id = LOWER(order_id),
ship_mode = LOWER(ship_mode),
customer_id = LOWER(customer_id),
customer_name = LOWER(customer_name),
segment = LOWER(segment),
country = LOWER(country),
city = LOWER(city),
state = LOWER(state),
region = LOWER(region),
product_id = LOWER(product_id),
category = LOWER(category),
sub_category = LOWER(sub_category),
product_name = LOWER(product_name);

-- 7.Check The order start and ending Year
SELECT MIN(order_date) AS start_order_year,
MAX(order_date) AS ending_order_year
FROM superstore;

-- 8.Check The ship date starting and ending year
SELECT MIN(ship_date) AS start_ship_year,
MAX(ship_date) AS ending_ship_year
FROM superstore;

-- 9.Check All Numeric Columns Stat Summary
SELECT AVG(sales) AS average,
MIN(sales) AS minimum_value,
STDDEV_SAMP(sales) AS std,
PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY sales) AS Q1,
PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY sales) AS Q2,
PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY sales) AS Q3,
MAX(sales) AS maximum_value
FROM superstore;

SELECT AVG(quantity) AS average,
MIN(quantity) AS minimum_value,
STDDEV_SAMP(quantity) AS std,
PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY quantity) AS Q1,
PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY quantity) AS Q2,
PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY quantity) AS Q3,
MAX(quantity) AS maximum_value
FROM superstore;

SELECT AVG(discount) AS average,
MIN(discount) AS minimum_value,
STDDEV_SAMP(discount) AS std,
PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY discount) AS Q1,
PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY discount) AS Q2,
PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY discount) AS Q3,
MAX(discount) AS maximum_value
FROM superstore;

-- 10.Check The Dataset size
SELECT pg_size_pretty(pg_total_relation_size('superstore')) AS total_size;
SELECT * FROM superstore;

-- 11.Check The Which Category is Most Frequent
SELECT category,COUNT(*) AS total_count
FROM superstore
GROUP BY category
ORDER BY COUNT(*) DESC LIMIT 1;

-- 12.Check The Which sub category is Most Frequent
SELECT sub_category,COUNT(*) AS total_sub_category_count
FROM superstore
GROUP BY sub_category
ORDER BY COUNT(*) DESC LIMIT 1;

-- 13.what is different between avergae sales and median sales
SELECT AVG(sales) -  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY sales) AS diff
FROM superstore;

-- 14.Check How Many Extremae Outliers Present In Dataset
SELECT * FROM superstore
WHERE sales > (SELECT AVG(sales) * 3 FROM superstore);

-- 15.what is total sales for each category
SELECT category,SUM(sales) AS total_sales,
COUNT(*)
FROM superstore
GROUP BY category
ORDER BY SUM(sales) DESC;

-- 16.what is total sales for sub category
SELECT sub_category,SUM(sales) AS total_sales,
COUNT(*) AS total_quantity
FROM superstore
GROUP BY sub_category
ORDER BY SUM(sales) DESC;

-- 17.Check The top 2 category in contribution is high in sales and also check profit
SELECT category,SUM(sales) AS total_sales,SUM(profit) AS total_profit,
COUNT(*) AS total_quantity
FROM superstore
GROUP BY category
ORDER BY SUM(sales) DESC LIMIT 2;

-- 18.Check The Top 5 sub category in contribution 
SELECT sub_category,SUM(sales) AS total_sales,SUM(profit) AS total_profit,
COUNT(*) AS total_quantity
FROM superstore
GROUP BY sub_category
ORDER BY SUM(sales) DESC LIMIT 5;

-- 19.Top 5 Lowest Sub category 
SELECT sub_category,SUM(sales) AS total_sales,
COUNT(*) AS total_quantity
FROM superstore
GROUP BY sub_category
ORDER BY SUM(sales) ASC LIMIT 5;

-- 20.Check The Which Top 5 product sales is high 
SELECT product_name,SUM(sales) AS total_sales
FROM superstore
GROUP BY product_name
ORDER BY SUM(sales) DESC LIMIT 5;

-- 21.Check The Which Top 5 Lowest Product sales is low
SELECT product_name,SUM(sales) AS total_sales
FROM superstore
GROUP BY product_name
ORDER BY SUM(sales) ASC LIMIT 5;

-- 22.which category contribution is high in sales
SELECT category,SUM(sales) AS total_sales,
	ROUND(SUM(sales) * 100.0 / SUM(SUM(sales)) OVER(),2) AS contribution_per
FROM superstore
GROUP BY category
ORDER BY contribution_per DESC;

-- 23.which sub category contribution is high in sales
SELECT sub_category,SUM(sales) AS total_sales,
	ROUND(SUM(sales) * 100.0 / SUM(SUM(sales)) OVER(),2) AS contribution_percentage
FROM superstore
GROUP BY sub_category
ORDER BY contribution_percentage DESC;

-- 24.Check The Which Product is Most Frequent
SELECT product_name,COUNT(*) AS total_quantity
FROM superstore
GROUP BY product_name
ORDER BY COUNT(*) DESC LIMIT 1;

-- 25.two layers breakdown category and sub category
SELECT category,sub_category,SUM(sales) AS total_sales
FROM superstore
GROUP BY category,sub_category
ORDER BY SUM(sales) DESC;

-- 26.what is the grand total and sub total for category
SELECT category,SUM(sales) AS total_sales
FROM superstore
GROUP BY ROLLUP(category)
ORDER BY SUM(sales) ASC;

-- 27.what is the grand total and sub total for sub category
SELECT sub_category,SUM(sales) AS total_sales
FROM superstore
GROUP BY ROLLUP(sub_category)
ORDER BY SUM(sales) ASC;

-- 28.Year wise sales distribution
SELECT EXTRACT(YEAR FROM order_date) AS year,
COUNT(*) AS total_quantity,SUM(sales) AS total_sales
FROM superstore
GROUP BY 1
ORDER BY 1;

-- 29.month wise sales distribution
SELECT TO_CHAR(order_date,'month') AS month,
COUNT(*) AS total_quantity,SUM(sales) AS total_sales
FROM superstore
GROUP BY 1
ORDER BY 1;

-- 30.quture wise sales distribution
SELECT TO_CHAR(order_date,'YYYY-"Q"Q') AS quters,
COUNT(*) AS total_qunatity,SUM(sales) AS total_sales
FROM superstore
GROUP BY 1
ORDER BY 1;

-- 31.day wise sales distribution
SELECT TO_CHAR(order_date,'day') AS day,
COUNT(*) AS total_qunatity,SUM(sales) AS total_sales
FROM superstore
GROUP BY 1
ORDER BY 1;

-- 32.check the which day sales is high weekend or weekday
SELECT CASE WHEN EXTRACT(ISODOW FROM order_date) 
IN(6,7) THEN 'weekend' ELSE 'weekday' END AS day_type,
SUM(sales) AS total_sales
FROM superstore
GROUP BY 1;

-- 33.check the year wise profit
SELECT EXTRACT(YEAR FROM order_date) AS profit_year,
COUNT(*) AS total_quantity,SUM(profit) AS total_profit
FROM superstore
GROUP BY 1
ORDER BY 1;

-- 34.check the quanter wise profit
SELECT TO_CHAR(order_date,'YYYY-"Q"Q') AS profit_quanter,
COUNT(*) AS total_quantity,SUM(profit) AS total_profit
FROM superstore
GROUP BY 1
ORDER BY 1;

-- 35.check the month wise profit
SELECT TO_CHAR(order_date,'month') AS profit_month,
COUNT(*) AS total_quantity,SUM(profit) AS total_profit
FROM superstore
GROUP BY 1
ORDER BY 1;

-- 36.check the day wise profit
SELECT TO_CHAR(order_date,'day') AS profit_day,
COUNT(*) AS total_quantity,SUM(profit) AS total_profit
FROM superstore
GROUP BY 1
ORDER BY 1;

-- 37.check the which day profit is high weekday or weekend
SELECT CASE WHEN EXTRACT(ISODOW FROM order_date) 
IN (6,7) THEN 'weekend' ELSE 'weekday' END AS day_type,
SUM(profit) AS total_profit
FROM superstore
GROUP BY 1;

-- 38.check the year wise running total sales
SELECT EXTRACT(YEAR FROM order_date) AS year,sales,SUM(sales) AS total_sales
OVER(ORDER BY EXTRACT(YEAR FROM order_date)) AS running_total
FROM superstore;

-- 39.check the month wise running total sales
SELECT EXTRACT(MONTH FROM order_date) AS month,sales,SUM(sales) AS total_sales
OVER(ORDER BY EXTRACT(MONTH FROM order_date)) AS running_month_total
FROM superstore;

-- 40.What are the top 3 highest-value transactions in each category
SELECT * FROM (SELECT customer_id,category,sales,
RANK() OVER(PARTITION BY category ORDER BY sales DESC) AS rnk
FROM superstore)
WHERE rnk <= 3;

-- 41.what are the top 5 highest value transactions in each sub category
SELECT * FROM (SELECT customer_id,sub_category,sales,
RANK() OVER(PARTITION BY sub_category ORDER BY sales DESC) AS rnk
FROM superstore)
WHERE rnk <= 5;

-- 42.check 3rd highest sales in category
SELECT * FROM (SELECT category,sales,
DENSE_RANK() OVER(PARTITION BY category ORDER BY sales DESC) AS rnk
FROM superstore)
WHERE rnk = 3;

-- 43.check the year wise growth
SELECT year,total,
	ROUND((total - LAG(total) OVER(ORDER BY year)) * 100.0 / LAG(total) OVER(ORDER BY year),2) AS year_growth
FROM(
	SELECT EXTRACT(YEAR FROM order_date) AS year,SUM(sales) AS total FROM superstore GROUP BY 1
	) t;

-- 44.check the month to month growth of sales
SELECT month,total,
	ROUND((total - LAG(total) OVER(ORDER BY month)) * 100.0 / LAG(total) OVER(ORDER BY month),2) AS month_growth
FROM(
	SELECT EXTRACT(MONTH FROM order_date) AS month,SUM(sales) AS total FROM superstore GROUP BY 1
	) t;

-- 45.check the year to year profit growth
SELECT year,total,
	ROUND((total - LAG(total) OVER(ORDER BY year)) * 100.0 / LAG(total) OVER(ORDER BY year),2) AS year_wise_profit_growth
FROM (
	SELECT EXTRACT(YEAR FROM order_date) AS year,SUM(profit) AS total FROM superstore GROUP BY 1
	) t;

-- 46.check the month to month profit growth
SELECT month,total,
	ROUND((total - LAG(total) OVER(ORDER BY month)) * 100.0 / LAG(total) OVER(ORDER BY month),2) AS month_wise_profi_growth
FROM (
	SELECT EXTRACT(MONTH FROM order_date) AS month,SUM(profit) as total FROM superstore GROUP BY 1
	) t;

-- 47.What was the gap of days between each transaction
SELECT customer_id,order_date,
	order_date - LAG(order_date) OVER(PARTITION BY customer_id ORDER BY order_date) AS days_since_lasy
FROM superstore;

-- 48.Check The Which Ship mode is most freqeunt
SELECT ship_mode,COUNT(*) AS most_frequent
FROM superstore
GROUP BY ship_mode
ORDER BY COUNT(*) DESC LIMIT 1;

-- 49.Check The ship mode wise total sales
SELECT ship_mode,SUM(sales) AS total_sales,
COUNT(*) AS total_quantity
FROM superstore
GROUP BY ship_mode
ORDER BY SUM(sales) DESC;

-- 50.check the ship mode wise sales and category distribution
SELECT category,ship_mode,SUM(sales) AS total_sales,
COUNT(*) AS total_quantity
FROM superstore
GROUP BY category,ship_mode
ORDER BY SUM(sales) DESC;

-- 51.check the which segment is most frequent 
SELECT segment,COUNT(*) AS most_frequent
FROM superstore
GROUP BY segment
ORDER BY COUNT(*) DESC LIMIT 1;

-- 52.Check The segment wise total sales
SELECT segment,SUM(sales) AS total_sales,
COUNT(*) AS total_quantity
FROM superstore
GROUP BY segment
ORDER BY SUM(sales) DESC;

-- 53.Check The Top 10 Most frequent city and there total sales
SELECT city,SUM(sales) AS total_sales,
COUNT(*) AS total_quantity
FROM superstore
GROUP BY city
ORDER BY SUM(sales) DESC LIMIT 10;

-- 54.Check the state wise total sales
SELECT state,SUM(sales) AS total_sales,
COUNT(*) AS total_quantity
FROM superstore
GROUP BY state
ORDER BY SUM(sales) DESC;

-- 55.Check the region wise total sales
SELECT region,SUM(sales) AS total_sales,
COUNT(*) AS total_quantity
FROM superstore
GROUP BY region
ORDER BY SUM(sales) DESC;

-- 56.Preview The Dataset
SELECT * FROM superstore;


-- total 2739 unqiue records in dataset
-- dataset Not Contains Any Missing Values
-- dataset Not Contains Any Duplicates Rows
-- sales data column is right skewd and outliers and high spread
-- quantity column data is normal distributed and high spread and contains too many outliers
-- discount column data is left skewd and high spread

-- Insights:-

-- total 2739 unqiue records in dataset
-- order start year is 02/01/2014 and order ending year is 11/12/2017
-- ship date start year is 05/02/2014 and ending year is 12/12/2017
-- sales average value is 230.9713 and median value is 58.24 
-- Dataset size is 1544kb
-- in category column office supplies is most frequent category
-- binders is sub category that is most frequent in dataset
-- average sales and median sales diff is 172.7313
-- technology sales is 256390.09 and total quantity 520,furniture sales is 200920.67 and total quantity 577 and office supplies quantity is 1642 but sales is down is 175319.89
-- sub category sales distribution,
/*
sub category total sales total quantity
"chairs"		90947.35	169
"phones"		83805.55	237
"machines"		74140.44	38
"storage"		54722.14	234
"tables"		53592.58	90
"copiers"		49409.33	24
"accessories"	49034.77	221
"binders"		42929.38	421
"bookcases"		31091.82	57
"appliances"	27771.97	123
"furnishings"	25288.92	261
"paper"			20967.64	380
"supplies"		11755.16	43
"art"			8846.98		212
"envelopes"		3920.27		64
"labels"		3615.51		107
"fasteners"		790.84		58
*/
-- tehncolory and fruniture are Top 2 category that contribution is high in sales and technolory total profit is 50753.99 and furniture total profit is 8025.58
-- top 5 sub category contribution in sales and profit,
/*
sub category total sales total profit total quantity
"chairs"		90947.35	9980.29	 	169
"phones"		83805.55	12302.38	237
"machines"		74140.44	5858.99		38
"storage"		54722.14	6488.04		234
"tables"		53592.58	-3456.94	90
*/

-- top 5 lowst sub category,
/*
sub category total sales total quantity
"fasteners"		790.84		58
"labels"		3615.51		107
"envelopes"		3920.27		64
"art"			8846.98		212
"supplies"		11755.16	43
*/

-- top 5 product that contribution is high in sales
/*
product name                             						  total sales 
"canon imageclass 2200 advanced copier"								17499.95
"lexmark mx611dhe monochrome laser printer"							11219.93
"hp designjet t520 inkjet large format printer - 24"" color"		8749.95
"riverside palais royal lawyers bookcase, royale cherry finish"		8298.84
"hewlett packard laserjet 3310 copier"								8159.86
*/

-- top 5 lowest product is sales is low
/*
product name                                                       total sales
"self-adhesive ring binder labels"									   1.41
"avery triangle shaped sheet lifters, black, 2/pack"				   1.48
"eureka disposable bags for sanitaire vibra groomer i upright vac"	   1.62
"avery hidden tab dividers for binding systems"						   1.79
"acco banker's clasps, 5 3/4""-long"	2.30
*/

-- category wise contribution in sales
/*
category 			total sales 	contribution percentage
"technology"		256390.09				40.53%
"furniture"			200920.67				31.76%
"office supplies"	175319.89				27.71%
*/

-- sub category wise contribution in sales
/*
sub category 	total sales 	contribution percentage
"chairs"		90947.35				14.38
"phones"		83805.55				13.25
"machines"		74140.44				11.72
"storage"		54722.14				8.65
"tables"		53592.58				8.47
"copiers"		49409.33				7.81
"accessories"	49034.77				7.75
"binders"		42929.38				6.79
"bookcases"		31091.82				4.91
"appliances"	27771.97				4.39
"furnishings"	25288.92				4.00
"paper"			20967.64				3.31
"supplies"		11755.16				1.86
"art"			8846.98					1.40
"envelopes"		3920.27					0.62
"labels"		3615.51					0.57
"fasteners"		790.84					0.13
*/

-- Most frequent product is easy staple paper quantity is 21
-- two layers breakdown category and sub category distribution for sales
/*
category                 	sub category   total sales
"furniture"					"chairs"		90947.35
"technology"				"phones"		83805.55
"technology"				"machines"		74140.44
"office supplies"			"storage"		54722.14
"furniture"					"tables"		53592.58
"technology"				"copiers"		49409.33
"technology"				"accessories"	49034.77
"office supplies"			"binders"		42929.38
"furniture"					"bookcases"		31091.82
"office supplies"			"appliances"	27771.97
"furniture"					"furnishings"	25288.92
"office supplies"			"paper"			20967.64
"office supplies"			"supplies"		11755.16
"office supplies"			"art"			8846.98
"office supplies"			"envelopes"		3920.27
"office supplies"			"labels"		3615.51
"office supplies"			"fasteners"		790.84
*/

-- grand total and sub total of each category for sales
/* 
category 					total sales
"office supplies"			 175319.89
"furniture"					 200920.67
"technology"				 256390.09
grand total					 632630.65
*/

-- grand total and sub total of each sub category for sales
/*
sub category         total sales
"fasteners"	          790.84
"labels"	          3615.51
"envelopes"	          3920.27
"art"				  8846.98
"supplies"			  11755.16
"paper"				  20967.64
"furnishings"		  25288.92
"appliances"	      27771.97
"bookcases"			  31091.82
"binders"			  42929.38
"accessories"		  49034.77          
"copiers"	          49409.33
"tables"	          53592.58
"storage"	          54722.14
"machines"	          74140.44
"phones"	          83805.55
"chairs"	          90947.35
grand total		      632630.65
*/

-- Year wise sales distribution
/*
Year    total sales
2014	110303.97
2015	116978.37
2016	203260.25
2017	202088.06
*/

-- Month wise sales distirbution
/* 
month          total quantity   total sales 
"april    "	      308	        68162.30
"august   "	      210	        69297.31
"december "	      17	        4710.63
"february "	      379	        105139.10
"january  "	      337	        95524.55
"july     "	      261	        53903.39
"june     "	      264	        47092.21
"march    "	      365	        72319.95
"may      "	      366	        64520.53
"november "	      60	        14585.22
"october  "	      66	        13519.52
"september"	      106	        23855.94
*/

-- quanter wise sales distrbution
/*
quanter       total quantity  total sales
"2014-Q1"	   199	          38633.72
"2014-Q2"	   195	          39579.84
"2014-Q3"	   105	          31316.66
"2014-Q4"	   7	          773.75
"2015-Q1"	   192	          42927.38
"2015-Q2"	   193	          32692.79
"2015-Q3"	   134	          34058.09
"2015-Q4"	   30	          7300.11
"2016-Q1"	   280	          95694.66
"2016-Q2"	   286	          60151.86
"2016-Q3"	   133	          36071.57
"2016-Q4"	   46	          11342.16
"2017-Q1"	   410	          95727.84
"2017-Q2"	   264	          47350.55
"2017-Q3"	   205	          45610.32
"2017-Q4"	   60	          13399.35
*/

-- day wise sales distribution
/*
day 	total quantity  total sales
"friday   "	371		 	73439.74
"monday   "	458			89180.33
"saturday "	393			91003.62
"sunday   "	427			95435.95
"thursday "	416			87462.15
"tuesday  "	355			106278.31
"wednesday"	319		    89830.55
*/

-- weekend and weekday sales distribution
/*
Day Type    Total Sales
"weekend"	186439.57
"weekday"	446191.08
*/

-- Year wise Profit Distribution
/*
profit year total quantity    total profit
2014	     506	      		13820.21
2015	     549				12555.82
2016	     745				36504.52
2017	     939				22920.71
*/

-- quanter wise profit distribution
/*
profit quanter  total quantity total profit
2014				506			13820.21
2015				549			12555.82
2016				745			36504.52
2017	939	22920.71
*/

-- month wise profit distribution
/*
profit month  total quantity total profit
"april    "	          308	6873.67
"august   "	          210	6976.92
"december "	          17	82.11
"february "	          379	19441.11
"january  "	          337	17006.78
"july     "	          261	6716.54
"june     "	          264	6746.37
"march    "	          365	7090.50
"may      "	          366	7498.33
"november "	          60	1416.73
"october  "	          66	844.02
"september"	          106	5108.18
*/

-- day wise profit distribution
/*
profit day  total quantity total profit
"friday   "	     371	 	9130.97
"monday   "	     458		13018.49
"saturday "	     393		10004.40
"sunday   "	     427		10258.03
"thursday "	     416		10674.14
"tuesday  "	     355		15526.26
"wednesday"	     319		17188.97
*/

-- weekend and weekday profit distribution
/*
day type   total profit
"weekend"	20262.43
"weekday"	65538.83
*/

-- top 3 highest-value transactions in each category
/*
customer id  category           sales     rank
"qj-19255"	"furniture"	        4404.90		1
"rp-19390"	"furniture"			2807.84		2
"cj-12010"	"furniture"			2803.92		3
"ab-10060"	"office supplies"	4355.17		1
"gm-14695"	"office supplies"	4164.05		2
"aa-10315"	"office supplies"	3930.07		3
"tc-20980"	"technology"		17499.95	1
"se-20110"	"technology"		8749.95		2
"bm-11140"	"technology"		8159.95		3
*/

-- 3rd highest sales in category
/*
category           sales       rank
"furniture"			2803.92		3
"office supplies"	3930.07		3
"technology"		8159.95		3
*/

-- year wise growth in (%)
/*
year   total sales  year growth
2014	110303.97	0%
2015	116978.37	6.05%
2016	203260.25	73.76%
2017	202088.06	-0.58%
*/

-- month wise growth in (%)
/*
month  total sales mpnth growth
1	     95524.55	  0%
2	     105139.10	  10.07%
3	     72319.95	  -31.21%
4	     68162.30	  -5.75%
5	     64520.53	  -5.34%
6	     47092.21	  -27.01%
7	     53903.39	  14.46%
8	     69297.31	  28.56%
9	     23855.94	  -65.57%
10	     13519.52	  -43.33%
11	     14585.22	   7.88%
12	     4710.63	  -67.70%
*/

-- year wise profit growth
/*
year  total profit  year to year profit growth
2014	13820.21	 0%
2015	12555.82	-9.15%
2016	36504.52	190.74%
2017	22920.71	-37.21%
*/

-- month to month profit growth
/*
month  total profit month to month profit growth
1	     17006.78	0%
2	     19441.11	14.31%
3	     7090.50	-63.53%
4	     6873.67	-3.06%
5	     7498.33	9.09%
6	     6746.37	-10.03%
7	     6716.54	-0.44%
8	     6976.92	3.88%
9	     5108.18	-26.78%
10	     844.02	   	-83.48%
11	     1416.73	67.86%
12	     82.11	    -94.20%
*/

-- in ship mode standard class is most frequent mode in sales
-- ship mode wise total sales
/*
ship mode         total sales   total quantity
"standard class"	325757.76	1418
"second class"		130162.18	541
"first class"		115933.54	535
"same day"			60777.17	245
*/

-- segment wise total sales
/*
sgment        total sales  total quantity
"consumer"		295429.78	1411
"corporate"		205852.12	809
"home office"	131348.75	519
*/

-- Top 10 Most frequent city and there total sales
/*
city             total sales  total quantity
"new york city"		73774.44	280
"los angeles"		49429.38	199
"san francisco"		31053.83	134
"seattle"			25284.14	113
"philadelphia"		22804.21	154
"lafayette"			18948.79	12
"houston"			18097.20	114
"burlington"		14796.85	7
"san antonio"		14219.96	31
"henderson"			13428.74	27
*/

-- state wise total sales distribution
/*
state				 total sales total quantity
"california"			122989.25	530
"new york"				91708.18	340
"texas"					59888.85	301
"washington"			33278.68	136
"indiana"				28937.85	44
"virginia"				26156.82	68
"north carolina"		25788.60	96
"pennsylvania"			23283.41	159
"florida"				21656.10	108
"michigan"				18245.24	76
"kentucky"				17050.67	55
"ohio"					14883.67	122
"wisconsin"				14284.47	30
"illinois"				13040.06	114
"massachusetts"			11107.83	44
"rhode island"			9736.71		16
"colorado"				8219.27		53
"minnesota"				8068.96		31
"georgia"				7962.24		42
"maryland"				7549.57		28
"tennessee"				6896.98		45
"arizona"				6857.07		50
"vermont"				6619.88		4
"delaware"				4977.75		32
"oregon"				4805.37		31
"arkansas"				4229.78		19
"connecticut"			4012.65		19
"oklahoma"				4004.65		14
"utah"					3942.41		13
"nevada"				3058.15	    7
"nebraska"				3036.87		9
"missouri"				2068.13		17
"mississippi"			1725.92		9
"new jersey"			1689.73		19
"wyoming"				1603.14		1
"new hampshire"			1539.23		7
"alabama"				1459.51	  	6
"south carolina"		1384.18	  	8
"new mexico"			1003.06	  	4
"iowa"					874.20	  	7
"idaho"					806.78	  	6
"louisiana"				699.33	  	8
"west virginia"			673.34	  	1
"maine"					617.12	  	3
"kansas"				175.07	  	6
"district of columbia"	33.92	  	1
*/

-- region wise total sales
/*
region  	total sales  total quantity
"west"		186563.18		831
"east"		178432.99		795
"central"	152624.35		649
"south"		115010.13		464
*/