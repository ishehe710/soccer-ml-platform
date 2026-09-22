# in-project imports
from tests.pipeline_testing.test_extract import data
from src.pipeline.transform import (
    transform_competitions, 
    transform_seasons,
    transform_teams,
    transform_matches,
    transform_standings
    )

transformed_data = transform_standings(data)

print("Transformed data:")
print(transformed_data)