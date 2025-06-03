import argparse
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from indicators import rsi, ma, macd, volatility

from utils.common import export_plot_image
from utils.constants import Indicators, PriceFields

def plot_price(df, symbol: str, ax=None, show=True, save=False):
    standalone = ax is None
    if standalone:
        fig, ax = plt.subplots(figsize=(14, 4))

    label = "Close Price"

    ax.plot(df[PriceFields.CLOSE], label=label, color='black')
    ax.set_title(f"{symbol} - {label}")
    ax.grid()
    ax.legend()

    if save and standalone:
        export_plot_image(fig, symbol, label)
        
    if show and standalone:
        plt.tight_layout()
        plt.show()
    elif standalone:
        plt.close()

def plot_multiple_indicators(df, symbol: str, indicators: list[str], show=True, save=False):
    plot_dispatch = {
        Indicators.RSI: lambda ax: rsi.plot_rsi(df, symbol, ax=ax, show=False),
        Indicators.MACD: lambda ax: macd.plot_macd(df, symbol, ax=ax, show=False),
        Indicators.ATR: lambda ax: volatility.plot_atr(df, symbol, ax=ax, show=False),
        Indicators.VOLATILITY: lambda ax: volatility.plot_volatility_std(df, symbol, ax=ax, show=False),
        Indicators.SMA: lambda ax: ma.plot_sma(df, symbol, periods=[20, 50], ax=ax, show=False),
        Indicators.EMA: lambda ax: ma.plot_ema(df, symbol, periods=[13, 21], ax=ax, show=False),
    }

    n = len(indicators)
    fig, axs = plt.subplots(n, 1, figsize=(14, 3 * n), sharex=True)

    if n == 1:
        axs = [axs]

    for ax, name in zip(axs, indicators):
        if name in plot_dispatch:
            plot_dispatch[name](ax)
        else:
            ax.set_title(f"Unknown indicator: {name}")
            ax.grid()

    if save:
        export_plot_image(fig, symbol, "Multi")
        
    if show :
        plt.tight_layout()
        plt.show()
