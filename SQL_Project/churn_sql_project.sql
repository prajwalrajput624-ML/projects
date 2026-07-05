SELECT 
    AVG(customer_age) AS customer_average_age, 
    AVG(tenure) AS customer_average_tenure, 
    AVG(usage_frequency) AS customer_average_usage_frequency, 
    AVG(support_calls) AS customer_average_support_calls, 
    AVG(payment_delay) AS customer_average_payment_delay, 
    AVG(total_spend) AS customer_average_total_spend, 
    AVG(last_intraction) AS customer_average_last_intraction 
FROM churn_data;

SELECT 
    churn,
    gender,
    customer_age,
    COUNT(*) AS customer_age_count 
FROM churn_data 
WHERE churn = 1 
  AND customer_age >= (SELECT AVG(customer_age) FROM churn_data) 
  AND gender IN ('Male', 'Female') 
GROUP BY churn, gender, customer_age
ORDER BY customer_age DESC;

SELECT 
    churn,
    gender,
    tenure,
    COUNT(*) AS customer_tenure_count 
FROM churn_data 
WHERE churn IN (0, 1) 
  AND gender IN ('Male', 'Female') 
  AND tenure >= (SELECT AVG(tenure) FROM churn_data) 
GROUP BY churn, gender, tenure 
ORDER BY customer_tenure_count DESC;


SELECT gender,churn,ROUND(AVG(customer_age)) AS average_customer_age
FROM churn_data
GROUP BY gender,churn;

SELECT gender,churn,ROUND(AVG(tenure)) AS average_customer_tenure
FROM churn_data
GROUP BY gender,churn;

SELECT gender,churn,COUNT(*) AS total_churn_customers
FROM churn_data
WHERE churn = 1
GROUP BY gender,churn
ORDER BY total_churn_customers;

SELECT gender,churn,ROUND(AVG(support_calls)) AS Average_support_calls
FROM churn_data
GROUP BY gender,churn;

SELECT gender,churn,support_calls,COUNT(*) AS total_support_calls
FROM churn_data
WHERE support_calls >= (SELECT AVG(support_calls) FROM churn_data)
AND churn = 1
GROUP BY gender,churn,support_calls;

SELECT gender,churn,ROUND(AVG(payment_delay)) AS Average_payment_delay
FROM churn_data
GROUP BY gender,churn
ORDER BY Average_payment_delay DESC;

SELECT gender,churn,payment_delay,COUNT(*) AS total_payment_delay
FROM churn_data
WHERE payment_delay >= (SELECT AVG(payment_delay) FROM churn_data)
AND churn = 1
GROUP BY gender,churn,payment_delay
ORDER BY payment_delay DESC;

SELECT gender,churn,usage_frequency,COUNT(*) AS total_usage_frequency
FROM churn_data
WHERE churn = 1 AND usage_frequency >= (SELECT AVG(usage_frequency) FROM churn_data)
GROUP BY gender,churn,usage_frequency;

SELECT gender,customer_age,COUNT(*) AS customer_age_distribution
FROM churn_data
WHERE customer_age = (SELECT MIN(customer_age) FROM churn_data)
OR customer_age = (SELECT MAX(customer_age) FROM churn_data)
GROUP BY gender,customer_age
ORDER BY customer_age DESC;

SELECT churn,gender,ROUND(AVG(total_spend)) AS average_total_spend,
ROUND(MIN(total_spend)) AS minimum_total_spend,
ROUND(MAX(total_spend)) AS maximum_total_spend
FROM churn_data
GROUP BY churn,gender;

SELECT churn,gender,total_spend,COUNT(*) AS total_spend_distribution
FROM churn_data
WHERE churn = 1
AND total_spend >= (SELECT AVG(total_spend) FROM churn_data)
AND gender = 'Female'
GROUP BY churn,gender,total_spend;

SELECT churn,gender,ROUND(AVG(last_intraction)) AS average_last_intraction,
ROUND(MIN(last_intraction)) AS minimum_last_intraction,
ROUND(MAX(last_intraction)) AS maximum_last_intraction
FROM churn_data
GROUP BY churn,gender;

SELECT churn,gender,last_intraction,COUNT(*) AS total_last_intraction
FROM churn_data
WHERE last_intraction >= (SELECT AVG(last_intraction) FROM churn_data)
AND churn = 1 AND gender = 'Female'
GROUP BY churn,gender,last_intraction
ORDER BY last_intraction DESC;

SELECT gender,churn,subscription_type,COUNT(*) AS total_subscription_type_count
FROM churn_data
WHERE churn = 1
GROUP BY gender,churn,subscription_type
ORDER BY total_subscription_type_count DESC;

SELECT gender,churn,contract_length,COUNT(*) AS contract_length_count
FROM churn_data
WHERE churn = 1
GROUP BY gender,churn,contract_length
ORDER BY contract_length_count DESC;

SELECT * FROM churn_data;