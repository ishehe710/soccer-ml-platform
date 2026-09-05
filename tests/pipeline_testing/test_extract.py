# in-projects imports
from src.pipeline.extract import (
    extract_competitions, 
    extract_seasons,
    extract_teams
    )

data = extract_teams()

print("Extracting teams data")
print(data)