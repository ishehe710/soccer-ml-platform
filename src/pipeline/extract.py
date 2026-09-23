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
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import datetime

# in-project imports
from src.config.settings import settings
from src.config.pipeline import COMPETITIONS, PREMIER_LEAGUE_ID
from src.database.queries import (
    get_seasons_api_ids, 
    get_all_matches_finished_ids,
    get_all_team_ids,
    get_all_player_ids,
    get_all_active_player_ids
    )

'''
        ESTABLISH session
'''

session = requests.Session()

retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"]
)

adapter = HTTPAdapter(max_retries=retry_strategy)

session.mount("http://", adapter)
session.mount("https://", adapter)


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
    r = session.get(settings.sports_bzzoiro_api_url + path, headers=headers, timeout=30)
    
    
    print("URL:", r.url)
    print("Status:", r.status_code)

    r.raise_for_status()
    
    
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
    
    print("Fetching competitions was succesful!")
    
    # finding the appropriate leagues
    raw_comps_data = response['results']
    
    comps_data = []
    
    for comp_id in COMPETITIONS:            # desired competitions
        for comp in raw_comps_data:

            if comp['id'] == comp_id:
                comps_data.append(comp)
                
    print("Succesfully extracted competitions.")
    
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

        print("Fetching season data...")
        response = fetch_api_data(path) # seasons info
        print("Fetching seasons was succesful.")

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
    
    print("Extracting seasons was successful.")
    
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
    print("Fetching team data...")
    for competition_id in COMPETITIONS:
        
        path = f"/api/v2/teams/?league_id={competition_id}&in_competition=true"
        
        response = fetch_api_data(path)
        
        raw_data = response['results']
        
        teams_data += raw_data
    
    print("Fetching team data was successful.")
    print("Extracting team data succesfull.")
    
    return teams_data

def extract_a_team(team_id):
    
    path = f"/api/v2/teams/{team_id}"
    
    print(f"Fetching team with id = {team_id} info...")
    response = fetch_api_data(path)
    print(f"Fetched succesful for getting team data for id = {team_id}.")
    print(f"Extracting team with id = {team_id} successful.")
    
    return response

'''
        MATCHES
'''

def extract_matches():
    
    # Getting seasons api ids according to Sports Bzzoiro Data API
    seasons_api_ids = get_seasons_api_ids()
    
    all_matches = []
    
    print("Fetching match data from API...")
    for season_id in seasons_api_ids:
        
        offset = 0
        limit = 200
                
        while True:
            
            path = f"/api/v2/events/?limit={limit}&offset={offset}&season_id={season_id}" 
            response = fetch_api_data(path)
            
            matches = response["results"]
                        
            # Exceeded total number of matches
            if not matches:
                break
            
            all_matches.extend(matches)
    
            # last batch of matches
            if len(matches) < limit:
                break
            
            offset += limit
    
    print("Fetch successful for getting match data from API.")
    print("Extracting match data from API.")
    
    return all_matches

'''
        MATCH_STATS
'''

def extract_match_stats():
    
    match_ids = get_all_matches_finished_ids()
    
    all_matches_stats = []
    
    print(f"Fetching match stats from API...")

    for i, match_id in enumerate(match_ids):
        print(f"Fetching match stats {i+1}/{len(match_ids)}")
        
        path = f"/api/v2/events/{match_id}/stats"
        
        response = fetch_api_data(path) # singular match stats
        
        match_stats = response
        
        all_matches_stats.append(match_stats)
            
    print("Fetching match stats was succesful.")
    print("Extraction of match stats was successful.")
    
    return all_matches_stats

'''
        PLAYER_SEASON_STATS
'''

def extract_player_season_stats():
    
    player_ids = get_all_player_ids()
    
    data = []
    
    for i, player_id in enumerate(player_ids):
        print(f"Fetching player career stats {i+1}/{len(player_ids)}")
        
        path = f"/api/v2/players/{player_id}/career/"
        
        response = fetch_api_data(path)
        
        data.append(response)
        
    print("Extracting player season stats was successful.")
    
    return data

'''
        PLAYERS + ROSTERS
'''

def extract_rosters_and_players():
    
    team_ids = get_all_team_ids()
    
    roster_data = []
    player_data = []
    
    for i, team_id in enumerate(team_ids):
        print(f"Fetching team's roster data {i+1}/{len(team_ids)}")

        roster_path = f"/api/v2/teams/{team_id}/squad/"
        
        roster_response = fetch_api_data(roster_path)
        
        players = roster_response["players"]
        
        roster_data.append(roster_response)
        
        for player in players:
            
            id = player["id"]
            
            player_path = f"/api/v2/players/{id}/"
            
            player_response = fetch_api_data(player_path)
            
            player_data.append(player_response)
            
    print("Extracting rosters was successful.")
    
    return (roster_data, player_data)

'''
        STANDINGS
'''

def extract_standings():
    
    season_ids = get_seasons_api_ids()
    
    standings_data = []
    for season_id in season_ids:
            
        path = f"/api/v2/leagues/{PREMIER_LEAGUE_ID}/standings/?season_id={season_id}"
        
        response = fetch_api_data(path)
        
        standings_data.append(response)
    
    print("Extracting standings was successful.")
    
    return standings_data


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        UPDATE FUNCTIONS
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def extract_match_updates(match_ids):
        
    raw_data = []
    n = len(match_ids)
    for i, match_id in enumerate(match_ids):
        print(f"Fetching updated match info for matches {i+1}/{n}")
        path = f"/api/v2/events/{match_id}"
        
        response = fetch_api_data(path)
        
        raw_data.append(response)
    
    return raw_data

'''
        MATCH STATS
'''


def extract_match_stats_updates(match_ids):
    
        
    raw_data = []
    n = len(match_ids)


    for i, match_id in enumerate(match_ids):
        print(f"Fetching updated match stats for matches {i+1}/{n}")
        path = f"/api/v2/events/{match_id}/stats"
        
        response = fetch_api_data(path)
        
        raw_data.append(response)
    
    return raw_data

def extract_player_season_stats_updates():
    
    player_ids = get_all_active_player_ids()
    
    raw_data = []
    n = len(player_ids)

    for i, player_id in enumerate(player_ids):
        print(f"Fetching for updated player career stats for players {i+1}/{n}")
        path = f"/api/v2/players/{player_id}/career/"
        
        response = fetch_api_data(path)
        
        raw_data.append(response)
    
    return raw_data

def extract_standing_updates(season_id):
    
    path = f"/api/v2/leagues/{PREMIER_LEAGUE_ID}/standings/?season_id={season_id}"

    return [fetch_api_data(path)]

