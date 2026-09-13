
# in-project imports
from src.models.competition import Competition
from src.models.season import Season
from src.models.team import Team
from src.models.match import Match
from src.models.match_stats import MatchStats
from src.config.models import IMG_API_URL
from src.database.queries import get_team_ids_from_match

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

'''
    MATCHES
'''

def transform_match(match):
    
    status = match["status"]
    
    if status == 'notstarted':
    
        return Match(
            api_id=match["id"],
            comp_id=match["league_id"],
            season_id=match["season_id"],
            home_team_id=match["home_team_id"],
            away_team_id=match["away_team_id"],
            match_date=match["event_date"],
            status=status
        )

    else:
        
        return Match(
            api_id=match["id"],
            comp_id=match["league_id"],
            season_id=match["season_id"],
            home_team_id=match["home_team_id"],
            away_team_id=match["away_team_id"],
            home_score=match["home_score"],
            away_score=match["away_score"],
            match_date=match["event_date"],
            status=status
        )
        
def transform_matches(matches):
    
    transformed_matches = [transform_match(match) for match in matches]
    
    return transformed_matches

'''
        MATCH_STATS
'''

def transform_team_match_stats(team_match_stats, match_id, team_id):
    
    xg_dict = team_match_stats.get("xg")
    crosses_dict = team_match_stats.get("crosses")
    
    
    return MatchStats(
        match_id=match_id,
        team_id=team_id,
        fouls=team_match_stats.get("fouls"),
        passes=team_match_stats.get("passes"),
        tackles=team_match_stats.get("tackles"),
        crosses= None if not crosses_dict else xg_dict.get("total"),
        offsides=team_match_stats.get("offsides"),
        big_saves=team_match_stats.get("big_saves"),
        clearances=team_match_stats.get("clearances"),
        free_kicks=team_match_stats.get("free_kicks"),
        big_chances=team_match_stats.get("big_chances"),
        total_shots=team_match_stats.get("total_shots"),
        corner_kicks=team_match_stats.get("corner_kicks"),
        yellow_cards=team_match_stats.get("yellow_cards"),
        red_cards=team_match_stats.get("red_cards"),
        expected_goals=team_match_stats.get("expected_goals"),
        accurate_passes=team_match_stats.get("accurate_passes"),
        ball_possession=team_match_stats.get("ball_possession"),
        goals_prevented=team_match_stats.get("goals_prevented"),
        shots_on_target=team_match_stats.get("shots_on_target"),
        shots_off_target=team_match_stats.get("shots_off_target"),
        big_chances_missed=team_match_stats.get("big_chances_missed"),
        errors_lead_to_a_goal=team_match_stats.get("errors_lead_to_a_goal"),
        errors_lead_to_a_shot=team_match_stats.get("errors_lead_to_a_shot"),
        pass_accuracy_pct=team_match_stats.get("pass_accuracy_pct"),
        xg= None if not xg_dict else xg_dict.get("actual") 
    )

def transform_match_stats(match_stats):
        
    match_id = match_stats["event_id"]
    stats = match_stats["stats"]
    home_match_stats = stats["home"]
    away_match_stats = stats["away"]
    
    # get team ids
    home_id, away_id = get_team_ids_from_match(match_id)
    
    # call helper function
    home_stats = transform_team_match_stats(home_match_stats, match_id, home_id)
    away_stats = transform_team_match_stats(away_match_stats, match_id, away_id)
    
    # return the data 
    return (home_stats, away_stats)

def transform_all_match_stats(all_match_stats):
    
    transformed_match_stats = []
    
    for a_match_stats in all_match_stats:
        
        transformed_stats = transform_match_stats(a_match_stats)
        
        transformed_match_stats.extend(transformed_stats)
    
    return transformed_match_stats
        
    
    
    