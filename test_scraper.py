from google_play_scraper import app, search
import pandas as pd
from sqlalchemy import create_engine

print("1. Searching the Play Store for target niches...")

# We are now searching for multiple categories from your Master Plan!
search_queries = ["arcade games", "puzzle games"]
all_game_ids = []

for query in search_queries:
    print(f"Searching for top 100 {query}...")
    search_results = search(query, n_hits=100) # Upgraded to 100 hits per category
    for result in search_results:
        all_game_ids.append(result['appId'])

# Remove duplicates in case a game ranks in both Arcade and Puzzle
all_game_ids = list(set(all_game_ids))
print(f"Success! Found {len(all_game_ids)} unique games to scrape.")
print("2. Starting Heavy Data Pipeline (ETL)... This might take a minute or two!")

all_games_data = []

for game_id in all_game_ids:
    # A 'try/except' block is crucial for big data. If one game fails, the pipeline keeps going!
    try:
        game_details = app(game_id)

        raw_installs = game_details['installs']
        cleaned_installs = int(raw_installs.replace('+', '').replace(',', ''))

        extracted_data = {
            'title': game_details['title'], 
            'developer': game_details['developer'],
            'content_rating': game_details['contentRating'], 
            'installs': cleaned_installs, 
            'genre': game_details['genre'],
            'ad_supported': game_details['adSupported'],
            'rating_score': game_details.get('score', 0.0),
            'ratings_count': game_details.get('ratings', 0),
            'reviews_count': game_details.get('reviews', 0),
            'iap_price_range': game_details.get('inAppProductPrice', 'None'),
            'last_updated': str(game_details.get('updated', 'Unknown'))
        }
        all_games_data.append(extracted_data)
        print(f"Scraped: {game_details['title']}") 
        
    except Exception as e:
        print(f"Skipped {game_id} due to an error: {e}")

print("\n=========================")
print("3. Loading massive dataset into PostgreSQL Database...")

df = pd.DataFrame(all_games_data)
# Upgraded backup file 
df.to_csv('my_massive_games_dataset.csv', index=False)

DB_PASSWORD = "root123" 

engine = create_engine(f'postgresql://postgres:{'root123'}@localhost:5432/playstore_db')
df.to_sql('top_games', engine, if_exists='append', index=False)

print(f"SUCCESS! {len(df)} rows loaded into PostgreSQL.")