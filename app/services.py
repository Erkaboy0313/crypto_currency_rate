import time, aiohttp, asyncio
from .models import Price
from .logger import logger
from .schemas import TickerEnum
from typing import List
from fastapi import HTTPException

DERIBIT_INDEX_URL = "https://www.deribit.com/api/v2/public/get_index_price"

async def fetch_and_store_prices() -> None:
    tickers = {
        "BTC_USD": "btc_usd",
        "ETH_USD": "eth_usd",
    }

    timestamp = int(time.time())

    async with aiohttp.ClientSession() as session:
        for ticker, index_name in tickers.items():
            params = {"index_name": index_name}

            try:
                async with session.get(DERIBIT_INDEX_URL, params=params, timeout=10) as response:
                    if response.status != 200:
                        logger.warning(f"{ticker}: HTTP {response.status}, skipping")
                        continue

                    data = await response.json()

                    if "result" not in data or "index_price" not in data["result"]:
                        logger.warning(f"{ticker}: Missing 'index_price' in response, skipping")
                        continue

                    price = data["result"]["index_price"]

                    if not isinstance(price, (int, float)):
                        logger.warning(f"{ticker}: Invalid price type {type(price)}, skipping")
                        continue

                    await Price.create(
                        ticker=ticker,
                        price=price,
                        timestamp=timestamp,
                    )

                    logger.info(f"Saved {ticker}: {price} at {timestamp}")

            except aiohttp.ClientError as e:
                logger.error(f"{ticker}: Client error: {e}")
            except asyncio.TimeoutError:
                logger.error(f"{ticker}: Request timed out")
            except Exception as e:
                logger.error(f"{ticker}: Unexpected error: {e}")
                
async def get_latest_price_service(ticker: TickerEnum):
    """Return the latest price for a given ticker"""
    price_obj = await Price.filter(ticker=ticker.value).order_by("-timestamp").first()

    if not price_obj:
        raise HTTPException(status_code=404, detail=f"No price found for {ticker.value}")
    
    return price_obj

async def get_price_history_service(ticker: TickerEnum) -> List[Price]:
    """Return all prices for a given ticker"""
    price_objs = await Price.filter(ticker=ticker.value).order_by("-timestamp").all()
    if not price_objs:
        raise HTTPException(status_code=404, detail=f"No price history found for {ticker.value}")

    return price_objs

async def get_price_range_service(ticker: TickerEnum, start: int, end: int) -> List[Price]:
    """Return prices in a specific range"""
    if start > end:
        raise HTTPException(status_code=400, detail="Start timestamp cannot be greater than end timestamp")

    price_objs = await Price.filter(
        ticker=ticker.value,
        timestamp__gte=start,
        timestamp__lte=end
    ).order_by("timestamp").all()
    if not price_objs:
        raise HTTPException(status_code=404, detail=f"No prices found for {ticker.value} in this range")                
    return price_objs

