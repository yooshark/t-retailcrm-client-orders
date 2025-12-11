import logging
from pathlib import Path
from typing import Self, Any

from pydantic_settings import BaseSettings, SettingsConfigDict
logger = logging.getLogger('app')

ENV_FILE = Path.cwd() / '.env'


class InjectableSettings(BaseSettings):
    @classmethod
    def new(cls) -> Self:
        return cls()



class AppSettings(InjectableSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_prefix='APP_',
        extra='ignore',
    )

    DEBUG: bool = True
    DEVELOP: bool = True

    NAME: str = 'app'
    VERSION: str = '0.1.0'
    ENVIRONMENT: str = 'local'


    ALLOW_ORIGINS: list[str] = [
        'http://localhost:8000',
    ]
    ALLOW_ORIGIN_REGEX: str | None = r'https://(.*\.)?localhost\.com'

    @staticmethod
    def get_develop_settings() -> dict[str, Any]:
        return {
            'host': 'localhost',
            'port': 8000,
            'reload': True,
        }

    @staticmethod
    def get_prod_settings() -> dict[str, Any]:
        return {
            'host': '0.0.0.0',
            'port': 80,
        }


class RetailCRMSettings(InjectableSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_prefix='RETAILCRM_',
        extra='ignore',
    )

    API_KEY: str
    API_VERSION: int = 5
    SUBDOMAIN: str
    HTTP_TIMEOUT: int = 10

    @property
    def base_url(self) -> str:
        return f'https://{self.SUBDOMAIN}.retailcrm.ru'
