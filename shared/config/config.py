import logging
from pathlib import Path

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

logging.getLogger('config').setLevel(logging.INFO)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parents[2] / ".env"),
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )

    #   Postgres MANUFACTORY
    POSTGRES_USER_MANUFACTORY: str
    POSTGRES_PASSWORD_MANUFACTORY: str
    POSTGRES_HOST_MANUFACTORY: str
    POSTGRES_PORT_INDUSTRIAL: int
    POSTGRES_DB_MANUFACTORY: str

    #   Postgres INDUSTRIAL
    POSTGRES_USER_INDUSTRIAL: str
    POSTGRES_PASSWORD_INDUSTRIAL: str
    POSTGRES_HOST_INDUSTRIAL: str
    POSTGRES_DB_INDUSTRIAL: str

    #   Telegram-Bot
    BOT_TOKEN_TEST: str
    CHAT_ID_TEST: str
    BOT_TOKEN: str
    CHAT_ID: str

    #   API connect
    API_IP: str
    API_PORT: str
    API_POSTFIX: str

    #   MQTT
    MQTT_CLIENT_ID: str
    MQTT_HOST: str
    MQTT_PORT: int

    #   PLC
    DB_NUMBER: int

    #   Redis
    REDIS_HOST: str
    REDIS_PORT: int

    @staticmethod
    def _get_postgres_url(user: str, password: str, host: str, db: str, async_mode: bool) -> PostgresDsn:
        protocol = "postgresql+asyncpg" if async_mode else "postgresql"
        url = f"{protocol}://{user}:{password}@{host}/{db}"
        return PostgresDsn(url)  # Создание PostgresDsn из строки

    @property
    def manufactory_db_url_async(self) -> PostgresDsn:
        return self._get_postgres_url(
            self.POSTGRES_USER_MANUFACTORY,
            self.POSTGRES_PASSWORD_MANUFACTORY,
            self.POSTGRES_HOST_MANUFACTORY,
            self.POSTGRES_DB_MANUFACTORY,
            async_mode=True,
        )

    @property
    def manufactory_db_url_sync(self) -> PostgresDsn:
        return self._get_postgres_url(
            self.POSTGRES_USER_MANUFACTORY,
            self.POSTGRES_PASSWORD_MANUFACTORY,
            self.POSTGRES_HOST_MANUFACTORY,
            self.POSTGRES_DB_MANUFACTORY,
            async_mode=False,
        )

    @property
    def industrial_db_url_async(self) -> PostgresDsn:
        return self._get_postgres_url(
            self.POSTGRES_USER_INDUSTRIAL,
            self.POSTGRES_PASSWORD_INDUSTRIAL,
            self.POSTGRES_HOST_INDUSTRIAL,
            self.POSTGRES_DB_INDUSTRIAL,
            async_mode=True,
        )

    @property
    def industrial_db_url_sync(self) -> PostgresDsn:
        return self._get_postgres_url(
            self.POSTGRES_USER_INDUSTRIAL,
            self.POSTGRES_PASSWORD_INDUSTRIAL,
            self.POSTGRES_HOST_INDUSTRIAL,
            self.POSTGRES_DB_INDUSTRIAL,
            async_mode=False,
        )


settings = Settings()
