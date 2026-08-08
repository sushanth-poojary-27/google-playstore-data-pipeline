from google_play_scraper import app, search
import pandas as pd
print("Searching the Playstore for top arcade games...")
search_results = search("puzzle games", n_hits=10)
game_ids = []
for results in search_results:
    game_ids.append(results['appId'])

all_games_data = []
for game_id in game_ids:
    game_details = app(game_id)

    raw_installs_data = game_details['installs']
    cleaned_installs_data = raw_installs_data.replace('+', '').replace(',', '')

    extracted_data = {
        'title': game_details['title'], 
        'developer': game_details['developer'],
        'contentRating': game_details['contentRating'],
        'installs': cleaned_installs_data,
        'genre': game_details['genre'],
        'ad supported': game_details['adSupported']
    }
    all_games_data.append(extracted_data)   
    print("\n=========================")
    print("Scraping Completed saving to CSV file")

df = pd.DataFrame(all_games_data)
df.to_csv('my_game_details.csv', index=False)

print("Data saved to my_game_details.csv")