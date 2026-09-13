from pydantic import BaseModel

class Player(BaseModel):
    api_id: int
    name: str
    short_name: str | None = None
    preferred_position: str | None = None
    date_of_birth: str | None = None
    preferred_foot: str | None = None
    nationality: str | None = None
    market_value_euro: int | None = None
    wage_annual_euro: int | None = None
    height_cm: int | None = None
    player_img: str | None = None