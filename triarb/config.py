import json
from typing import Dict, List, Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    EXCHANGE: str = "binance"
    QUOTE: str = "USDT"
    TRI_SYMBOLS: str = "BTC,ETH,BNB"
    TOP_LEVELS: int = 3
    PAPER_MODE: bool = True
    TARGET_NOTIONAL_QUOTE: float = 10000.0
    MIN_GROSS_EDGE_BPS: float = 40.0
    MIN_NET_EDGE_BPS: float = 10.0
    SLIPPAGE_BPS: float = 5.0
    FEE_TABLE_JSON: str = '{"binance":{"taker":0.0004,"maker":0.0002}}'
    MAX_LEG_NOTIONAL_QUOTE: float = 20000.0
    MAX_OPEN_CYCLES: int = 1
    PRICE_TICK_BUFFER_BPS: float = 3.0
    REDIS_URL: str = "redis://redis:6379/0"
    DB_URL: str = "postgresql+asyncpg://postgres:postgres@db:5432/triarb"
    ADMIN_PORT: int = 8081

    BINANCE_API_KEY: str | None = None
    BINANCE_API_SECRET: str | None = None

    FEE_TABLE: Dict[str, Dict[str, float]] = {}

    @field_validator("FEE_TABLE", mode='before')
    def parse_fee_table(cls, v, values):
        fee_json = values.data.get("FEE_TABLE_JSON")
        if fee_json and isinstance(fee_json, str):
            return json.loads(fee_json)
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
