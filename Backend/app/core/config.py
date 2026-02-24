from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App
    APP_NAME: str
    DEBUG: bool = True
    API_V1_STR: str 
    
    # Supabase
    DATABASE_URL: str

    # Redis
    REDIS_URL: str
    
    # JWT
    SECRET_KEY: str
    ALGORITHM: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int 
    REFRESH_TOKEN_EXPIRE_DAYS: int
    JWT_ISSUER : str

    # Security
    BCRYPT_ROUNDS: int = 12
    
    # @property
    # def DATABASE_URL(self) -> str:
    #     return (
    #         f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
    #         f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    #     )

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }

settings = Settings()
