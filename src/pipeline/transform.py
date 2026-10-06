"""
Transformation functions for the Soccer ML Platform ETL pipeline.

Converts raw Sports Bzzoiro API responses into validated application models
before database loading.
"""
# in-project imports
from src.models.competition import Competition
from src.models.season import Season
from src.models.team import Team
from src.models.match import Match
from src.models.match_stats import MatchStats
from src.models.roster import Roster
from src.models.player import Player
from src.models.player_season_stats import PlayerSeasonStats
from src.models.standing import Standing
from src.config.models import IMG_API_URL
from src.database.queries import get_team_ids_from_match
from src.config.logger import create_logger

# Instantiating module logger
logger = create_logger(__name__)

'''
    Competitions
'''
def transform_competition(comp):
    """Transforms and validates a single instace of raw competition data.

    Args:
        comp (dict): A single raw extracted competition data. 

    Returns:
        Competition: A transformed and validated compeition data.
    """
    
    id = comp["id"]
    path = f"{IMG_API_URL}league/{id}"
    
    return Competition(
        api_id=id,
        name=comp["name"],
        country=comp["country"],
        logo_url=path  
    )
    
def transform_competitions(comps):
    """Transforms and validates all given raw compeition data.

    Args:
        comps (list[dict]): List of raw competition data.

    Returns:
        list[Competition]: List of transformed and validation competition data.
    """
    
    transformed_comps = [transform_competition(comp) for comp in comps]
    
    logger.info("Transfomring seasons was successful.")
    
    return transformed_comps
    
'''
    Seasons
'''
def transform_season(season, id):
    """Transform and validate a single instance of raw season data.

    Args:
        season (dict): Raw extracted season data.
        id (int): Officail api id of the season.

    Returns:
        Season: Transformed and validated season data.
    """
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
        
    logger.info("Transfomring seasons was successful.")
    
    return transformed_seasons

'''
    TEAMS
'''
def transform_team(team):
    """Transform and validate a single raw data info of a team.

    Args:
        team (dict): Raw team data information.

    Returns:
        Team: Transformed and validated team data.
    """
    
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
    """Transform and validate a list raw data for multiple teams.
    
    Args:
        teams (list[dict]): List of raw data for multiple teams.

    Returns:
        list[Team]: List of transformed and validated teams data.
    """
    
    transformed_teams = [transform_team(team) for team in teams]
    
    logger.info("Transforming teams was successful.")
    
    return transformed_teams

'''
    MATCHES
'''
def transform_match(match):
    """Transforming and validating for a single raw match data.

    Args:
        match (dict): Raw match data.

    Returns:
        Match: Transformed and validated match data.
    """
    
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
    """Transform and validate a list raw data for multiple matches.
        
    Args:
        teams (list[dict]): List of raw data for multiple matches.

    Returns:
        list[Match]: List of transformed and validated data for multiple matches.
    """
    transformed_matches = [transform_match(match) for match in matches]
    
    logger.info("Transforming matches was successful.")
    
    return transformed_matches

'''
        MATCH_STATS
'''
def transform_team_match_stats(team_match_stats, match_id, team_id):
    """Transforms and validates a single instance of raw match stats for one team of that game.

    Args:
        team_match_stats (dict): Raw match stats for a single game.
        match_id (int): Offical api of the match.
        team_id (_type_): The offical api id of the team's stats for that game.

    Returns:
        _type_: _description_
    """
    
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
    """Transforms and validates the home and away teams match stats for one match.

    Args:
        match_stats (dict): Raw match stats for a single game for the two teams.

    Returns:
        tuple(MatchStats, MatchStats): A tuple of transformed and validated match stats for both home and away teams.
    """
        
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
    """Transforming and validating match stats for multiple games.

    Args:
        all_match_stats (list[dict]): List of raw match stats for multiple games.

    Returns:
        list[MatchStats]: Transformed and validated match stats data for multiple teams.
    """
    
    transformed_match_stats = []
    
    for a_match_stats in all_match_stats:
        
        transformed_stats = transform_match_stats(a_match_stats)
        
        transformed_match_stats.extend(transformed_stats)
    
    logger.info("Transforming match stats was successful.")
    
    return transformed_match_stats
        
'''
        ROSTERS
'''
def transform_roster(roster):
    """Transform and validate raw data for a single team roster.

    Args:
        roster (dict): Raw data for a single roster

    Returns:
        list[roster]: Transformed and validated list of a team's roster.
    """
    
    team_id = roster["team_id"]
    players = roster["players"]
    
    transformed_roster = []
    
    for player in players:
        
        transformed_roster.append(Roster(
            team_id=team_id,
            player_id=player["id"],
            jersey_number=player["jersey_number"],
            position=player["position"]
        ))
    
    return transformed_roster

