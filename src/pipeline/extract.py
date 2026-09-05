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
from datetime import datetime

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


'''
        COMPETITIONS
'''
def extract_competitions():
    """Calls the Sports Bzzoiro Data API to get information for competitions for the website.

    Returns:
        list: A list of dicts that contain league data.
            [{}, ..., {}]
    """
    
    path = f"/api/v2/leagues"
    
    print("Fetching competition data...")
    
    response = fetch_api_data(path)
    
    print("Fetch succesful!")
    
    # finding the appropriate leagues
    raw_comps_data = response['results']
    
    comps_data = []
    
    for comp_id in COMPETITIONS:            # desired competitions
        for comp in raw_comps_data:

            if comp['id'] == comp_id:
                comps_data.append(comp)
                
    return comps_data


'''
        SEASONS
'''
def extract_seasons():
    """Calls the Sports Bzzoiro Data API to get information for current and historic season ata for the website.

    Returns:
        dict: Where the key is an int for competition API id and the value is the latest 6 seasons data for all competitions.
            {int: list}
    """
    
    data = {}
    for competition_id in COMPETITIONS:
        
        path = f"/api/v2/leagues/{competition_id}/seasons/"

        response = fetch_api_data(path) # seasons info

        # Finding appropriate seasons
        seasons_data = response['seasons']

        current_season_year = datetime.now().year
        season_years = [current_season_year - i for i in range(settings.seasons_to_load)]

        comp_seasons_data = []

        for season in seasons_data:
            for start_year in season_years:
                if season['year'] == start_year:
                    comp_seasons_data.append(season)
                
        data[competition_id] = comp_seasons_data
    
    return data

'''
        TEAMS
'''

def extract_teams():
    """Calls the Sports Bzzoiro Data API to get information for in competition teams data
        per competition indicated

    Returns:
        list[dict]: A list of dicts that have team info.
    """
    
    teams_data = []
    for competition_id in COMPETITIONS:
        
        path = f"/api/v2/teams/?league_id={competition_id}&in_competition=true"
        
        response = fetch_api_data(path)
        
        raw_data = response['results']
        
        teams_data += raw_data
        
    return teams_data

