from typing import List

from tg_bot.models.stocks import TickerBase, TickersList
import yfinance as yf


def get_tickers(ticker_list: List[str]) -> TickersList:
    """Get tickers info and return them as TickersList"""
    ticks = yf.Tickers((" ").join(ticker_list))
    ticks = TickersList(tickers=[TickerBase(**tick.info)
                                 for tick in ticks.tickers.values()])
    return ticks


def get_ticker_info(ticker: str) -> yf.Ticker:
    """Get ticker info"""
    tick = yf.Ticker(ticker)
    return tick.info
