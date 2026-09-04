
# in-project imports
from src.database.connect_db import get_connection

'''
        COMPETITIONS
'''
def load_competition(competition):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO competitions
                    (api_id, comp_name, country, logo_url, created_at)
                VALUES
                    (%s, %s, %s, %s, NOW())
                ON CONFLICT (api_id)
                DO UPDATE SET
                    comp_name = EXCLUDED.comp_name,
                    country = EXCLUDED.country,
                    logo_url = EXCLUDED.logo_url;
                """,
                (
                    competition.api_id,
                    competition.name,
                    competition.country,
                    competition.logo_url,
                ),
            )
            
def load_competitions(comps):
    
    for comp in comps:
        load_competition(comp)
        
'''
        SEASONS
'''
def load_season(season):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO seasons
                    (api_id, comp_id, start_date, end_date, is_current, created_at)
                VALUES
                    (%s, %s, %s, %s, %s, NOW())
                ON CONFLICT (api_id)
                DO UPDATE SET
                    start_date = EXCLUDED.start_date,
                    end_date = EXCLUDED.end_date,
                    is_current = EXCLUDED.is_current
                """,
                (
                    season.api_id,
                    season.comp_id,
                    season.start_date,
                    season.end_date,
                    season.is_current,
                ),
            )
            
def load_seasons(seasons):
    
    for season in seasons:
        load_season(season)