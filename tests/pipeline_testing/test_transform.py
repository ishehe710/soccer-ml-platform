# in-project imports
from tests.pipeline_testing.test_extract import data
from src.pipeline.transform import transform_competitions

transformed_data = transform_competitions(data)

print("Transformed data:")
print(transformed_data)