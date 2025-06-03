# Moving Average

import matplotlib.pyplot as plt
from pandas import DataFrame
from utils.constants import Indicators, PriceFields
from utils.common import export_plot_image, indicator_column, indicator_label

# Simple Moving Averages
def enrich_sma(df: DataFrame, period: int = 20):
    df = df.copy()
    
    column = indicator_column(Indicators.SMA, period)
    df[column] = df[PriceFields.CLOSE].rolling(window=period).mean()
    
    return df

def plot_sma(
    df: DataFrame,
    symbol: str,
    periods: list[int] = [20],
    ax=None,
    save=False,
    show=True,
):
    standalone = ax is None
    if standalone:
        fig, ax = plt.subplots(figsize=(14, 5))

    ax.plot(df[PriceFields.CLOSE], label='Close Price', color='gray', alpha=0.5)

    for period in periods:
        column = indicator_column(Indicators.SMA, period)
        label = indicator_label(Indicators.SMA, period)
        ax.plot(df[column], label=label, linewidth=2)

    ax.set_title(f'{symbol} {label}')
    ax.set_ylabel('Price')
    ax.grid()
    ax.legend()

    if save and standalone:
        export_plot_image(fig, symbol, label)

    if show and standalone:
        plt.tight_layout()
        plt.show()
    elif standalone:
        plt.close()

# Exponential Moving Averages
def enrich_ema(df: DataFrame, period: int = 13):
    df = df.copy()

    column = indicator_column(Indicators.EMA, period)
    df[column] = df[PriceFields.CLOSE].ewm(span=period, adjust=False).mean()
    
    return df

def plot_ema(
    df: DataFrame,
    symbol: str,
    periods: list[int] = [13],
    ax=None,
    save=False,
    show=True,
):
    standalone = ax is None
    if standalone:
        fig, ax = plt.subplots(figsize=(14, 5))

    ax.plot(df[PriceFields.CLOSE], label='Close Price', color='gray', alpha=0.5)
    
    for period in periods:
        column = indicator_column(Indicators.EMA, period)
        label = indicator_label(Indicators.EMA, period)
        ax.plot(df[column], label=label, linewidth=2)

    ax.set_title(f'{symbol} {label}')
    ax.set_ylabel('Price')
    ax.grid()
    ax.legend()

    if save and standalone:
        export_plot_image(fig, symbol, label)

    if show and standalone:
        plt.tight_layout()
        plt.show()
    elif standalone:
        plt.close()
