from google_play_scraper import app, search
import pandas as pd
from sqlalchemy import create_engine # <--- Our new Database tool!

print("1. Searching the Play Store for top games...")

# 1. EXTRACT
search_results = search("action games", n_hits=10)
game_ids = []
for result in search_results:
    game_ids.append(result['appId'])

print(f"Success! Found {len(game_ids)} games.")
print("2. Starting Data Pipeline (ETL)...\n")

all_games_data = []

# 2. TRANSFORM
for game_id in game_ids:
    game_details = app(game_id)

    raw_installs = game_details['installs']
    cleaned_installs = int(raw_installs.replace('+', '').replace(',', ''))

    # CRITICAL: These keys must exactly match your PostgreSQL columns!
    extracted_data = {
        'title': game_details['title'], 
        'developer': game_details['developer'],
        'content_rating': game_details['contentRating'], 
        'installs': cleaned_installs, 
        'genre': game_details['genre'],
        'ad_supported': game_details['adSupported'] 
    }
    all_games_data.append(extracted_data)
    print(f"Scraped: {game_details['title']}") 

print("\n=========================")
print("3. Loading data into PostgreSQL Database...")

df = pd.DataFrame(all_games_data)
# Let's keep a CSV backup just in case
df.to_csv('my_dynamic_games.csv', index=False)

# 3. LOAD (To Database!)
# --> STOP! REPLACE 'your_password_here' WITH YOUR ACTUAL POSTGRES PASSWORD <--
DB_PASSWORD = "root123"  # <-- CHANGE THIS TO YOUR POSTGRES PASSWORD

# This line builds the bridge to your specific database
engine = create_engine(f'postgresql://postgres:{"root123"}@localhost:5432/playstore_db')

# This single line shoots your Pandas table directly into your SQL table!
df.to_sql('top_games', engine, if_exists='append', index=False)

print("SUCCESS! Your Python Data Pipeline is connected to your Database!")