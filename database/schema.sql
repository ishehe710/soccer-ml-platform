/* 
    Creates the necessary tables for the platform
*/

CREATE TABLE competitions (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    api_id INTEGER UNIQUE NOT NULL,
    comp_name TEXT NOT NULL,
    country TEXT NOT NULL,
    logo_url TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE seasons (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    api_id INTEGER UNIQUE NOT NULL,
    comp_id INTEGER REFERENCES competitions(api_id),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_current BOOL NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE standings (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    season_id INTEGER REFERENCES seasons(api_id),
    team_id INTEGER REFERENCES teams(api_id),
    UNIQUE (season_id, team_id),
    position INTEGER NOT NULL,
    games_played INTEGER NOT NULL,
    wins INTEGER NOT NULL,
    draws INTEGER NOT NULL,
    losses INTEGER NOT NULL,
    goals_for INTEGER NOT NULL,
    goals_against INTEGER NOT NULL,
    goal_difference INTEGER NOT NULL,
    form TEXT NOT NULL,
    points INTEGER NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE teams (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    api_id INTEGER UNIQUE NOT NULL,
    short_name TEXT NOT NULL,
    team_name TEXT NOT NULL,
    country TEXT NOT NULL,
    logo_url TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE rosters (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    team_id INTEGER REFERENCES teams(api_id),
    player_id INTEGER REFERENCES players(api_id),
    UNIQUE (team_id, player_id),
    jersey_number INTEGER,
    position TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE players (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    api_id INTEGER UNIQUE NOT NULL,
    name TEXT NOT NULL,
    short_name TEXT,
    preferred_position TEXT,
    date_of_birth DATE,
    preferred_foot TEXT,
    nationality TEXT,
    market_value_euro INTEGER,
    wage_annual_euro INTEGER,
    height_cm INTEGER,
    player_img TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE matches (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    api_id INTEGER UNIQUE NOT NULL,
    comp_id INTEGER REFERENCES competitions(api_id),
    season_id INTEGER REFERENCES seasons(api_id),
    home_team_id INTEGER REFERENCES teams(api_id),
    away_team_id INTEGER REFERENCES teams(api_id),
    final_score TEXT,
    home_score INTEGER,
    away_score INTEGER,
    match_date DATE NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE match_stats (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    match_id INTEGER UNIQUE REFERENCES matches(api_id),
    team_id INTEGER REFERENCES teams(api_id),
    fouls INTEGER,
    passes INTEGER,
    tackles INTEGER,
    crosses INTEGER,
    offsides INTEGER,
    big_saves INTEGER,
    clearances INTEGER,
    free_kicks INTEGER,
    big_chances INTEGER,
    total_shots INTEGER,
    corner_kicks INTEGER,
    yellow_cards INTEGER,
    red_cards INTEGER,
    expected_goals DECIMAL,
    accurate_passes INTEGER,
    ball_possession INTEGER,
    goals_prevented DECIMAL,
    shots_on_target INTEGER,
    shots_off_target INTEGER,
    big_chances_missed INTEGER,
    errors_lead_to_a_goal INTEGER,
    errors_lead_to_a_shot INTEGER,
    pass_accuracy_pct DECIMAL,
    xg DECIMAL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE player_season_stats (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    player_id INTEGER REFERENCES players(api_id),
    season_id INTEGER REFERENCES seasons(api_id),
    comp_id INTEGER REFERENCES competitions(api_id),
    team_id INTEGER REFERENCES teams(api_id),
    UNIQUE (player_id, season_id, team_id, comp_id),
    matches INTEGER NOT NULL,
    minutes INTEGER NOT NULL,
    goals INTEGER NOT NULL,
    assists INTEGER NOT NULL,
    avg_rating DECIMAL,
    created_at TIMESTAMPTZ NOT NULL
);