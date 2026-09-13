from pydantic import BaseModel

class Match(BaseModel):
    api_id: int
    comp_id: int
    season_id: int
    home_team_id: int
    away_team_id: int
    home_score: int | None = None
    away_score: int | None = None
    match_date: str | None = None
    status: str