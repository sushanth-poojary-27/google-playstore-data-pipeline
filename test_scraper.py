from google_play_scraper import app

game_ids = ["com.supercell.clashofclans" , "com.pubg.imobile" , "com.supercell.clashroyale" , "com.nekki.shadowfight"]

print("====Multi Game Details====")
for game_id in game_ids:
    game_details = app(game_id)
    print("Game Name", game_details['title'])
    print("Game Developer" ,game_details['developer'])
    print("Game Rating", game_details['contentRating'])
    print("Total Installs:", game_details['installs'])
    print("Genre:", game_details['genre'])
    print("Ad Supported:", game_details['adSupported'])
    print("\n=========================")