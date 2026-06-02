import sqlite3
import pandas as pd

conn = sqlite3.connect("ecommerce.db")

# ─────────────────────────────────────────────────────────────
# QUERY 1: Monthly Revenue Trends + MoM Growth
# ─────────────────────────────────────────────────────────────
# What is this? 
# We're calculating total revenue (GMV) per month.
# Then using a "window function" LAG() to compare each month 
# to the previous month and calculate % growth.
#
# CTE = Common Table Expression — just a temporary named result
# you can reference later in the same query. Like a sub-query
# but much cleaner to read.

q1 = """
WITH monthly AS (
    SELECT
        strftime('%Y-%m', o.order_purchase_timestamp) AS month,
        ROUND(SUM(oi.price + oi.freight_value), 2)    AS gmv,
        COUNT(DISTINCT o.order_id)                     AS total_orders,
        ROUND(SUM(oi.price + oi.freight_value) * 1.0 /
              COUNT(DISTINCT o.order_id), 2)           AS aov
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY month
)
SELECT *,
    ROUND(
        (gmv - LAG(gmv) OVER (ORDER BY month)) * 100.0
        / NULLIF(LAG(gmv) OVER (ORDER BY month), 0),
    2) AS mom_growth_pct
FROM monthly
ORDER BY month;
"""

df_monthly = pd.read_sql(q1, conn)
df_monthly.to_csv("outputs/monthly_revenue.csv", index=False)
print("✅ Query 1 done — Monthly Revenue")
print(df_monthly.tail())

# ─────────────────────────────────────────────────────────────
# QUERY 2: Customer Segmentation using RFM
# ─────────────────────────────────────────────────────────────
# RFM = Recency, Frequency, Monetary
# Recency   — how recently did they buy?
# Frequency — how many times did they buy?
# Monetary  — how much did they spend?
#
# NTILE(4) splits customers into 4 equal buckets (quartiles)
# Score 4 = best customers, Score 1 = worst

q2 = """
WITH rfm_base AS (
    SELECT
        o.customer_id,
        MAX(o.order_purchase_timestamp)    AS last_purchase,
        COUNT(DISTINCT o.order_id)         AS frequency,
        ROUND(SUM(op.payment_value), 2)    AS monetary
    FROM orders o
    JOIN order_payments op ON o.order_id = op.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY o.customer_id
),
rfm_scored AS (
    SELECT *,
        NTILE(4) OVER (ORDER BY last_purchase DESC) AS r_score,
        NTILE(4) OVER (ORDER BY frequency DESC)     AS f_score,
        NTILE(4) OVER (ORDER BY monetary DESC)      AS m_score
    FROM rfm_base
)
SELECT *,
    (r_score + f_score + m_score) AS rfm_total,
    CASE
        WHEN (r_score + f_score + m_score) >= 10 THEN 'Champions'
        WHEN (r_score + f_score + m_score) >= 7  THEN 'Loyal'
        WHEN (r_score + f_score + m_score) >= 5  THEN 'At Risk'
        ELSE 'Lost'
    END AS segment
FROM rfm_scored
ORDER BY rfm_total DESC;
"""

df_rfm = pd.read_sql(q2, conn)
df_rfm.to_csv("outputs/rfm_segments.csv", index=False)
print("\n✅ Query 2 done — RFM Segmentation")
print(df_rfm["segment"].value_counts())

# ─────────────────────────────────────────────────────────────
# QUERY 3: Return Rate by Category
# ─────────────────────────────────────────────────────────────
# We're joining products → category translation
# Then counting canceled/unavailable orders as "returns"
# and calculating what % of ALL returns each category causes

q3 = """
WITH category_stats AS (
    SELECT
        ct.product_category_name_english            AS category,
        COUNT(o.order_id)                           AS total_orders,
        SUM(CASE WHEN o.order_status IN ('canceled','unavailable') 
                 THEN 1 ELSE 0 END)                 AS returns
    FROM orders o
    JOIN order_items oi   ON o.order_id  = oi.order_id
    JOIN products p       ON oi.product_id = p.product_id
    JOIN category_translation ct 
                          ON p.product_category_name = ct.product_category_name
    GROUP BY category
)
SELECT *,
    ROUND(returns * 100.0 / NULLIF(total_orders, 0), 2) AS return_rate_pct,
    ROUND(returns * 100.0 / NULLIF(SUM(returns) OVER(), 0), 2) AS pct_of_all_returns
FROM category_stats
WHERE total_orders > 100
ORDER BY return_rate_pct DESC;
"""

df_returns = pd.read_sql(q3, conn)
df_returns.to_csv("outputs/category_returns.csv", index=False)
print("\n✅ Query 3 done — Category Returns")
print(df_returns.head(5))

# ─────────────────────────────────────────────────────────────
# QUERY 4: Revenue by Region (State)
# ─────────────────────────────────────────────────────────────

q4 = """
SELECT
    c.customer_state                          AS state,
    COUNT(DISTINCT o.order_id)                AS orders,
    ROUND(SUM(op.payment_value), 2)           AS revenue,
    ROUND(AVG(op.payment_value), 2)           AS avg_order_value
FROM orders o
JOIN customers c    ON o.customer_id  = c.customer_id
JOIN order_payments op ON o.order_id = op.order_id
WHERE o.order_status = 'delivered'
GROUP BY state
ORDER BY revenue DESC;
"""

df_region = pd.read_sql(q4, conn)
df_region.to_csv("outputs/revenue_by_region.csv", index=False)
print("\n✅ Query 4 done — Revenue by Region")
print(df_region.head())

conn.close()
print("\n✅ All queries complete. Check your outputs/ folder.")