# imports
from datetime import datetime
# in-project imports
from src.database.connect_db import get_connection
from src.config.pipeline import PREMIER_LEAGUE_ID

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

def get_current_season_ids():
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            
            
            cur.execute(f"SELECT api_id FROM seasons WHERE (is_current = true AND comp_id = {PREMIER_LEAGUE_ID})")
            
            season_ids = [ row[0] for row in cur]
            
            return season_ids

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
        
def get_all_non_finished_match_ids():
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            
            cur.execute(f"SELECT api_id FROM matches WHERE status != 'finished'")
            
            ids = []
            
            for row in cur:
                id = row[0]
                ids.append(id)
                
            return ids
        
def get_match_ids_to_update():
    
    today = datetime.now()
    
    today_formatted = f"{today.year}-{today.month}-{today.day}"
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            
            cur.execute(f"SELECT api_id FROM matches WHERE (match_date <= '{today_formatted}' AND status != 'finished' AND status != 'canceled')")
            
            ids = []
                        
            for row in cur:
                id = row[0]
                ids.append(id)
                
            return ids

'''
        MATCH_STATS
'''

def get_match_ids_with_no_stats():
    
    match_ids = get_all_matches_finished_ids()
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            

            cur.execute("SELECT match_id FROM match_stats WHERE match_id = ANY(%s);", (match_ids,))
        
            # Fetch all matching records
            results = cur.fetchall()
            found_ids = {row[0] for row in results}
            missing_ids = set(match_ids) - found_ids
            
            return list(missing_ids)

'''
        PLAYERS
'''

def get_all_player_ids():
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            
            player_ids = []
            
            cur.execute("SELECT api_id FROM players")
            
            for id in cur:
                player_ids.append(id[0])
                
            return player_ids
        
# currently rostered in Premier League and Champions League
def get_all_active_player_ids():
    
    season_ids = get_current_season_ids()
    
    team_ids = []
    
    for season_id in season_ids:
        team_ids.extend(get_all_team_ids_from_standings(season_id))
        
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            
            
            cur.execute("""SELECT player_id FROM rosters WHERE team_id = ANY(%s)""", (team_ids,))
            
            result = cur.fetchall()
            player_ids = [id[0] for id in result]

            return player_ids
'''
        STANDINGS
'''

def get_all_team_ids_from_standings(season_id):
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            
            team_ids = []
            
            cur.execute(f"SELECT team_id FROM standings WHERE season_id = {season_id}")
            
            for row in cur:
                team_id = row[0]
                
                team_ids.append(team_id)
                
            return team_ids
