from pydantic import BaseModel

class Team(BaseModel):
    api_id: int
    short_name: str
    team_name: str
    country: str
    logo_url: str