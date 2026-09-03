
# in-project imports
from src.models.competition import Competition
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
    
    
    