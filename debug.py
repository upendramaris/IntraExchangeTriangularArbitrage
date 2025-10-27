from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    TRI_SYMBOLS: List[str]

    class Config:
        pass

settings = Settings()

print(settings.TRI_SYMBOLS)
