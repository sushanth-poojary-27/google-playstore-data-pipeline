# Google Play Store ETL Pipeline 🚀

## Overview
This project is an automated Data Engineering pipeline (ETL) built in Python. It dynamically scrapes the Google Play Store for trending games, cleans and transforms the raw data, and loads it into a normalized **Star Schema** within a local PostgreSQL database for advanced time-series analysis.

## Architecture

* **Language:** Python
* **Extraction:** `google-play-scraper` (Dynamic web scraping)
* **Transformation:** `pandas` (Data cleaning, deduplication, type conversion)
* **Loading:** `SQLAlchemy` & `psycopg2`
* **Security:** `python-dotenv` (Environment variable management)
* **Database:** PostgreSQL (Star Schema Architecture)

## 📂 Project Structure

```text
├── data/                  # Local CSV backups (Ignored in Git for storage optimization)
├── sql/                   # DDL scripts (init_schema.sql)
├── src/                   # Python ETL scripts (test_scraper.py)
├── .env.example           # Safe template for local credentials
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation ```

How It Works
Extract: The script searches the Play Store for specific niches (e.g., "action games" or "puzzle games") and extracts unique App IDs. It then scrapes detailed metadata for each app.

Transform: Raw text data (e.g., installs like "100,000,000+") is cleaned by stripping special characters and converting to optimized integer/float types. The flat data is then split into separate Fact and Dimension DataFrames.

Load (Star Schema): The cleaned DataFrames are injected into PostgreSQL using relational integrity:

dim_app_details (Dimension): Static game profile data (Title, Developer, Genre).

dim_technical_specs (Dimension): Configuration data (IAP Pricing).

fact_daily_app_metrics (Fact): Daily numerical snapshots (Installs, Ratings, Reviews) linked via foreign keys.

Setup Instructions
Clone the repository and install dependencies: pip install -r requirements.txt

Create a playstore_db database in PostgreSQL and run sql/init_schema.sql to build the tables.

Copy .env.example to .env and add your local PostgreSQL credentials.

Run the pipeline: python src/test_scraper.py

Future Upgrades
Migrate storage to a Cloud Data Lake using AWS S3 (Bronze Layer).

Host the PostgreSQL database on the cloud using Amazon RDS.

Orchestrate daily pipeline runs using Apache Airflow or Docker.