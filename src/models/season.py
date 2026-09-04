from pydantic import BaseModel

class Season(BaseModel):
    api_id: int
    comp_id: int
    start_date: str
    end_date: str
    is_current: bool