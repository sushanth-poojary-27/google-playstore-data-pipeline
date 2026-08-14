-- Google Play Store ETL - Star Schema DDL

-- 1. Dimension: App Details
CREATE TABLE IF NOT EXISTS dim_app_details (
    app_id VARCHAR(255) PRIMARY KEY,
    title VARCHAR(255),
    developer VARCHAR(255),
    genre VARCHAR(100),
    content_rating VARCHAR(50),
    ad_supported BOOLEAN
);

-- 2. Dimension: Technical Specs
CREATE TABLE IF NOT EXISTS dim_technical_specs (
    app_id VARCHAR(255) PRIMARY KEY,
    iap_price_range VARCHAR(100)
);

-- 3. Fact: Daily App Metrics
CREATE TABLE IF NOT EXISTS fact_daily_app_metrics (
    metric_id SERIAL PRIMARY KEY,
    app_id VARCHAR(255),
    scrape_date DATE DEFAULT CURRENT_DATE,
    installs INTEGER,
    rating_score FLOAT,
    ratings_count BIGINT,
    reviews_count BIGINT,
    last_updated VARCHAR(100),
    FOREIGN KEY (app_id) REFERENCES dim_app_details(app_id)
);