# in-project imports
from src.pipeline.extract import (
    extract_match_updates,
    extract_match_stats_updates,
    extract_player_season_stats_updates,
    extract_standing_updates
)
from src.pipeline.transform import (
    transform_matches,
    transform_all_match_stats,
    transform_all_player_season_stats,
    transform_standings
)
from src.pipeline.load import (
    load_matches,
    load_all_match_stats,
    load_players_season_stats,
    load_standings
)
from src.database.queries import (
    get_match_ids_to_update,
    get_match_ids_with_no_stats,
    get_current_season_ids
)
'''
    Need to update:
    - matches
    - match_stats
    - player_season_stats
    - standings
'''

'''
        UPDATE FUNCTIONS
'''

def update_matches(match_ids):
    print("Updating match data...")
    raw_updated_match_data = extract_match_updates(match_ids)
    transformed_updated_match_data = transform_matches(raw_updated_match_data)
    load_matches(transformed_updated_match_data)
    print("Succesfully updated match info.")
    
def update_match_stats(match_ids):
    print("Updating match stats data...")
    raw_updated_match_stats_data = extract_match_stats_updates(match_ids)
    transformed_updated_match_stats_data = transform_all_match_stats(raw_updated_match_stats_data)
    load_all_match_stats(transformed_updated_match_stats_data)
    print("Succesfully updated match stats info.")
    
def update_player_season_stats():
    print("Updating player season stats...")
    raw_updated_player_season_stats_data = extract_player_season_stats_updates()
    transformed_updated_player_season_stats_data = transform_all_player_season_stats(raw_updated_player_season_stats_data)
    load_players_season_stats(transformed_updated_player_season_stats_data)
    print("Succesfully updated player season stats info.")

def update_standings(season_id):
    print("Updating standings...")
    raw_updated_standing_data = extract_standing_updates(season_id)
    transformed_updated_standing_data = transform_standings(raw_updated_standing_data)
    load_standings(transformed_updated_standing_data)
    print("Succesfully standings.")    

def run_update():
    
    print("Updating database data...")
    
    # Updating matches
    match_ids = get_match_ids_to_update()
    update_matches(match_ids)
    
    # Updating match stats
    match_ids.extend(get_match_ids_with_no_stats())
    update_match_stats(match_ids)
    
    # Updating player season stats
    update_player_season_stats()
    
    # Updating standings
    current_season_ids = get_current_season_ids()
    for season_id in current_season_ids:
        update_standings(season_id)
    
    print("Update complete.")
    
    

if __name__ == "__main__":
    run_update()