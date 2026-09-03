"""
extract.py

Handles extraction of raw soccer data from the Bzzoiro Sports Data API.

Responsibilities:
    - Build API request URLs.
    - Authenticate API requests.
    - Fetch raw data from the Bzzoiro API.
    - Return API responses for downstream transformation.

Pipeline stage:
    Bzzoiro Sports Data API -> [EXTRACT] -> Raw API data
"""
import requests

# in-project imports
from src.config.settings import settings
from src.config.pipeline import COMPETITIONS

# base fetch
def fetch_api_data(path):
    """This function fetche API data indicated by the parameter path, form the SPORT 
        BZZOIRO Data website.

    Args:
        path (str): The path of what kind of data to get from website.

    Returns:
        A Python dictionary of the API request data
    """
    
    # fetch request for data 
    headers = {"Authorization": f"Token {settings.sports_bzzoiro_api_key}"}
    r = requests.get(settings.sports_bzzoiro_api_url + path, headers=headers)
    
    return r.json()


def extract_competitions():
    
    path = f"/api/v2/leagues"
    
    print("Fetching competition data...")
    
    response = fetch_api_data(path)
    
    print("Fetch succesful!")
    
    # finding the appropriate leagues
    raw_comps_data = response['results']
    
    comps_data = []
    
    for comp_id in COMPETITIONS: # desired competitions
        for comp in raw_comps_data:

            if comp['id'] == comp_id:
                comps_data.append(comp)
                
    return comps_data
    
    
    
    