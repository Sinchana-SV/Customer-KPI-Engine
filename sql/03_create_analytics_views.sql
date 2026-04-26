USE olist_kpi_engine;

-- =====================================================
-- 1. Clean orders view
-- =====================================================

CREATE OR REPLACE VIEW analytics_orders AS
SELECT
    order_id,
    customer_id,
    order_status,

    STR_TO_DATE(order_purchase_timestamp, '%Y-%m-%d %H:%i:%s') AS order_purchase_timestamp,
    STR_TO_DATE(order_approved_at, '%Y-%m-%d %H:%i:%s') AS order_approved_at,
    STR_TO_DATE(order_delivered_carrier_date, '%Y-%m-%d %H:%i:%s') AS order_delivered_carrier_date,
    STR_TO_DATE(order_delivered_customer_date, '%Y-%m-%d %H:%i:%s') AS order_delivered_customer_date,
    STR_TO_DATE(order_estimated_delivery_date, '%Y-%m-%d %H:%i:%s') AS order_estimated_delivery_date,

    DATE_FORMAT(STR_TO_DATE(order_purchase_timestamp, '%Y-%m-%d %H:%i:%s'), '%Y-%m-01') AS order_month,

    CASE
        WHEN order_delivered_customer_date IS NOT NULL
        THEN DATEDIFF(
            STR_TO_DATE(order_delivered_customer_date, '%Y-%m-%d %H:%i:%s'),
            STR_TO_DATE(order_purchase_timestamp, '%Y-%m-%d %H:%i:%s')
        )
        ELSE NULL
    END AS delivery_days,

    CASE
        WHEN order_delivered_customer_date > order_estimated_delivery_date THEN 1
        ELSE 0
    END AS is_late_delivery

FROM orders;


-- =====================================================
-- 2. Clean customers view
-- =====================================================

CREATE OR REPLACE VIEW analytics_customers AS
SELECT
    customer_id,
    customer_unique_id,
    customer_zip_code_prefix,
    customer_city,
    customer_state
FROM customers;


-- =====================================================
-- 3. Clean order items view
-- =====================================================

CREATE OR REPLACE VIEW analytics_order_items AS
SELECT
    order_id,
    order_item_id,
    product_id,
    seller_id,
    STR_TO_DATE(shipping_limit_date, '%Y-%m-%d %H:%i:%s') AS shipping_limit_date,
    price,
    freight_value,
    price + freight_value AS item_total_value
FROM order_items
WHERE price >= 0
  AND freight_value >= 0;


-- =====================================================
-- 4. Clean payments view
-- =====================================================

CREATE OR REPLACE VIEW analytics_payments AS
SELECT
    order_id,
    payment_sequential,
    payment_type,
    payment_installments,
    payment_value
FROM payments
WHERE payment_value >= 0;


-- =====================================================
-- 5. Clean reviews view
-- =====================================================

CREATE OR REPLACE VIEW analytics_reviews AS
SELECT
    review_id,
    order_id,
    review_score,
    STR_TO_DATE(review_creation_date, '%Y-%m-%d %H:%i:%s') AS review_creation_date,
    STR_TO_DATE(review_answer_timestamp, '%Y-%m-%d %H:%i:%s') AS review_answer_timestamp,

    CASE
        WHEN review_score >= 4 THEN 'positive'
        WHEN review_score = 3 THEN 'neutral'
        WHEN review_score <= 2 THEN 'negative'
        ELSE 'unknown'
    END AS review_sentiment
FROM reviews
WHERE review_score IS NOT NULL;


-- =====================================================
-- 6. Seller revenue base view
-- This will be used for seller revenue and concentration KPIs
-- =====================================================

CREATE OR REPLACE VIEW analytics_seller_revenue_base AS
SELECT
    oi.order_id,
    oi.seller_id,
    o.order_purchase_timestamp,
    o.order_month,
    o.order_status,
    oi.price,
    oi.freight_value,
    oi.item_total_value
FROM analytics_order_items oi
JOIN analytics_orders o
    ON oi.order_id = o.order_id
WHERE o.order_status = 'delivered';