def transform_rosters(rosters):
    """Transform and validate raw data of multiple rosters.

    Args:
        rosters (list[dict]): List of raw data of rosters.

    Returns:
        list[list[Rosters]]: List of rosters data that have been transformed and validated.
    """
    
    transformed_rosters = [ transform_roster(roster) for roster in rosters]
    
    logger.info("Transforming rosters was successful.")
    
    return transformed_rosters

'''
        PLAYERS
'''
def transform_player(player_data):
    """Transforms and validates raw data of a single player.

    Args:
        player_data (dict): Raw data of a single player.

    Returns:
        Player: Transformed and validated player data.
    """
    
    id = player_data["id"]
    img_path = f"{IMG_API_URL}player/{id}"
    
    return Player(
        api_id=id,
        name=player_data["name"],
        short_name=player_data["short_name"],
        preferred_position=player_data["position"],
        date_of_birth=player_data["date_of_birth"],
        preferred_foot=player_data["preferred_foot"],
        nationality=player_data["nationality"],
        market_value_euro=player_data["market_value_eur"],
        wage_annual_euro=player_data["wage_eur_annual"],
        height_cm=player_data["height_cm"],
        player_img=img_path
    )
    
def transform_players(players):
    """Transform and validate raw data of multiple players.

    Args:
        players (list[dict]): List of raw player data.

    Returns:
        list[Player]: Transformed and validate data for multiple players.
    """
    
    transformed_players = [ transform_player(player) for player in players]
    
    logger.info("Transforming players was successful.")
    
    return transformed_players

'''
        PLAYER_SEASON_STATS
'''

# single player career stats
def transform_a_player_season_stats(player_seasons_data):
    """Transform and validate raw data for single player's career seasons stats.

    Args:
        player_seasons_data (dict): Raw data of a player's career stats.

    Returns:
        list[PlayerSeasonStats]: Transformed and validated data of a single player's career season stats.
    """
    
    player_id = player_seasons_data["player_id"]
    
    seasons = player_seasons_data["seasons"]
    
    transformed_seasons_data = []
    
    for season in seasons:
        
        transformed_seasons_data.append(
            PlayerSeasonStats(
                player_id=player_id,
                season_id=season["season_id"],
                comp_id=season["league_id"],
                team_id=season["team_id"],
                matches=season["matches"],
                minutes=season["minutes"],
                goals=season["goals"],
                assists=season["assists"],
                avg_rating=season["avg_rating"]
            )
        )
        
    return transformed_seasons_data
    
def transform_all_player_season_stats(player_seasons_stats):
    """Tranforming and validating raw data of mutiple players career season stats.

    Args:
        player_seasons_stats (list[dict]): List of raw multiple player season stats.

    Returns:
        list[PlayerSeasonStats]: List of transformed and validate player career season stats.
    """
    
    transformed_player_season_stats = []
    
    for player_stats in player_seasons_stats:
        
        transformed_stats = transform_a_player_season_stats(player_stats)
        
        transformed_player_season_stats.extend(transformed_stats)
        
    logger.info("Transforming player season stats was successful.")
        
    return transformed_player_season_stats

'''
        STANDINGS
'''
def transform_standing(raw_standing):
    """Transform and validate raw standing data for a single season.

    Args:
        raw_standing (dict): Raw standings data for a single season

    Returns:
        list[Standing]: Transformed and validated standings data for a single season, 
            if season id is available, otherwise None.
    """
    
    if raw_standing.get("season"):
    
        season_id = raw_standing["season"]["id"]
        standings_data = raw_standing["standings"]
        
        transformed_league_standings = []
        
        for team in standings_data:
            transformed_league_standings.append(
                Standing(
                    season_id=season_id,
                    team_id=team["team_id"],
                    position=team["position"],
                    games_played=team["played"],
                    wins=team["won"],
                    draws=team["drawn"],
                    losses=team["lost"],
                    goals_for=team["gf"],
                    goals_against=team["ga"],
                    goal_difference=team["gd"],
                    form=team["form"],
                    points=team["pts"]
                )              
            ) 
            
        return transformed_league_standings
    
    return None

def transform_standings(raw_standings):
    """Transforms and validates raw standings data for multiple seasons and compeitions.

    Args:
        raw_standings (list[dict]): List of raw standings for multiple seasons and competitions.

    Returns:
        list[Standings]: Transformed and validated standings data.
    """
    
    transformed_standings = []
    
    for raw_standing in raw_standings:
        transformed_standing = transform_standing(raw_standing)
        if transformed_standing:
            transformed_standings.extend(transformed_standing)
        
    logger.info("Transforming standings was successful.")
        
    return transformed_standings
