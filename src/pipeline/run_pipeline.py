
# in-project imports 
from src.pipeline.extract import (
    extract_competitions, 
    extract_seasons,
    extract_teams,
    extract_matches,
    extract_match_stats,
    extract_rosters_and_players
)
from src.pipeline.transform import (
    transform_competitions, 
    transform_seasons,
    transform_teams,
    transform_matches,
    transform_all_match_stats,
    transform_rosters,
    transform_players
)
from src.pipeline.load import (
    load_competitions, 
    load_seasons,
    load_teams,
    load_matches,
    load_all_match_stats,
    load_rosters,
    load_players
)

'''
I’d do them in this order because of the foreign-key dependencies:

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
    raw_roster_data, raw_player_data = extract_rosters_and_players()
    print("Extraction complete.\n")
    
    # Transformation
    '''
    transformed_competition_data = transform_competitions(raw_competition_data)
    transformed_season_data = transform_seasons(raw_season_data)
    transformed_team_data = transform_teams(raw_team_data)
    transformed_match_data = transform_matches(raw_match_data)

    transformed_match_stats_data = transform_all_match_stats(raw_match_stats_data)
    
    transformed_player_data = transform_players(raw_player_data)
    '''
    transformed_roster_data = transform_rosters(raw_roster_data)
    print("Transformation complete.\n")

    # Loading
    '''
    load_competitions(transformed_competition_data)
    load_seasons(transformed_season_data)
    load_teams(transformed_team_data)
    load_matches(transformed_match_data)
    
    load_all_match_stats(transformed_match_stats_data)
    
    load_players(transformed_player_data)
    '''
    load_rosters(transformed_roster_data)
    print("Loading complete.\n")
    print("Pipeline finished successfully.")

if __name__ == "__main__":
    run()