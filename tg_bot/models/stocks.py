from typing import List, Optional

from pydantic import BaseModel, Field


class TickerBase(BaseModel):
    """Базовая информация по тикеру"""

    short_name: Optional[str] = Field(None, alias="shortName")
    symbol: str
    currency: str = Field(None)
    two_hundred_day_average: float = Field(None, alias="twoHundredDayAverage")
    fifty_day_average: float = Field(None, alias="fiftyDayAverage")
    fifty_two_week_average: float = Field(None, alias="fiftyTwoWeekHigh")
    fifty_two_week_low: float = Field(None, alias="fiftyTwoWeekLow")
    previous_close: float = Field(None, alias="regularMarketPreviousClose")
    market_open: float = Field(None, alias="regularMarketOpen")
    current_price: float = Field(..., alias="regularMarketPrice")
    day_high: float = Field(None, alias="dayHigh")
    day_low: float = Field(None, alias="dayLow")


class TickersList(BaseModel):
    """Информация для группы тикеров"""

    tickers: List[TickerBase]


# TODO: добавить поддержку тикеров компаний
class CompanyTicker(TickerBase):
    """Информация по тикерам компаний"""

    city: str
    country: str
    industry: str
