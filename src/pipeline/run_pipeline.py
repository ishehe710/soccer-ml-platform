
# in-project imports 
from src.pipeline.extract import (
    extract_competitions, 
    extract_seasons,
    extract_teams,
    extract_matches,
    extract_match_stats
)
from src.pipeline.transform import (
    transform_competitions, 
    transform_seasons,
    transform_teams,
    transform_matches,
    transform_all_match_stats
)
from src.pipeline.load import (
    load_competitions, 
    load_seasons,
    load_teams,
    load_matches,
    load_all_match_stats 
)

'''
I’d do them in this order because of the foreign-key dependencies:

match_stats
players
rosters
player_season_stats
standings
'''

def run():
    print("Starting pipeline...")

    # Extraction
    
    '''
    raw_competition_data = extract_competitions()
    raw_season_data = extract_seasons()
    raw_team_data = extract_teams()
    raw_match_data = extract_matches()
    
    raw_match_stats_data = extract_match_stats()
    '''
    print("Extraction complete.\n")
    
    # Transformation
    '''
    transformed_competition_data = transform_competitions(raw_competition_data)
    transformed_season_data = transform_seasons(raw_season_data)
    transformed_team_data = transform_teams(raw_team_data)
    transformed_match_data = transform_matches(raw_match_data)

    transformed_match_stats_data = transform_all_match_stats(raw_match_stats_data)
    '''
    print("Transformation complete.\n")

    # Loading
    '''
    load_competitions(transformed_competition_data)
    load_seasons(transformed_season_data)
    load_teams(transformed_team_data)
    load_matches(transformed_match_data)
    
    load_all_match_stats(transformed_match_stats_data)
    '''
    print("Loading complete.\n")
    print("Pipeline finished successfully.")

if __name__ == "__main__":
    run()