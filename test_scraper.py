from google_play_scraper import app, search
import pandas as pd
from sqlalchemy import create_engine

print("1. Searching the Play Store for Arcade & Puzzle games...")

search_queries = ["arcade games", "puzzle games"]
all_game_ids = []

for query in search_queries:
    print(f"Searching: {query}...")
    search_results = search(query, n_hits=100)
    for result in search_results:
        all_game_ids.append(result['appId'])

all_game_ids = list(set(all_game_ids))
print(f"Found {len(all_game_ids)} unique game IDs.")
print("2. Starting Star Schema ETL Pipeline...")

# Three separate lists for our 3 Star Schema tables
app_details_list = []
tech_specs_list = []
fact_metrics_list = []

for game_id in all_game_ids:
    try:
        details = app(game_id)

        raw_installs = details['installs']
        cleaned_installs = int(raw_installs.replace('+', '').replace(',', ''))

        # 1. Dimension: App Details (Static text info)
        app_details_list.append({
            'app_id': game_id,
            'title': details['title'],
            'developer': details['developer'],
            'genre': details['genre'],
            'content_rating': details['contentRating'],
            'ad_supported': details['adSupported']
        })

        # 2. Dimension: Technical Specs
        tech_specs_list.append({
            'app_id': game_id,
            'iap_price_range': details.get('inAppProductPrice', 'None')
        })

        # 3. Fact: Daily App Metrics (Changing numbers/reviews)
        fact_metrics_list.append({
            'app_id': game_id,
            'installs': cleaned_installs,
            'rating_score': details.get('score', 0.0),
            'ratings_count': details.get('ratings', 0),
            'reviews_count': details.get('reviews', 0),
            'last_updated': str(details.get('updated', 'Unknown'))
        })

        print(f"Extracted & Formatted: {details['title']}")

    except Exception as e:
        print(f"Skipped {game_id} due to error: {e}")

print("\n==========================================")
print("3. Converting to DataFrames & Loading into PostgreSQL...")

# Convert lists into Pandas DataFrames
df_app_details = pd.DataFrame(app_details_list).drop_duplicates(subset=['app_id'])
df_tech_specs = pd.DataFrame(tech_specs_list).drop_duplicates(subset=['app_id'])
df_fact_metrics = pd.DataFrame(fact_metrics_list)

# Save local CSV backups
df_app_details.to_csv('dim_app_details.csv', index=False)
df_tech_specs.to_csv('dim_technical_specs.csv', index=False)
df_fact_metrics.to_csv('fact_daily_app_metrics.csv', index=False)


DB_PASSWORD = "root123" 

engine = create_engine(f'postgresql://postgres:{DB_PASSWORD}@localhost:5432/playstore_db')

# Insert into Dimensions FIRST, then Fact table
df_app_details.to_sql('dim_app_details', engine, if_exists='append', index=False)
df_tech_specs.to_sql('dim_technical_specs', engine, if_exists='append', index=False)
df_fact_metrics.to_sql('fact_daily_app_metrics', engine, if_exists='append', index=False)

print("SUCCESS! Data distributed across Star Schema tables.")