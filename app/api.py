from fastapi import APIRouter, Depends
from .schemas import PriceSchema, PriceQueryParams, PriceRangeQueryParams
from typing import List
from .services import (
    get_latest_price_service,
    get_price_history_service,
    get_price_range_service
)


router = APIRouter(prefix="/prices", tags=["Prices"])

# Latest price
@router.get("/latest", response_model=PriceSchema)
async def get_latest_price(params: PriceQueryParams = Depends()):
    return await get_latest_price_service(params.ticker)

# All price history
@router.get("/history", response_model=List[PriceSchema])
async def get_price_history(params: PriceQueryParams = Depends()):
    return await get_price_history_service(params.ticker)

# Price range
@router.get("/range", response_model=List[PriceSchema])
async def get_price_range(params: PriceRangeQueryParams = Depends()):
    return await get_price_range_service(params.ticker, params.start, params.end)

