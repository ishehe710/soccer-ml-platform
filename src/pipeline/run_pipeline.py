
# in-project imports 
from src.pipeline.extract import extract_competitions, extract_seasons
from src.pipeline.transform import transform_competitions, transform_seasons
from src.pipeline.load import load_competitions, load_seasons

'''
I’d do them in this order because of the foreign-key dependencies:

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

    # Extraction
    raw_competition_data = extract_competitions()
    raw_season_data = extract_seasons()
    print("Extraction complete.\n")
    
    # Transformation
    transformed_competition_data = transform_competitions(raw_competition_data)
    transformed_season_data = transform_seasons(raw_season_data)
    print("Transformation complete.\n")

    # Loading
    load_competitions(transformed_competition_data)
    load_seasons(transformed_season_data)
    print("Loading complete.\n")
    print("Pipeline finished successfully.")

if __name__ == "__main__":
    run()