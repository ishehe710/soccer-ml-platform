
# in-project imports 
from src.pipeline.extract import (
    extract_competitions, 
    extract_seasons,
    extract_teams
)
from src.pipeline.transform import (
    transform_competitions, 
    transform_seasons,
    transform_teams
)
from src.pipeline.load import (
    load_competitions, 
    load_seasons,
    load_teams
)

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
    raw_team_data = extract_teams()
    print("Extraction complete.\n")
    
    # Transformation
    transformed_competition_data = transform_competitions(raw_competition_data)
    transformed_season_data = transform_seasons(raw_season_data)
    transformed_team_data = transform_teams(raw_team_data)
    print("Transformation complete.\n")

    # Loading
    load_competitions(transformed_competition_data)
    load_seasons(transformed_season_data)
    load_teams(transformed_team_data)
    print("Loading complete.\n")
    print("Pipeline finished successfully.")

if __name__ == "__main__":
    run()