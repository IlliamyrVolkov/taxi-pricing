from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GRPC_PORT: int = 50051
    GRPC_HOST: str = "[::]"

    ENV_NAME: str = "local"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
