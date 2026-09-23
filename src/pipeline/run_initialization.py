
# in-project imports 
from src.pipeline.extract import (
    extract_competitions, 
    extract_seasons,
    extract_teams,
    extract_matches,
    extract_match_stats,
    extract_rosters_and_players,
    extract_player_season_stats,
    extract_standings
)
from src.pipeline.transform import (
    transform_competitions, 
    transform_seasons,
    transform_teams,
    transform_matches,
    transform_all_match_stats,
    transform_rosters,
    transform_players,
    transform_all_player_season_stats,
    transform_standings
)
from src.pipeline.load import (
    load_competitions, 
    load_seasons,
    load_teams,
    load_matches,
    load_all_match_stats,
    load_rosters,
    load_players,
    load_players_season_stats,
    load_standings
)

def run():
    print("Starting pipeline...")
    
    '''
            Extraction Transformation Load
    '''
    # Competitions
    raw_competition_data = extract_competitions()
    transformed_competition_data = transform_competitions(raw_competition_data)
    load_competitions(transformed_competition_data)
    
    # Seasons
    raw_season_data = extract_seasons()
    transformed_season_data = transform_seasons(raw_season_data)
    load_seasons(transformed_season_data)
    
    # Teams
    raw_team_data = extract_teams()
    transformed_team_data = transform_teams(raw_team_data)
    load_teams(transformed_team_data)
    
    # Matches
    raw_match_data = extract_matches()
    transformed_match_data = transform_matches(raw_match_data)
    load_matches(transformed_match_data)
    
    # Match stats
    raw_match_stats_data = extract_match_stats()
    transformed_match_stats_data = transform_all_match_stats(raw_match_stats_data)
    load_all_match_stats(transformed_match_stats_data)
    
    # Rosters + Players
    raw_roster_data, raw_player_data = extract_rosters_and_players()
    transformed_player_data = transform_players(raw_player_data)
    transformed_roster_data = transform_rosters(raw_roster_data)
    load_players(transformed_player_data)
    load_rosters(transformed_roster_data)
    
    # Player season stats
    raw_player_season_stats_data = extract_player_season_stats()
    transformed_player_season_stats_data = transform_all_player_season_stats(raw_player_season_stats_data)
    load_players_season_stats(transformed_player_season_stats_data)
    
    # Standings
    raw_standing_data = extract_standings()
    transformed_standing_data = transform_standings(raw_standing_data)    
    load_standings(transformed_standing_data)

    print("Pipeline finished successfully.")

if __name__ == "__main__":
    run()