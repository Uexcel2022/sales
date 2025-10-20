from pydantic_settings import BaseSettings,SettingsConfigDict

class DBSettings(BaseSettings):
    POSTGRES_USER: str = "eiie"
    POSTGRES_PASSWORD: str = "qjq09"
    POSTGRES_SERVER: str = "whewre"
    POSTGRES_PORT: int = 5000
    POSTGRES_DB: str = "qmqmw"

    model_config = SettingsConfigDict(
        env_file= "./.env",
        env_ignore_empty= True,
        extra="ignore"
    )

    @property
    def POSTGRES_URL(self)-> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

settings =  DBSettings()