# fetch_prices.py

from datetime import datetime
import yfinance as yf
import pandas as pd
from pathlib import Path

from indicators.ma import enrich_ema, enrich_sma
from indicators.macd import enrich_macd
from indicators.rsi import enrich_rsi
from indicators.volatility import enrich_atr, enrich_volatility_std
from utils.common import save_csv
from utils.constants import Indicators, PriceFields

def fetch_data(symbol, start='2024-01-01', end=None):
    print(f"Fetching: {symbol}")
    if end is None:
        end = datetime.now()
    
    df = yf.download(symbol, start=start, end=end, auto_adjust=False)

    # Flatten multi-index columns if present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df[Indicators.RETURN] = df[PriceFields.CLOSE].pct_change()
    df = enrich_sma(df, 20)
    df = enrich_sma(df, 50)
    df = enrich_ema(df, 13)
    df = enrich_ema(df, period=21)
    df = enrich_rsi(df, period=14)
    df = enrich_macd(df, 12, 26, 9)
    df = enrich_volatility_std(df, 20)
    df = enrich_atr(df)
    
    return df
