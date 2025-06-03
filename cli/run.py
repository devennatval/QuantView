import argparse
import pandas as pd
from core.fetch import fetch_data
from core.plot import plot_multiple_indicators
from indicators.ma import plot_ema, plot_sma
from indicators.macd import plot_macd
from indicators.rsi import plot_rsi
from indicators.volatility import plot_atr, plot_volatility_std
from utils.common import get_csv_data_path, save_csv
from utils.constants import Indicators

def run_cli():
    parser = argparse.ArgumentParser(description="QuantView CLI")
    parser.add_argument('--symbol', required=True, help="Ticker symbol (e.g. BTC-USD, AAPL)")
    parser.add_argument('--indicators', nargs='+', choices=['sma', 'ema', 'rsi', 'macd', 'atr', 'volatility'], default=[], help="Indicators to plot")
    parser.add_argument('--dashboard', action='store_true', help="Show full dashboard (SMA, RSI, MACD)")
    parser.add_argument('--save', action='store_true', help="Save plots to PNG")
    parser.add_argument('--no-show', action='store_true', help="Suppress plot windows")
    parser.add_argument('--fetch', action='store_true', help="Force fetch data again from Yahoo Finance")

    args = parser.parse_args()

    symbol = args.symbol
    save = args.save
    show_plot = not args.no_show

    if args.fetch:
        df = fetch_data(symbol)
        save_csv(df, symbol)
    else:
        df_path = get_csv_data_path(symbol)
        df = pd.read_csv(df_path, parse_dates=["Date"], index_col="Date")

    if args.dashboard:
        plot_multiple_indicators(df, symbol, indicators=[Indicators.EMA, Indicators.RSI, Indicators.MACD, Indicators.ATR], save=args.save, show=show_plot)
    else:
        if 'sma' in args.indicators:
            plot_sma(df, symbol=symbol, save=save, show=show_plot)
        if 'ema' in args.indicators:
            plot_ema(df, symbol=symbol, save=save, show=show_plot)
        if 'rsi' in args.indicators:
            plot_rsi(df, symbol=symbol, save=save, show=show_plot)
        if 'macd' in args.indicators:
            plot_macd(df, symbol=symbol, save=save, show=show_plot)
        if 'atr' in args.indicators:
            plot_atr(df, symbol=symbol, save=save, show=show_plot)
        if 'volatility' in args.indicators:
            plot_volatility_std(df, symbol=symbol, save=save, show=show_plot)
