# in-projects imports
from src.pipeline.extract import extract_competitions

data = extract_competitions()

print("Extracting competition data")
print(data)