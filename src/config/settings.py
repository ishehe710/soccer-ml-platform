from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """This model is used for environment variables needed for the program and other configurable 
        values for the application.

    """
    
    # Enviroment variable stuff
    sports_bzzoiro_api_url: str
    sports_bzzoiro_api_key: str

    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str
    
    # Data Pipeline
    seasons_to_load: int = 6

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

# Loading configurable settings
settings = Settings()