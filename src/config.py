from pydantic import PostgresDsn, computed_field, Field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_DB: str

    BOT_TOKEN_TEST: str
    CHAT_ID_TEST: str
    BOT_TOKEN: str
    CHAT_ID: str

    API: str
    MQTT_HOST: str = Field(..., env="MQTT_HOST")
    MQTT_PORT: int = Field(1883, env="MQTT_PORT")
    MQTT_USERNAME: str = Field("", env="MQTT_USERNAME")
    MQTT_PASSWORD: str = Field("", env="MQTT_PASSWORD")

    @computed_field
    @property
    def asyncpg_url(self) -> PostgresDsn:
        """
        This is a computed field that generates a PostgresDsn URL for asyncpg.

        The URL is built using the MultiHostUrl.build method, which takes the following parameters:
        - scheme: The scheme of the URL. In this case, it is "postgresql+asyncpg".
        - username: The username for the Postgres database, retrieved from the POSTGRES_USER environment variable.
        - password: The password for the Postgres database, retrieved from the POSTGRES_PASSWORD environment variable.
        - host: The host of the Postgres database, retrieved from the POSTGRES_HOST environment variable.
        - path: The path of the Postgres database, retrieved from the POSTGRES_DB environment variable.

        Returns:
            PostgresDsn: The constructed PostgresDsn URL for asyncpg.
        """
        url = MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            path=self.POSTGRES_DB,
        )
        return str(url)

    @computed_field
    @property
    def mqtt_url(self) -> str:
        """
        Создает URL для подключения к MQTT.
        """
        auth_part = (
            f"{self.MQTT_USERNAME}:{self.MQTT_PASSWORD}@" if self.MQTT_USERNAME else ""
        )
        return f"mqtt://{auth_part}{self.MQTT_HOST}:{self.MQTT_PORT}"


settings = Settings()
