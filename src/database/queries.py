# in-project imports
from src.database.connect_db import get_connection

'''
        COMPETITIONS
'''
def get_competition_ids():
    with get_connection() as conn:
        with conn.cursor() as cur:
            
            cur.execute("SELECT api_id FROM competitions")
            
            ids = []
            
            for comp_api_id in cur:
                ids.append(comp_api_id[0])
                
            return ids
            

'''
        SEASONS
'''
def get_seasons_api_ids():
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            
            cur.execute("SELECT api_id FROM seasons")
            
            seasons_api_ids = []
            for id in cur:
                seasons_api_ids.append(id[0])
            
            print("Successfully got seasons api_ids from database.")
            return seasons_api_ids

'''
        TEAMS
'''
def team_exists(team_api_id):
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            
            cur.execute(f"SELECT * FROM teams WHERE api_id = {team_api_id}")
            if cur.rowcount: # row count > 0
                return True
            else:
                return False

def get_all_team_ids():
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            
            team_ids = []
            
            cur.execute("SELECT api_id FROM TEAMS")
            
            for team_id in cur:
                team_ids.append(team_id[0])
                
            return team_ids

'''
        MATCHES
'''
def get_all_matches_finished_ids():
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            
            match_ids = []
            cur.execute("SELECT api_id FROM matches WHERE status = 'finished'")
            
            for match_id in cur:
                match_ids.append(match_id[0])
                
            return match_ids

def get_team_ids_from_match(match_id):
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            
            cur.execute(f"SELECT home_team_id, away_team_id FROM matches WHERE api_id = {match_id}")
            
            data = cur.fetchall()
            
            home_team = data[0][0]
            away_team = data[0][1]
            return (home_team, away_team)
            
