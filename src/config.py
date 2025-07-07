import sys
from pydantic_settings import BaseSettings, SettingsConfigDict
import locale
from typing import Optional
from dotenv import load_dotenv

if sys.platform == "win32":
    locale.setlocale(locale.LC_ALL, "rus_rus")
else:
    locale.setlocale(locale.LC_ALL, ("ru_RU", "UTF-8"))

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    APP_HOST: str = '0.0.0.0'
    APP_PORT: int = 8000
    REDIS_HOST: str = 'redis'
    REDIS_PORT: int = 6379
    RABBIT_HOST: str = 'rabbitmq'
    RABBIT_PORT: int = 5672
    RABBIT_USER: str = 'guest'
    RABBIT_PASS: str = 'guest'
    SERVICE_A_URL: str = 'http://web_a:8000/api/v1/equipment/cpe/'

settings = Settings()
