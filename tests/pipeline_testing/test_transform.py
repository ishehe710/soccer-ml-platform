# in-project imports
from tests.pipeline_testing.test_extract import data
from src.pipeline.transform import transform_competitions, transform_seasons

transformed_data = transform_seasons(data)

print("Transformed data:")
print(transformed_data)