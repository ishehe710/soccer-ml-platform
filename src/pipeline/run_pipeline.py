"""
Incremental ETL pipeline for the Soccer ML Platform.

Updates mutable match, match statistics, player season statistics,
and standings data in PostgreSQL.
"""

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
from src.config.logger import create_logger

# Update pipeline logger
logger = create_logger(__name__)

'''
        UPDATE FUNCTIONS
'''
def update_matches(match_ids):
    """Updates match info for games that have come to pass in the database.

    Args:
        match_ids (list[match_ids]): List of official api ids for matches that are set for update.
    """
    logger.info("Updating match data...")
    
    raw_updated_match_data = extract_match_updates(match_ids)
    transformed_updated_match_data = transform_matches(raw_updated_match_data)
    load_matches(transformed_updated_match_data)
    
    logger.info("Succesfully updated match info.")
    
def update_match_stats(match_ids):
    """Update match stats in the databse for matches that have beeen concluded and not yet been updated.

    Args:
        match_ids (list[match_ids]): List of official api ids for match stats for matches that are set for update.
    """
    
    logger.info("Updating match stats data...")
    
    raw_updated_match_stats_data = extract_match_stats_updates(match_ids)
    transformed_updated_match_stats_data = transform_all_match_stats(raw_updated_match_stats_data)
    load_all_match_stats(transformed_updated_match_stats_data)
    
    logger.info("Succesfully updated match stats info.")
    
def update_player_season_stats():
    """Update active players current season stats.
    """
    logger.info("Updating player season stats...")
    
    raw_updated_player_season_stats_data = extract_player_season_stats_updates()
    transformed_updated_player_season_stats_data = transform_all_player_season_stats(raw_updated_player_season_stats_data)
    load_players_season_stats(transformed_updated_player_season_stats_data)
    
    logger.info("Succesfully updated player season stats info.")

def update_standings(season_id):
    """Update current competition standings.

    Args:
        season_id (int): Official api id of the season's standings to update.
    """
    logger.info("Updating standings...")
    raw_updated_standing_data = extract_standing_updates(season_id)
    transformed_updated_standing_data = transform_standings(raw_updated_standing_data)
    load_standings(transformed_updated_standing_data)
    logger.info("Succesfully standings.")    

def run_update():
    
    try:
        logger.info("Updating database data...")
            
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
        logger.info("Updating %d standings for the database.", len(current_season_ids))
        for season_id in current_season_ids:
            update_standings(season_id)
        
        logger.info("Update completed successfully.")
    except Exception: 
        logger.exception("Update failed.")
        raise 
        
if __name__ == "__main__":
    run_update()