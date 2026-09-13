from pydantic import BaseModel

class MatchStats(BaseModel):
    match_id: int
    team_id: int
    fouls: int | None = None
    passes: int | None = None
    tackles: int | None = None
    crosses: int | None = None
    offsides: int | None = None
    big_saves: int | None = None
    clearances: int | None = None
    free_kicks: int | None = None
    big_chances: int | None = None
    total_shots: int | None = None
    corner_kicks: int | None = None
    yellow_cards: int | None = None
    red_cards: int | None = None
    expected_goals: float | None = None
    accurate_passes: int | None = None
    ball_possession: int | None = None
    goals_prevented: float | None = None
    shots_on_target: int | None = None
    shots_off_target: int | None = None
    big_chances_missed: int | None = None
    errors_lead_to_a_goal: int | None = None
    errors_lead_to_a_shot: int | None = None
    pass_accuracy_pct: float | None = None
    xg: float | None = None