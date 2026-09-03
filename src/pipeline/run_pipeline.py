
# in-project imports 
from src.pipeline.extract import extract_competitions
from src.pipeline.transform import transform_competitions
from src.pipeline.load import load_competitions

'''
I’d do them in this order because of the foreign-key dependencies:

✅ competitions
seasons
teams
matches
match_stats
players
rosters
player_season_stats
standings
'''

def run():
    print("Starting pipeline...")

    raw_competition_data = extract_competitions()
    print("Extraction complete.\n")
    
    transformed_competition_data = transform_competitions(raw_competition_data)
    print("Transformation complete.\n")


    load_competitions(transformed_competition_data)
    print("Loading complete.\n")
    
    print("Pipeline finished successfully.")

if __name__ == "__main__":
    run()