
# in-project imports
from src.models.competition import Competition
from src.models.season import Season
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
    
        
    