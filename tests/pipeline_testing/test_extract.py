# in-projects imports
from src.pipeline.extract import extract_competitions, extract_seasons

data = extract_seasons()

print("Extracting seasons data")
print(data)