# in-projects imports
from src.pipeline.extract import (
    extract_competitions, 
    extract_seasons,
    extract_teams,
    extract_matches,
    extract_a_team,
    extract_match_stats,
    extract_standings,
    extract_match_updates,
    extract_match_stats_updates
    )


data = extract_match_stats_updates()

print("Extracting data")
print("data", data)
