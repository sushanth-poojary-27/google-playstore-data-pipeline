# Google Play Store ETL Pipeline 🚀

## Overview
This project is an automated Data Engineering pipeline (ETL) built in Python. It dynamically scrapes the Google Play Store for trending games, cleans and transforms the raw data, and loads it directly into a local PostgreSQL database for analysis.

## Architecture
* **Language:** Python
* **Extraction:** `google-play-scraper` (Dynamic web scraping)
* **Transformation:** `pandas` (Data cleaning, type conversion)
* **Loading:** `SQLAlchemy` & `psycopg2`
* **Database:** PostgreSQL (Viewed via DBeaver)

## How It Works
1. **Extract:** The script searches the Play Store for a specific keyword (e.g., "action games") and extracts the unique App IDs. It then scrapes detailed metadata for each app (Title, Developer, Content Rating, Installs, Genre, Ad Support).
2. **Transform:** The raw install data (e.g., `"100,000,000+"`) is cleaned by stripping special characters and converting the string into actionable integer types.
3. **Load:** The cleaned dataset is converted into a Pandas DataFrame and injected directly into a PostgreSQL relational database using a SQLAlchemy engine. A backup `.csv` is also generated.

## Future Upgrades
* Implement automated daily scheduling using Windows Task Scheduler / Cron.
* Build data visualizations using Matplotlib or Tableau.