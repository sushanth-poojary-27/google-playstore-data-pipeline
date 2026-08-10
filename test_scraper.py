from google_play_scraper import app, search
import pandas as pd
from sqlalchemy import create_engine

# Helper function to convert all sizes into Megabytes (MB)
def parse_size_to_mb(size_str):
    if not size_str or size_str in ['Varies with device', 'Unknown', 'None']:
        return None
    
    size_str = str(size_str).strip().upper()
    
    try:
        if size_str.endswith('M'):
            return float(size_str.replace('M', '').replace(',', ''))
        elif size_str.endswith('K'):
            return round(float(size_str.replace('K', '').replace(',', '')) / 1024, 2)
        elif size_str.endswith('G'):
            return round(float(size_str.replace('G', '').replace(',', '')) * 1024, 2)
    except ValueError:
        return None
        
    return None

print("1. Searching the Play Store for Arcade games...")

search_results = search("arcade games", n_hits=10)
game_ids = [result['appId'] for result in search_results]

print(f"Success! Found {len(game_ids)} Arcade games.")
print("2. Starting Data Pipeline (ETL)...")

all_games_data = []

for game_id in game_ids:
    game_details = app(game_id)

    raw_installs = game_details['installs']
    cleaned_installs = int(raw_installs.replace('+', '').replace(',', ''))
    
    # Standardize size to Megabytes
    raw_size = game_details.get('size', 'Unknown')
    cleaned_size_mb = parse_size_to_mb(raw_size)

    extracted_data = {
        'title': game_details['title'], 
        'developer': game_details['developer'],
        'content_rating': game_details['contentRating'], 
        'installs': cleaned_installs, 
        'genre': game_details['genre'],
        'ad_supported': game_details['adSupported'],
        'app_size_mb': cleaned_size_mb,
        'min_android': game_details.get('androidVersionText', 'Unknown'),
        'iap_price_range': game_details.get('inAppProductPrice', 'None'),
        'rating_score': game_details.get('score', 0.0)
    }
    all_games_data.append(extracted_data)
    print(f"Scraped: {game_details['title']} | Clean Size: {cleaned_size_mb} MB") 

print("\n=========================")
print("3. Loading clean data into PostgreSQL Database...")

df = pd.DataFrame(all_games_data)
df.to_csv('my_dynamic_games.csv', index=False)

DB_PASSWORD = "root123" 

engine = create_engine(f'postgresql://postgres:{"root123"}@localhost:5432/playstore_db')
df.to_sql('top_games', engine, if_exists='append', index=False)

print("SUCCESS! Standardized dataset loaded into PostgreSQL.")