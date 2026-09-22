from pydantic import BaseModel

class PlayerSeasonStats(BaseModel):
    player_id: int
    season_id: int
    comp_id: int
    team_id: int
    matches: int
    minutes: int
    goals: int
    assists: int
    avg_rating: float | None = None