from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class TickerEnum(str, Enum):
    BTC_USD = "BTC_USD"
    ETH_USD = "ETH_USD"

class PriceQueryParams(BaseModel):
    ticker: TickerEnum = Field(..., description="Ticker symbol")

class PriceRangeQueryParams(PriceQueryParams):
    start: int = Field(..., description="Start timestamp (UNIX)")
    end: int = Field(..., description="End timestamp (UNIX)")


class PriceSchema(BaseModel):
    ticker: str
    price: float
    timestamp: int  # UNIX timestamp
    created_at: datetime

    class Config:
        from_attributes = True
        
    