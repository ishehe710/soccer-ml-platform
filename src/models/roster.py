from pydantic import BaseModel

class Roster(BaseModel):
    team_id: int
    player_id: int
    jersey_number: int | None = None
    position: str | None = None
    