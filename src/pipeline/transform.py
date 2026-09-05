
# in-project imports
from src.models.competition import Competition
from src.models.season import Season
from src.models.team import Team
from src.config.models import IMG_API_URL

'''
    Competitions
'''

def transform_competition(comp):
    
    id = comp["id"]
    path = f"{IMG_API_URL}league/{id}"
    
    return Competition(
        api_id=id,
        name=comp["name"],
        country=comp["country"],
        logo_url=path  
    )
    
def transform_competitions(comps):
    
    transformed_comps = [transform_competition(comp) for comp in comps]
    
    return transformed_comps
    
'''
    Seasons
'''

def transform_season(season, id):
    return Season(
        api_id=season['id'],
        comp_id=id,
        start_date=season['start_date'],
        end_date=season['end_date'],
        is_current=season['is_current']
    )
    
def transform_seasons(seasons):
    """Converts raw seasons data into Season Pydantic Model objects for loading 
        in the database.

    Args:
        seasons (dict): A dict containing seasons info by league.

    Returns:
        list[Season]: A list of Season objects. 
    """

    transformed_seasons = []
    for comp_id, seasons_data in seasons.items():
        transformed_seasons += [transform_season(season, comp_id) for season in seasons_data]
    
    return transformed_seasons

'''
    TEAMS
'''

def transform_team(team):
    
    id =  team["id"]
    path = f"{IMG_API_URL}team/{id}"

    return Team(
        api_id=team["id"],
        short_name=team["short_name"],
        team_name=team["name"],
        country=team["country"],
        logo_url=path
    )
        
def transform_teams(teams):
    
    transformed_teams = [transform_team(team) for team in teams]
    
    return transformed_teams