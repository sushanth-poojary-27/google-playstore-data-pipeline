from google_play_scraper import app
import pandas as pd

game_ids = ["com.supercell.clashofclans" , "com.pubg.imobile" , "com.supercell.clashroyale" , "com.nekki.shadowfight"]
all_games_data = []
print("====Multi Game Details====")
for game_id in game_ids:
    game_details = app(game_id)
    extracted_data = {
        'title': game_details['title'], 
        'developer': game_details['developer'],
        'contentRating': game_details['contentRating'],
        'installs': game_details['installs'],
        'genre': game_details['genre'],
        'ad supported': game_details['adSupported']
    }
    all_games_data.append(extracted_data)   
    print("\n=========================")
    print("Scraping Completed saving to CSV file")

df = pd.DataFrame(all_games_data)
df.to_csv('my_game_details.csv', index=False)

print("Data saved to my_game_details.csv")