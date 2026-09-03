from pydantic import BaseModel

class Competition(BaseModel):
    api_id: int
    name: str
    country: str
    logo_url: str