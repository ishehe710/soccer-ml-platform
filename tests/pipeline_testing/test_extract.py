# in-projects imports
from src.pipeline.extract import (
    extract_competitions, 
    extract_seasons,
    extract_teams,
    extract_matches,
    extract_a_team,
    extract_match_stats,
    extract_standings
    )


data = extract_standings()

print("Extracting data")
print("data", data)
