USE olist_kpi_engine;

-- 1. Duplicate order IDs
SELECT 
    'Duplicate order_id in orders' AS check_name,
    COUNT(*) AS issue_count
FROM (
    SELECT order_id
    FROM orders
    GROUP BY order_id
    HAVING COUNT(*) > 1
) t;

-- 2. Missing customer_id in orders
SELECT
    'Missing customer_id in orders' AS check_name,
    COUNT(*) AS issue_count
FROM orders
WHERE customer_id IS NULL;

-- 3. Orders without payment record
SELECT
    'Orders without payment record' AS check_name,
    COUNT(*) AS issue_count
FROM orders o
LEFT JOIN payments p
    ON o.order_id = p.order_id
WHERE p.order_id IS NULL;

-- 4. Orders without customer record
SELECT
    'Orders without customer record' AS check_name,
    COUNT(*) AS issue_count
FROM orders o
LEFT JOIN customers c
    ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

-- 5. Negative payment values
SELECT
    'Negative payment values' AS check_name,
    COUNT(*) AS issue_count
FROM payments
WHERE payment_value < 0;

-- 6. Order items without product_id
SELECT
    'Order items without product_id' AS check_name,
    COUNT(*) AS issue_count
FROM order_items
WHERE product_id IS NULL;

-- 7. Delivered date before purchase date
SELECT
    'Delivered date before purchase date' AS check_name,
    COUNT(*) AS issue_count
FROM orders
WHERE order_delivered_customer_date < order_purchase_timestamp;

-- 8. Missing review scores
SELECT
    'Missing review scores' AS check_name,
    COUNT(*) AS issue_count
FROM reviews
WHERE review_score IS NULL;