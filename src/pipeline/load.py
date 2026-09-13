
# in-project imports
from src.database.connect_db import get_connection
from src.database.queries import team_exists, get_competition_ids
from src.pipeline.extract import extract_a_team
from src.pipeline.transform import transform_team
from src.config.pipeline import COMPETITIONS

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
            conn.commit()
            
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
            
            conn.commit()
            
def load_seasons(seasons):
    
    for season in seasons:
        load_season(season)
        
'''
        TEAMS
'''
def load_team(team):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO teams 
                    (api_id, short_name, team_name, country, logo_url, created_at)
                VALUES
                    (%s, %s, %s, %s, %s, NOW())
                ON CONFLICT (api_id)
                DO UPDATE SET
                    short_name = EXCLUDED.short_name,     
                    team_name = EXCLUDED.team_name,     
                    country = EXCLUDED.country,     
                    logo_url = EXCLUDED.logo_url     
                """,
                (
                    team.api_id,
                    team.short_name, 
                    team.team_name,
                    team.country,
                    team.logo_url
                )
            )
            
            conn.commit()

def load_team_v2(team_api_id):
    team_data = extract_a_team(team_api_id)
    transformed_team_data = transform_team(team_data)
    load_team(transformed_team_data)

def load_teams(teams):
    
    for team in teams:
        load_team(team)

        
'''
        MATCHES
'''
def load_match(match):
    with get_connection() as conn:
        with conn.cursor() as cur:
            
            if not team_exists(match.home_team_id):
                load_team_v2(match.home_team_id)
            
            if not team_exists(match.away_team_id):
                load_team_v2(match.away_team_id)
                
            if match.comp_id in COMPETITIONS:
            
                cur.execute(
                    """
                    INSERT INTO matches
                        (api_id, comp_id, season_id, home_team_id, away_team_id, home_score, away_score, match_date, status, created_at)
                    VALUES 
                        (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                    ON CONFLICT (api_id)
                    DO UPDATE SET
                        comp_id = EXCLUDED.comp_id,
                        season_id = EXCLUDED.season_id,
                        home_team_id = EXCLUDED.home_team_id,
                        away_team_id = EXCLUDED.away_team_id,
                        home_score = EXCLUDED.home_score,
                        away_score = EXCLUDED.away_score,
                        match_date = EXCLUDED.match_date,
                        status = EXCLUDED.status
                    """,
                    (
                        match.api_id,
                        match.comp_id,
                        match.season_id,
                        match.home_team_id,
                        match.away_team_id,
                        match.home_score,
                        match.away_score,
                        match.match_date,
                        match.status
                    )
                )
            
                conn.commit()

def load_matches(matches):
    
    for match in matches:
        load_match(match)
        
'''
        MATCH_STATS
'''

# per team
def load_a_match_stats(a_match_stats):
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            
            #if not team_exists(a_match_stats.team_id):
            #    load_team_v2(a_match_stats.team_id)
            
            cur.execute(
                """
                INSERT INTO match_stats 
                    (match_id, team_id, fouls, passes, tackles, crosses, offsides, big_saves, clearances, free_kicks, big_chances, total_shots, corner_kicks, yellow_cards, red_cards, expected_goals, accurate_passes, ball_possession, goals_prevented, shots_on_target, shots_off_target, big_chances_missed, errors_lead_to_a_goal, errors_lead_to_a_shot, pass_accuracy_pct, xg, created_at)
                VALUES
                    (      %s,      %s,    %s,     %s,      %s,      %s,       %s,        %s,         %s,         %s,          %s,          %s,           %s,           %s,        %s,             %s,              %s,              %s,              %s,              %s,               %s,                 %s,                    %s,                    %s,                %s, %s, NOW())
                ON CONFLICT (match_id)
                DO UPDATE SET
                    team_id = EXCLUDED.team_id,
                    fouls = EXCLUDED.fouls,
                    passes = EXCLUDED.passes,
                    tackles = EXCLUDED.tackles,
                    crosses = EXCLUDED.crosses,
                    offsides = EXCLUDED.offsides,
                    big_saves = EXCLUDED.big_saves,
                    clearances = EXCLUDED.clearances,
                    free_kicks = EXCLUDED.free_kicks,
                    big_chances = EXCLUDED.big_chances,
                    total_shots = EXCLUDED.total_shots,
                    corner_kicks = EXCLUDED.corner_kicks,
                    yellow_cards = EXCLUDED.yellow_cards,
                    red_cards = EXCLUDED.red_cards,
                    expected_goals = EXCLUDED.expected_goals,
                    accurate_passes = EXCLUDED.accurate_passes,
                    ball_possession = EXCLUDED.ball_possession,
                    goals_prevented = EXCLUDED.goals_prevented,
                    shots_on_target = EXCLUDED.shots_on_target,
                    shots_off_target = EXCLUDED.shots_off_target,
                    big_chances_missed = EXCLUDED.big_chances_missed,
                    errors_lead_to_a_goal = EXCLUDED.errors_lead_to_a_goal,
                    errors_lead_to_a_shot = EXCLUDED.errors_lead_to_a_shot,
                    pass_accuracy_pct = EXCLUDED.pass_accuracy_pct,
                    xg = EXCLUDED.xg
                """,
                (
                    
                    a_match_stats.match_id,
                    a_match_stats.team_id,
                    a_match_stats.fouls,
                    a_match_stats.passes,
                    a_match_stats.tackles,
                    a_match_stats.crosses,
                    a_match_stats.offsides,
                    a_match_stats.big_saves,
                    a_match_stats.clearances,
                    a_match_stats.free_kicks,
                    a_match_stats.big_chances,
                    a_match_stats.total_shots,
                    a_match_stats.corner_kicks,
                    a_match_stats.yellow_cards,
                    a_match_stats.red_cards,
                    a_match_stats.expected_goals,
                    a_match_stats.accurate_passes,
                    a_match_stats.ball_possession,
                    a_match_stats.goals_prevented,
                    a_match_stats.shots_on_target,
                    a_match_stats.shots_off_target,
                    a_match_stats.big_chances_missed,
                    a_match_stats.errors_lead_to_a_goal,
                    a_match_stats.errors_lead_to_a_shot,
                    a_match_stats.pass_accuracy_pct,
                    a_match_stats.xg
                )            
            )
        
            conn.commit()
            
# loading all matches per team stats       
def load_all_match_stats(all_match_stats):
    
    for match_stats in all_match_stats:
        load_a_match_stats(match_stats)

'''
        ROSTERS
'''

def load_roster(roster):
    
    for roster_player in roster:
    
        with get_connection() as conn:
            with conn.cursor() as cur:
                
                cur.execute(
                    """
                    INSERT INTO rosters
                        (team_id, player_id, jersey_number, position, created_at)
                    VALUES 
                        (%s, %s, %s, %s, NOW())
                    ON CONFLICT (team_id)
                    DO UPDATE SET
                        player_id = EXCLUDED.player_id,
                        jersey_number = EXCLUDED.jersey_number,
                        position = EXCLUDED.position
                    """,
                        (
                            roster_player.team_id,
                            roster_player.player_id, 
                            roster_player.jersey_number,
                            roster_player.position
                        )
                    )

                conn.commit()
            
def load_rosters(rosters):
    
    for roster in rosters:
        load_roster(roster)

'''
        PLAYERS
'''

def load_player(player):
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            
            cur.execute(
                """
                INSERT INTO players 
                    (api_id, name, short_name, preferred_position, date_of_birth, preferred_foot, nationality, market_value_euro, wage_annual_euro, height_cm, player_img, created_at)
                VALUES
                    (    %s,   %s,         %s,                 %s,            %s,             %s,          %s,                 %s,              %s,        %s,         %s,      NOW())  
                ON CONFLICT (api_id)
                DO UPDATE SET
                    name = EXCLUDED.name,
                    short_name = EXCLUDED.short_name,
                    preferred_position = EXCLUDED.preferred_position,
                    date_of_birth = EXCLUDED.date_of_birth,
                    preferred_foot = EXCLUDED.preferred_foot,
                    nationality = EXCLUDED.nationality,
                    market_value_euro = EXCLUDED.market_value_euro,
                    wage_annual_euro = EXCLUDED.wage_annual_euro,
                    height_cm = EXCLUDED.height_cm,
                    player_img = EXCLUDED.player_img          
                """,
                (
                    player.api_id,
                    player.name,
                    player.short_name, 
                    player.preferred_position,
                    player.date_of_birth,
                    player.preferred_foot,
                    player.nationality,
                    player.market_value_euro,
                    player.wage_annual_euro,
                    player.height_cm,
                    player.player_img
                )
            )
            
            conn.commit()
            
def load_players(players):

    for player in players:
        load_player(player)
        
