"""Use Yahoo Finance to retrieve data data"""
import pandas as pd
import yfinance as yf
import os 


def get_data(symbol='AAPL', period='1d', days=365):
    """Retrieve daily data for symbol

    days is the number of (calendar) days back from today to retrieve

    docstring of yfinance.Ticker.history

    period : str
        Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        Either Use period parameter or use start and end
    interval : str
        Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        Intraday data cannot extend last 60 days
    start: str
        Download start date string (YYYY-MM-DD) or _datetime.
        Default is 1900-01-01
    end: str
        Download end date string (YYYY-MM-DD) or _datetime.
        Default is now
    prepost : bool
        Include Pre and Post market data in results?
        Default is False
    auto_adjust: bool
        Adjust all OHLC automatically? Default is True
    back_adjust: bool
        Back-adjusted data to mimic true historical prices
    proxy: str
        Optional. Proxy server URL scheme. Default is None
    rounding: bool
        Round values to 2 decimal places?
        Optional. Default is False = precision suggested by Yahoo!
    tz: str
        Optional timezone locale for dates.
        (default data is returned as non-localized dates)
    """
    s = yf.Ticker(symbol)
    date_to = pd.Timestamp.utcnow().tz_convert('US/Central').floor('D')
    date_from = date_to - pd.Timedelta(days=days)
    fd = lambda x: x.isoformat()[:10]
    df = s.history(start=date_from, end=date_to, period='max', ).reset_index()
    df.columns = [x.lower().replace(' ', '_') for x in df.columns]
    df['date'] = pd.to_datetime(df['date'])

    return df.sort_values(by=['date']).reset_index(drop=True)
