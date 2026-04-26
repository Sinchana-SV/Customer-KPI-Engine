USE olist_kpi_engine;

-- =====================================================
-- View 1: Monthly GMV
-- =====================================================

CREATE OR REPLACE VIEW kpi_monthly_gmv AS
SELECT
    DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m-01') AS order_month,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(p.payment_value), 2) AS monthly_gmv,
    ROUND(SUM(p.payment_value) / COUNT(DISTINCT o.order_id), 2) AS average_order_value
FROM analytics_orders o
JOIN analytics_payments p
    ON o.order_id = p.order_id
WHERE o.order_status = 'delivered'
GROUP BY DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m-01');


-- =====================================================
-- View 2: Repeat Customer Rate
-- =====================================================

CREATE OR REPLACE VIEW kpi_repeat_customer_rate AS
WITH customer_order_counts AS (
    SELECT
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) AS order_count
    FROM analytics_orders o
    JOIN analytics_customers c
        ON o.customer_id = c.customer_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
)

SELECT
    COUNT(*) AS total_customers,
    SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) AS repeat_customers,
    ROUND(
        SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS repeat_customer_rate_pct
FROM customer_order_counts;


-- =====================================================
-- View 3: Delivery Performance by State
-- =====================================================

CREATE OR REPLACE VIEW kpi_delivery_by_state AS
SELECT
    c.customer_state,
    COUNT(DISTINCT o.order_id) AS delivered_orders,
    ROUND(AVG(o.delivery_days), 2) AS avg_delivery_days,
    ROUND(SUM(o.is_late_delivery) * 100.0 / COUNT(DISTINCT o.order_id), 2) AS late_delivery_rate_pct
FROM analytics_orders o
JOIN analytics_customers c
    ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
  AND o.delivery_days IS NOT NULL
GROUP BY c.customer_state;


-- =====================================================
-- View 4: Review Score Trend
-- =====================================================

CREATE OR REPLACE VIEW kpi_review_trend AS
SELECT
    DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m-01') AS order_month,
    COUNT(DISTINCT r.review_id) AS total_reviews,
    ROUND(AVG(r.review_score), 2) AS avg_review_score,
    ROUND(SUM(CASE WHEN r.review_sentiment = 'positive' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS positive_review_pct,
    ROUND(SUM(CASE WHEN r.review_sentiment = 'negative' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS negative_review_pct
FROM analytics_orders o
JOIN analytics_reviews r
    ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
GROUP BY DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m-01');


-- =====================================================
-- View 5: Revenue Concentration
-- =====================================================

CREATE OR REPLACE VIEW kpi_revenue_concentration AS
WITH seller_revenue AS (
    SELECT
        seller_id,
        ROUND(SUM(item_total_value), 2) AS seller_gmv
    FROM analytics_seller_revenue_base
    GROUP BY seller_id
),

ranked_sellers AS (
    SELECT
        seller_id,
        seller_gmv,
        CUME_DIST() OVER (ORDER BY seller_gmv DESC) AS seller_percentile
    FROM seller_revenue
)

SELECT
    ROUND(SUM(CASE WHEN seller_percentile <= 0.10 THEN seller_gmv ELSE 0 END), 2) AS top_10pct_seller_gmv,
    ROUND(SUM(seller_gmv), 2) AS total_seller_gmv,
    ROUND(
        SUM(CASE WHEN seller_percentile <= 0.10 THEN seller_gmv ELSE 0 END) * 100.0 / SUM(seller_gmv),
        2
    ) AS top_10pct_revenue_share_pct
FROM ranked_sellers;


-- =====================================================
-- View 6: Top 10 Sellers
-- =====================================================

CREATE OR REPLACE VIEW kpi_top_10_sellers AS
SELECT
    seller_id,
    ROUND(SUM(item_total_value), 2) AS seller_gmv,
    COUNT(DISTINCT order_id) AS total_orders
FROM analytics_seller_revenue_base
GROUP BY seller_id
ORDER BY seller_gmv DESC
LIMIT 10;