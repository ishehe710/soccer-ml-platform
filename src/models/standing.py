from pydantic import BaseModel

class Standing(BaseModel):
    season_id: int
    team_id: int
    position: int
    games_played: int
    wins: int
    draws: int
    losses: int
    goals_for: int
    goals_against: int
    goal_difference: int
    form: str
    points: int