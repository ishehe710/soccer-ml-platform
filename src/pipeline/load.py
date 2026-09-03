
# in-project imports
from src.database.connect_db import get_connection


def load_competition(competition):
    print(competition)
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