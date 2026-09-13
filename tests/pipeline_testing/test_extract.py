# in-projects imports
from src.pipeline.extract import (
    extract_competitions, 
    extract_seasons,
    extract_teams,
    extract_matches,
    extract_a_team,
    extract_match_stats
    )

data = extract_match_stats()

print("Extracting data")
print("data", data)